#!/usr/bin/python3
from flask import Flask, request, render_template, jsonify
from auth_spotify import token
import requests
import mysql.connector
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

app = Flask(__name__)

# MySQL connection configuration
mysql_host = 'localhost'
mysql_user = 'root'
mysql_password = 'prosperity'
mysql_database = 'music_app'

connection = mysql.connector.connect(
    host=mysql_host,
    user=mysql_user,
    password=mysql_password,
    database=mysql_database
)

user_headers = {
    "Authorization": "Bearer " + token,
    "Content-Type": "application/json"
}
BASE_URL = 'https://api.spotify.com/'
user_params = {
    "limit": 50
}


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/search", methods=["POST"])
def search():
    query = request.form.get("query")
    print(query)  # Get the query from the form

    # Perform recommendation based on the query
    results = perform_recommendation(query)
    return render_template("results.html", results=results)


@app.route("/recommend", methods=["GET"])
def recommend():
    # Get the query parameter from the request
    query = request.args.get("query")

    # Perform recommendation based on the query and get the results
    results = perform_recommendation(query)

    return jsonify(results)


def perform_recommendation(query):
    data = {
        'q': query,
        'type': 'track'
    }
    return_search = requests.get(
        BASE_URL + 'v1/search',
        params=data,
        headers=user_headers)
    return_searchs = return_search.json()

    track_id = return_searchs['tracks']['items'][0]['id']
    search_recommendations = requests.get(
        BASE_URL + 'v1/recommendations/',
        params={
            'seed_tracks': track_id
        },
        headers=user_headers)
    search_recommendation = search_recommendations.json()
    list_of_recommendaton = search_recommendation['tracks']
    recommended_song = []
    for recommendation in list_of_recommendaton:
        # print(recommendation)
        song = recommendation['name'] + ' By ' + \
            recommendation['artists'][0]['name']
        recommended_song.append(song)

    # Perform content-based filtering using TF-IDF vectorization
    # vectorizer = TfidfVectorizer()
    # tfidf_matrix = vectorizer.fit_transform(
    #     [entry[1] for entry in preprocessed_data])

    # # Get the user input's TF-IDF vector
    # user_input_tfidf = vectorizer.transform([query])

    # # Calculate the cosine similarity between user input and preprocessed data
    # similarity_scores = cosine_similarity(user_input_tfidf, tfidf_matrix)

    # # Get the indices of top similar songs
    # top_similar_indices = similarity_scores.argsort()[0][-5:][::-1]

    # Get the recommended songs based on the indices
    # recommended_songs = [preprocessed_data[index]
    #                      for index in top_similar_indices]

    return recommended_song


if __name__ == "__main__":
    app.run()
