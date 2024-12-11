import os
import sys
sys.path.append(rf"{os.getcwd()}\src")
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder, LabelEncoder, StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from exception import CustomError
import numpy as np
from utility import save_object
from logger import logging
import pandas as pd
from components.data_ingestion import DataIngestion
from dataclasses import dataclass

@dataclass
class DataTransformationConfig:
    preprocessor_obj_path = os.path.join("artifacts","preprocessor.pkl")

class DataTransformation:
    def __init__(self):
        logging.info("Initializing DataTransformation...")
        self.preprocessor_path = DataTransformationConfig().preprocessor_obj_path
        self.train = pd.read_csv(DataIngestion().initiate_data_ingestion()[0])
        self.test = pd.read_csv(DataIngestion().initiate_data_ingestion()[1])

    def differentiate_columns(self) -> tuple[list,list]:
        cat_columns = []
        num_columns = []
        # ic(cat_columns, num_columns)
        for i in enumerate(self.train.dtypes):
            if i[1] == "object":
                cat_columns.append(self.train.columns[i[0]])
            else:
                num_columns.append(self.train.columns[i[0]])
        logging.info("Columns classification process completed")
        return (num_columns, cat_columns)

    def get_data_transformer(self):
        try:
            

            logging.info("DataTransformer preprocess initialization process started...")
            num_transformer = Pipeline(steps=[
                ('imputer', SimpleImputer(strategy='mean')),
                ('scaler', StandardScaler(with_mean=False))
            ])
            cat_transformer = Pipeline(steps=[
                ('imputer', SimpleImputer(strategy='most_frequent')),
                ('onehot', OneHotEncoder(handle_unknown='ignore')),
                ('scaler',StandardScaler(with_mean=False))
            ])

            preprocessor = ColumnTransformer(
                transformers=[
                    ('num', num_transformer, self.differentiate_columns()[0]),
                    ('cat', cat_transformer, self.differentiate_columns()[1])
                ])
            
            logging.info("DataTransformer preprocess initialization process completed")
            
            return preprocessor
        except Exception as e:
            error = CustomError(e,sys)
            logging.info(error)
            raise error

    def initialize_data_transformer(self):

        try:
            train_df  = self.train
            test_df  = self.test

            preprocessor = self.get_data_transformer()

            targetcolumn = "math_score"

            train_set = train_df.drop(targetcolumn,axis=1)
            target_train_set = train_df[targetcolumn]

            test_set = test_df.drop(targetcolumn,axis=1)
            target_test_set = test_df[targetcolumn]

            train_transformed = preprocessor.fit_transform(train_df)
            test_transformed = preprocessor.transform(test_df)

            train_arr = np.c_[train_transformed,target_train_set]
            test_arr = np.c_[test_transformed,target_test_set]

            save_object(
                preprocessor,
                self.preprocessor_path
            )

            return(
                train_arr,
                test_arr,
                preprocessor
            )
    
        except Exception as e:
            error = CustomError(e,sys)
            logging.info(error)
            raise error
        
# Test the DataTransformation class

if __name__ == "__main__":
    data_transformer = DataTransformation()
    train_arr, test_arr, preprocessor = data_transformer.initialize_data_transformer()
    print(f"Train Array: {train_arr.shape}, Test Array: {test_arr.shape}")
    print(f"Preprocessor: {type(preprocessor)}")