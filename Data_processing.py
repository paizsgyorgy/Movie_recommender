"""This is a module that processes the user input and appends it to
    the Postgres database behind that stores all ratings and other info"""

import pandas as pd
import numpy as np
import pickle
from sqlalchemy import create_engine
import time

example_input = {   "1721": 5,
                    "3578": 5,
                    "318": 5,
                    "296": 5,
                    "2959": 5
                }

## Connect to database with SQL alchemy
host = 'localhost'
database = 'movies'
con = f'postgres://{host}/{database}'
db = create_engine(con, encoding='latin1', echo=False)

## Get maximum userId currently in database and append with 1 for new user input
query = f"""SELECT max(ratings."userId") FROM RATINGS;"""
max_userId = pd.read_sql(query, db).values[0][0]
new_userId = max_userId + 1

## Get current timestamp
timestamp = time.time()

## Create table format to be appended to the database
movie_id = []
user_id = []
ratings = []
time = []
for key in example_input:
    user_id.append(new_userId)
    time.append(timestamp)
    movie_id.append(key)
    ratings.append(example_input[key])

## Append data to existing database
query = f"""SELECT * FROM RATINGS
            WHERE "movieId"=1721;"""
pd.read_sql(query, db)
