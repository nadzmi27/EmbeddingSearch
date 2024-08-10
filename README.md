🔎 To access the app online please [click here](https://animesearch.streamlit.app/)  
📒 For more details about the embedding [access the Kaggle notebook here](#)

# Background

# Architecture
![image](https://github.com/user-attachments/assets/8cdabe41-72ef-40dc-b25b-3ed5f601f9f8)
- **Scraping (a):** The data is scraped from MyAnimeList using `requests` alongside `pickle` and `logging` to safeguard against failure, allowing the collection across different runtimes.
- **Cleaning (b) :** The data is cleaned using `pandas`
- **Preprocessing (c):**
- **Vectorization (d,g):**
- **Matching (h):**
- **Retrieve Candidates (i):**
- **Pass Candidates + Query (j)**
- **Filter (k):**
- **Return (l):** The filtered top anime will be displayed on the application.


# EmbeddingSearch
Searching for recommendations using vector embedding. I am currently trying to make it work for the Anime Dataset from MAL

### TODO:
GitHub:
- [ ] Documentation
- [x] Architecture
- [x] Deploy online
- [x] Add data scraping
- [ ] Put your .ipynb from Kaggle here

Streamlit:
- [ ] Format displayed df 
- [ ] Change theme
- [ ] Provide a better description
- [ ] Improve the UI

Future:
- [ ] Add recommendation system
