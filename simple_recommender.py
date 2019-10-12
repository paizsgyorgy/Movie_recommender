"""Have a recommender engine that randomly returns 5 movies from the CSV"""

import pandas as pd
import random

def recommend_movies():
    df = pd.read_csv('/Users/paizsgyorgy/Coding/spiced-academy/Week7/Movie recommender/Data/ml-latest-small/movies.csv')
    titles = df['title'].unique()
    random.shuffle(titles)
    result = list(titles[:5])

    return result
