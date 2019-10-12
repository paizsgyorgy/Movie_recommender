"""This is a recommender engine that runs NMF (non-negative matrix
factorization) on the MovieLens dataset to return a recommendation
for given user input"""

import pandas as pd
import numpy as np
import pickle
from sqlalchemy import create_engine
from sklearn.decomposition import NMF

example_input = {   "Titanic (1997)": 5,
                    "Gladiator (2000)": 5,
                    "Shawshank Redemption, The (1994)": 5,
                    "Pulp Fiction (1994)": 5,
                    "Fight Club (1999)": 5
                }

###############################################################################
def recommend_movies_nmf(user_dict):
    """"Takes user input in form of a dictionary and returns a recommendations
        based on the previously trained NMF model"""

    ## Define main connection variables (currently connects to local postgres db)
    host = 'localhost'
    database = 'movies'
    con = f'postgres://{host}/{database}'

    ## Create engine with SQL Alchemy's create engine function
    engine = create_engine(con, encoding='latin1', echo=False)

    ##############################################################################

    ## Create dataframe with movie information and user rating from user input
    list_of_dfs = []
    for title in user_dict.keys():
        sql_statement = f"select * from films where title='{title}';"
        movies = pd.read_sql(sql_statement, engine)
        movies['user_rating'] = user_dict[title]
        list_of_dfs.append(movies)

    user_ratings = pd.concat(list_of_dfs)

    ## Create a new array/vector that contains the 5 ratings and 0s in all other fields
    ## The 5 ratings have to be in the place where the movie ID is

    ## Read in ratings data with pandas (pandas allows us to use the sql engine)
    statement = 'SELECT * FROM ratings'
    ratings = pd.read_sql(statement, engine)

    ## Transpose data with pivottable, fill NAs with 0s to create a dense matrix

    R = pd.pivot_table(ratings, values='rating', index='userId', columns='movieId')
    R = R.fillna(0)


    ## Impute ratings into a vector populated with 0s
    R_user = np.zeros(R.shape[1])
    for index, rating in zip(user_ratings['index'], user_ratings['user_rating']):
        R_user[index] = rating

    R_user = R_user.reshape(-1,1).T

    ## Add the user input to the original R that was used to train the model

    ## Load model from pickle file
    filename= "/Users/paizsgyorgy/Coding/spiced-academy/Week7/Movie recommender/flask_app/nmf_model.sav"
    file = open(filename, "rb")
    m = pickle.load(file)

    ## Calculate model Q and P
    Q = m.components_
    P_user = m.transform(R_user)

    ## Create prediction as a dot product of the user submatrix and movie submatrix

    user_pred = np.dot(P_user, Q)

    recommendations = []
    for i in user_pred.argsort()[:, ::-1][0]:
        if i not in user_ratings['index'].values:
            recommendations.append(i)
            if len(recommendations) == 5:
                break

    ## Translate these into movies from the MovieLens database
    statement = f"""SELECT *
                    FROM films
                        WHERE index IN ({recommendations[0]},
                                        {recommendations[1]},
                                        {recommendations[2]},
                                        {recommendations[3]},
                                        {recommendations[4]}
                                        );"""

    recommended_movies = pd.read_sql(statement, engine)

    return recommended_movies['title']

##############################################################################
