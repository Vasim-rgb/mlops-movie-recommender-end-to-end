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
    

    def recommend(self, movie: str):
        import difflib
        # Try exact match first
        matches = self.movies[self.movies['title'] == movie]
        if not matches.empty:
            idx = matches.index[0]
        else:
            # Fuzzy match: find closest movie title
            all_titles = self.movies['title'].tolist()
            close_matches = difflib.get_close_matches(movie, all_titles, n=1, cutoff=0.6)
            if close_matches:
                idx = self.movies[self.movies['title'] == close_matches[0]].index[0]
            else:
                # If no close match, just use the first movie
                idx = 0
        dist = sorted(list(enumerate(self.similarity[idx])), reverse=True, key=lambda x: x[1])
        recommended_movies = [self.movies.iloc[i[0]].title for i in dist[1:6]]
        return recommended_movies