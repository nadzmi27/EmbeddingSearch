# Import dependencies
import streamlit as st
from streamlit.column_config import LinkColumn
import pandas as pd
import script

#

# Set page title
st.set_page_config(
    page_title="AniSearch",
    page_icon=":mag:",
)

anime_filtered = pd.read_csv('Data/AnimeFiltered.csv')
anime_filtered = anime_filtered[:15000]

# Description
st.header(":rainbow[AniSearch!] :mag:", divider='rainbow')

st.write(
    "AniSearch help you find the anime you want based on given description. \
    It leverages the use of **Vector Embeddings** to turn query and textual information provided by \
    [MyAnimeList](https://myanimelist.net/topanime.php) into vector of numbers. \
    The vector query will be matched to several anime based on the similarity of the encoding. \
    \n\n The purpose of this project is to teach myself about embeddings and encoders. \
    The same concept can be applied to Movies, TV Series, Books and even images/audio. \
    For more information please visit my [GitHub repo](https://github.com/nadzmi27/EmbeddingSearch)"
)

st.divider()


query = st.text_input("Anime Description:", placeholder="E.g. Time travel murder mystery")
top_n = st.slider("Top n-th anime:", 100, anime_filtered.shape[0], 5000, 100)
searched = st.button("Search")

if query or searched:
    df_output = script.find_anime(query, n_rows=top_n)
    cols = ['Title', 'Url', 'Description', 'Type', 'Episodes', 'Score', 'Popularity', 'Genres', 'Themes', 'Demographics']
    df_output = df_output[cols]
    df_output.index += 1

    column_config = {
        'Url': LinkColumn(
            "MAL Page",
            help="Click to view the Anime page",
            validate="^https://[a-z]+\.com$",
            display_text="More details"
        )
    }

    try:
        # st.dataframe(df_output, column_config=column_config)
        st.caption("Click the description twice to expand")
        st.dataframe(
            df_output,
            column_config=column_config,
            hide_index=False
        )
    except:
        st.dataframe(df_output.astype(str))