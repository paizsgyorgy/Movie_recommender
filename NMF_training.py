import pandas as pd
import numpy as np
from sqlalchemy import create_engine
from sklearn.decomposition import NMF
import pickle

##############################################################################

# Define function to connect to the SQL server where we store our movie ratings data

def load_data():

    ## Define main connection variables (currently connects to local postgres db)
    host = 'localhost'
    database = 'movies'
    con = f'postgres://{host}/{database}'

    ## Create engine with SQL Alchemy's create engine function
    engine = create_engine(con, encoding='latin1', echo=False)

    ## Read in ratings data with pandas (pandas allows us to use the sql engine)
    statement = 'SELECT * FROM ratings'
    ratings = pd.read_sql(statement, engine)

    return ratings

##############################################################################

## Train NMF model from a given input matrix

def train_nmf(ratings, comp):

    # 2. Transpose data with pivottable, fill NAs with 0s to create a dense matrix

    R = pd.pivot_table(ratings, values='rating', index='userId', columns='movieId')
    R = R.fillna(0)

    ##########################################################################

    # 3. Run NMF model on given ratings data

    ## Instantiate the model
    m = NMF(n_components = comp)

    ## Fit the model using the dense matrix R (movie ratings)
    m.fit(R)

    return m

##############################################################################

## Run the functions to load data and train model with 100 hidden components
ratings = load_data()
model = train_nmf(ratings, 100)

## Save the model as a pickle file for later use by recommender
filename = 'nmf_model.sav'
pickle.dump(model, open(filename, 'wb'))
