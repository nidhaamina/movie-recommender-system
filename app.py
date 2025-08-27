import streamlit as st
import pickle
import pandas as pd
import requests


st.set_page_config(
    page_title="🎬 Movie Recommender",
    page_icon="🎥",
    layout="wide",
)


st.markdown("""
    <style>
    .stApp {
        background-color: #0d0d0d;
        color: #ffffff;
    }
    h1, h2, h3 {
        color: #e50914 !important;
        text-align: center;
    }
    .stSelectbox>div>div {
        background-color: #1a1a1a;
        color: white;
        border: 2px solid #e50914;
        border-radius: 8px;
    }
    .stButton>button {
        background-color: #e50914;
        color: white;
        border-radius: 8px;
        padding: 0.6em 1.2em;
        font-size: 16px;
        font-weight: bold;
        transition: 0.3s;
    }
    .stButton>button:hover {
        background-color: #b20710;
        transform: scale(1.05);
    }
    /* Hover effect for posters */
    .movie-poster {
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        border-radius: 12px;
    }
    .movie-poster:hover {
        transform: scale(1.08);
        box-shadow: 0px 8px 20px rgba(229, 9, 20, 0.8);
    }
    .movie-title {
        text-align: center;
        font-size: 16px;
        color: #ffffff;
        margin-top: 8px;
    }
    </style>
""", unsafe_allow_html=True)



def fetch_poster(movie_id):
    response = requests.get(
        f'https://api.themoviedb.org/3/movie/{movie_id}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US'
    )
    data = response.json()
    return "https://image.tmdb.org/t/p/w500/" + data['poster_path']

def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_movies_posters = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_movies_posters.append(fetch_poster(movie_id))
    return recommended_movies, recommended_movies_posters



movies_dict = pickle.load(open('movie_dict.pkl','rb'))
movies = pd.DataFrame(movies_dict)
similarity = pickle.load(open('similarity.pkl','rb'))


st.markdown("<h1>🍿 Movie Recommender System</h1>", unsafe_allow_html=True)


selected_movie_name = st.selectbox(
    "🎥 Select a movie you like:",
    movies['title'].values
)


if st.button("🔥 Recommend"):
    names, posters = recommend(selected_movie_name)

    st.markdown("<h2>Top 5 Recommendations</h2>", unsafe_allow_html=True)
    cols = st.columns(5, gap="large")
    for idx, col in enumerate(cols):
        with col:
            st.markdown(
                f"<img src='{posters[idx]}' class='movie-poster' width='100%'>",
                unsafe_allow_html=True
            )
            st.markdown(f"<p class='movie-title'>{names[idx]}</p>", unsafe_allow_html=True)
