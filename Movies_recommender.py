import streamlit as st
import pickle
import requests
import pandas as pd 
import numpy as np
st.title('Movies Recommender System')

movies_df = pickle.load(open('movie_list.pkl','rb'))
similarity = pickle.load(open('similarity.pkl','rb'))

def fetch_poster(movie):
    movie_id = movies_df[movies_df['title'] == movie]['movie_id'].values[0]
    r = requests.get(f'https://api.themoviedb.org/3/movie/{movie_id}?api_key=b3392527287b99de327851062bf65c80')
    data = r.json()
    return 'https://image.tmdb.org/t/p/w500/'+data['poster_path']

def recommend(movie_name):
    lst_movies_poster = []
    header_name = []
    index = movies_df[movies_df['title'] == movie_name].index[0]
    distances = sorted(list(enumerate(similarity[index])),reverse=True,key = lambda x: x[1])
    for i in distances[1:11]:
        movie = movies_df.iloc[i[0]].title
        movie_poster = fetch_poster(movie)
        header_name.append(movie)
        lst_movies_poster.append(movie_poster)

    row1 = st.columns(5)

    while True:
        for number,value in enumerate(row1) :
            with value :
                image = st.image(lst_movies_poster[number])
                st.write(header_name[number])

        for number,value in enumerate(row1) :
            with value :
                    image = st.image(lst_movies_poster[5+number])
                    st.write(header_name[5+number])
        break

option = st.selectbox(
     'Select your movie',
    movies_df['title'].values)

rcmd_btn = st.button('Recommend')
if rcmd_btn : 
    recommend(option)

