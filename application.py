from flask import Flask, render_template, request
from NMF_recommender import recommend_movies_nmf


## Instantiate Flask, make application.py the web application
app = Flask(__name__)

## Decorator for the home page
@app.route("/")
@app.route("/home")
def hello():
    return render_template('index.html')

@app.route("/recommendation")
def recommend():
    results_dictionary = request.args

    movies = recommend_movies_nmf(results_dictionary)

    return render_template('recommendation.html', movies_html=movies)

app.run()
