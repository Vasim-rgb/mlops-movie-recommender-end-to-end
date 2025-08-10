import joblib
import numpy as np
import pandas as pd
from pathlib import Path


import joblib
from pathlib import Path

class PredictionPipeline:
    def __init__(self):
        # model.joblib should contain a dict with 'movies' DataFrame and 'similarity' matrix
        self.similarity = joblib.load(Path('artifacts/model_trainer/model.joblib'))
        self.movies = pd.read_csv(Path('artifacts/data_transformation/transformed_data.csv'))
    

    def recommend(self,movie:str):
        idx=self.movies[self.movies['title']==movie].index[0]
        dist=sorted(list(enumerate(self.similarity[idx])),reverse=True,key=lambda x: x[1])
        for i in dist[1:6]:
            print(self.movies.iloc[i[0]].title)

        recommended_movies = [self.movies.iloc[i[0]].title for i in dist[1:6]]
        return recommended_movies