import os
import sys
sys.path.append(rf"{os.getcwd()}\src")
import pandas as pd
from exception import CustomError
from logger import logging 
from utility import load_object

class PredictPipeline:
    def __init__(self):
        pass
    def predict(self,features):
        try:
            model = load_object(os.path.join(os.getcwd(),"artifacts","model.pkl"))
            preprocessor = load_object(os.path.join(os.getcwd(),"artifacts","preprocessor.pkl")) 
            features = preprocessor.transform(features)
            print(features)
            return model.predict(features)
        except Exception as e:
            error = CustomError(e,sys)
            logging.info(error)
            raise error

class CustomData:
    def __init__(self,
                 gender:str,
                 race_ethnicity:str,
                 lunch:str,
                 parental_level_of_education:str,
                 test_preparation_course:str,
                 reading_score:int,
                 writing_score:int):
        self.gender = gender
        self.race_ethnicity = race_ethnicity
        self.lunch = lunch
        self.parental_level_of_education = parental_level_of_education
        self.test_preparation_course = test_preparation_course
        self.reading_score = reading_score
        self.writing_score = writing_score

    def get_data_as_dataframe(self):
        try:
            frame = {
                'gender': [self.gender],
                'race_ethnicity': [self.race_ethnicity],
                'parental_level_of_education': [self.parental_level_of_education],
                'lunch': [self.lunch],
                'test_preparation_course': [self.test_preparation_course],
                'reading_score': [self.reading_score],
                'writing_score': [self.writing_score]
            }
            return pd.DataFrame(frame)
        except Exception as e:
            error = CustomError(e,sys)
            logging.info(error)
            raise error