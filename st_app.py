# Import dependencies
import streamlit as st
import pandas as pd
import Script

#

# Set page title
st.set_page_config(
    page_title="AniSearch",
    page_icon=":mag:",
)

anime_filtered = pd.read_csv('AnimeFiltered.csv')

# Description
st.header(":rainbow[AniSearch!] :mag:", divider='rainbow')

st.write(
    "AniSearch help you find the anime you want based on given description. \
    It leverages the use of **Vector Embeddings** to turn query and textual information provided by \
    [MyAnimeList](https://myanimelist.net/topanime.php) into vector of numbers. \
    The vector query will be matched to several anime based on the similarity of the encoding. \
    For more information please visit my [github repo](https://www.youtube.com/watch?v=BbeeuzU5Qc8)"
)

st.divider()


query = st.text_input("Anime description:", placeholder="E.g. Time travel murder mystery")
top_n = st.slider("Top n-th anime:", 100, anime_filtered.shape[0], 5000, 100)
searched = st.button("Search")

if searched:
    df_output = Script.find_anime(query, n_rows=top_n)
    df_output.index += 1
    try:
        st.dataframe(df_output)
    except:
        st.dataframe(df_output.astype(str))