import os
from src.datascience import logger
from src.datascience.entity.config_entity import DataTransformationConfig
import pandas as pd
from src.datascience.utils.common import convert, convertz, convertf

class DataTransformation:
    def __init__(self, config: DataTransformationConfig):
        self.config = config

    
    ## Note: You can add different data transformation techniques such as Scaler, PCA and all
    
    def train_test_splitting(self):
        movies=pd.read_csv(self.config.data_path)
        movies['overview']=movies.overview.to_list()[0]
        movies['genres']=movies['genres'].apply(convert)
        movies['keywords']=movies['keywords'].apply(convert)
        movies['genres'].apply(lambda x: [i.replace(' ','') for i in x]).apply(lambda x:[i.lower() for i in x])
        movies['keywords'].apply(lambda x: [i.replace(' ','') for i in x]).apply(lambda x:[i.lower() for i in x])
        movies['cast']=movies['cast'].apply(convertz)
        movies['cast']=movies['cast'].apply(lambda x: x[0:3])
        movies['crew']=movies['crew'].apply(convertf)
        movies['crew']=movies['crew'].apply(lambda x: [ i.replace(' ','') for i in x])
        movies['crew']=movies['crew'].apply(lambda x: [ i.lower() for i in x])
        movies['tag']=movies['genres']+movies['keywords']+movies['cast']+movies['crew']
        movies['overview']=movies['overview'].apply(lambda x:x.split())
        movies['tag']=movies['tag']+movies['overview']
        movies['tag']=movies['tag'].apply(lambda x:' '.join(x))
        movies.drop(columns=['cast','crew','overview','keywords','genres'],inplace=True)
        movies['title']=movies['title'].apply(lambda x:x.split()).apply(lambda x:[i.lower() for i in x]).apply(lambda x:' '.join(x))
        movies['tag']=movies['tag'].apply(lambda x : x.split())
        movies['tag']=movies['tag'].apply(lambda x : [i.lower() for i in x])
        movies['tag']=movies['tag'].apply(lambda x : ' '.join(x))
        movies= movies[['movie_id', 'title', 'tag']]
        movies.to_csv(self.config.transformed_data_path, index=False)



        logger.info("transofmation completed and data saved at: {}".format(self.config.transformed_data_path))
        