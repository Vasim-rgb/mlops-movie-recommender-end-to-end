import pandas as pd
import os
from src.datascience import logger
import joblib
from sklearn.metrics.pairwise import cosine_similarity
from src.datascience.entity.config_entity import ModelTrainerConfig
from sklearn.feature_extraction.text import CountVectorizer
class ModelTrainer:
    def __init__(self, config: ModelTrainerConfig):
        self.config = config

    def train(self):
        logger.info("Training the model")
        cv = CountVectorizer(max_features=5000,stop_words='english')
        movies=pd.read_csv(self.config.transformed_data_path)
        vector = cv.fit_transform(movies['tag']).toarray()
        similarity = cosine_similarity(vector)
        joblib.dump(similarity, os.path.join(self.config.root_dir, self.config.model_name))
        logger.info(f"Model trained and saved at {self.config.root_dir}/{self.config.model_name}")
    


    