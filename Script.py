# Import libraries
import pandas as pd # Data processing, CSV file I/O (e.g. pd.read_csv)
import numpy as np # Linear algebra
from scipy import stats
from sentence_transformers import SentenceTransformer, CrossEncoder, util # Sentence embedding and similarity
import torch
import streamlit as st

# Specify device
device = "cuda:0" if torch.cuda.is_available() else "cpu"

# We will use bi_encoder available from Sentence Transformer library
bi_encoder_name = 'all-distilroberta-v1' # 512 max sequence length
bi_encoder = SentenceTransformer('all-distilroberta-v1')
top_k = 100 #Number of passages we want to retrieve with the bi-encoder

#The bi-encoder will retrieve 100 documents. We use a cross-encoder, to re-rank the results list to improve the quality
cross_encoder = CrossEncoder('cross-encoder/ms-marco-MiniLM-L-6-v2')

# Read the csv
anime_filtered = pd.read_csv('AnimeFiltered.csv')
anime_filtered.index.name = "Rank"

# Read the corpus embeddings and corpus
ce1 = np.load("CE1.npy")
ce2 = np.load("CE2.npy")
ce3 = np.load("CE3.npy")
corpus_embeddings = np.concatenate((ce1, ce2, ce3))

corpus = anime_filtered.DescriptionAugmented.to_list()
columns = ['Name', 'EnglishName', 'Description', 'Type', 'Genres', 'Demographics', 
           'Episodes', 'Themes', 'Score', 'Ranked', 'Popularity', 'Members', 'Favorites']

# MinMax Scaler to restrict value between 0 and 1
def minmax_scaler(col, invert=False, boxcox=False):
    arr = col.to_numpy()
    if boxcox:
        mn = arr.min()
        if mn <= 0:
            arr += -mn + 1 # Make the data positive and non-zero
        arr = stats.boxcox(arr)[0]
    if invert:
        arr = -arr
    mx = arr.max()
    mn = arr.min()
    return (arr - mn)/(mx - mn)

# Search for vector embeddings that are similar to query using bi_encoder
def semantic_search(query, corpus_embeddings=corpus_embeddings, n_rows=5000, top_k=top_k):
    # Encode the query using the bi-encoder and find potentially relevant description
    if device == 'cuda:0':
        question_embedding = bi_encoder.encode(query, convert_to_tensor=True, show_progress_bar=True)
        question_embedding = question_embedding.cuda()
    else:
        question_embedding = bi_encoder.encode(query, convert_to_tensor=False, show_progress_bar=True)
        
    hits = util.semantic_search(question_embedding, corpus_embeddings[:n_rows], top_k=top_k)
    hits = hits[0]
    
    # Now, score all retrieved passages with the cross_encoder
    cross_inp = [[query, corpus[hit['corpus_id']]] for hit in hits]
    cross_scores = cross_encoder.predict(cross_inp, show_progress_bar=True)
    
    # Include cross-encoder scores
    for idx in range(len(cross_scores)):
        hits[idx]['cross-score'] = cross_scores[idx]
    return hits

# Function for adding weights to the hits
def add_weight(n_rows=5000):
    # Restrict score value to 0-1
    score_scaled = anime_filtered['Score'].iloc[:n_rows].map(lambda x: x/10)
    popularity_scaled = minmax_scaler(anime_filtered['Popularity'].iloc[:n_rows], boxcox=True, invert=True) # Lower is better
    favorites_scaled = minmax_scaler(anime_filtered['Favorites'].iloc[:n_rows], boxcox=True)
    
    # W1 is the geometric mean of ScoreScaled and PopularityScaled
    # W2 is the geometric mean of ScoreScaled, PopularityScaled, and FavoritesScaled
    # Favorite is correlated with Popularity
    
    w1 = score_scaled*popularity_scaled
    w2 = w1*favorites_scaled

    w1 = np.sqrt(w1)
    w2 = np.cbrt(w2)

    return w1, w2

# Function for filtering the hits
def hits_filter(hits, n_rows=5000, n=6, cs_threshold=-8):
    w1, w2 = add_weight(n_rows)
    
    for i in range(len(hits)):
        hits[i]['w1'] = w1[hits[i]['corpus_id']]
        hits[i]['w2'] = w2[hits[i]['corpus_id']]
    
    #
    hits = sorted(hits, key=lambda x: x['cross-score'], reverse=True)
    cs = [x['corpus_id'] for x in hits[:n] if x['cross-score'] >= cs_threshold]
    csmin = hits[-1]['cross-score']
    
    hits = sorted(hits, key=lambda x: (x['cross-score'] - csmin + 0.1)*x['w1'], reverse=True)
    csw1 = [x['corpus_id']for x in hits[:n] if x['cross-score'] >= cs_threshold]

    hits = sorted(hits, key=lambda x: (x['cross-score'] - csmin + 0.1)*x['w2'], reverse=True)
    csw2 = [x['corpus_id'] for x in hits[:n] if x['cross-score'] >= cs_threshold]
    
    #
    hits = sorted(hits, key=lambda x: x['score'], reverse=True)
    s = [x['corpus_id'] for x in hits[:n] if x['cross-score'] >= cs_threshold]
    
    hits = sorted(hits, key=lambda x: x['score']*x['w1'], reverse=True)
    sw1 = [x['corpus_id'] for x in hits[:n] if x['cross-score'] >= cs_threshold]

    hits = sorted(hits, key=lambda x: x['score']*x['w2'], reverse=True)
    sw2 = [x['corpus_id'] for x in hits[:n] if x['cross-score'] >= cs_threshold]
    
    # Combine
    ss = set(sw1).union(sw2).union(s)
    css = set(csw1).union(csw2).union(cs)
    combined = list(ss.union(css))
    
    return combined

@st.cache_data # To save space and time when working with streamlit
def find_anime(query, sort_rank=False, corpus_embeddings=corpus_embeddings, n_rows=5000, top_k=100, n=6, cs_threshold=-8):
    hits = semantic_search(query, corpus_embeddings, n_rows, top_k)
    idx = hits_filter(hits, n_rows, n, cs_threshold)
    if sort_rank:
        return anime_filtered.iloc[idx].sort_values("Score", ascending=False)
    else:
        df = pd.DataFrame(hits)
        cs_min = df["cross-score"].min()
        df = df[df.corpus_id.isin(idx)]
        idx = np.argsort((df['cross-score'] - cs_min + 0.1)*df['w2'])[::-1]
        df = df.iloc[idx]
        idx = df.corpus_id
        return anime_filtered.iloc[idx]
    
