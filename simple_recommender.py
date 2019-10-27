"""Have a recommender engine that randomly returns 5 movies from a CSV"""

import pandas as pd
import random

path = 'Your csv path'

def recommend_movies():
    df = pd.read_csv(path)
    titles = df['title'].unique()
    random.shuffle(titles)
    result = list(titles[:5])

    return result
