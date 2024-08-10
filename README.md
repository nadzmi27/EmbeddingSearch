🔎 [Click here to access the application](https://animesearch.streamlit.app/)

📒 [Click here to access the Kaggle notebook](#)

# Background

# Architecture
![image](https://github.com/user-attachments/assets/8cdabe41-72ef-40dc-b25b-3ed5f601f9f8)
a) **Scraping:** The data is scraped from MyAnimeList using `requests` alongside `pickle` and `logging` to safeguard against failure, allowing the collection across different runtimes.
b) **Cleaning:** The data is cleaned using `pandas`
c) **Preprocessing**
d,g) **Vectorization**
h) **Matching**
i) **Retrieve Candidates**
j) **Pass Candidates + Query**
k) **Filter**: 
l) **Return**: The filtered top anime will be displayed on the application.


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
