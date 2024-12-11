import os
import sys
sys.path.append(rf"{os.getcwd()}\src")
import numpy as np
import pandas as pd
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from dataclasses import dataclass
from exception import CustomError
from utility import save_object
from components.model_trainer import ModelTrainer
from logger import logging
from components.data_ingestion import DataIngestion

@dataclass
class DataTransformationConfig:
    preprocessor_obj_path = os.path.join("artifacts", "preprocessor.pkl")

class DataTransformation:
    def __init__(self):
        logging.info("Initializing DataTransformation...")
        self.preprocessor_path = DataTransformationConfig().preprocessor_obj_path
        ingestion = DataIngestion().initiate_data_ingestion()
        self.train = pd.read_csv(ingestion[0])
        self.test = pd.read_csv(ingestion[1])

    def get_data_transformer(self):
        """Creates a preprocessing pipeline for numerical and categorical data."""
        try:
            logging.info("Initializing DataTransformer preprocess...")

            num_transformer = Pipeline(steps=[
                ('imputer', SimpleImputer(strategy='mean')),
                ('scaler', StandardScaler(with_mean=False))
            ])

            cat_transformer = Pipeline(steps=[
                ('imputer', SimpleImputer(strategy='most_frequent')),
                ('onehot', OneHotEncoder(handle_unknown='ignore'))
            ])

            num_columns, cat_columns = (["reading_score","writing_score"],["gender","race_ethnicity","parental_level_of_education","lunch","test_preparation_course"])

            preprocessor = ColumnTransformer(
                transformers=[
                    ('num', num_transformer, num_columns),
                    ('cat', cat_transformer, cat_columns)
                ])

            logging.info("DataTransformer preprocess initialization completed")

            return preprocessor
        except Exception as e:
            raise CustomError(e, sys)

    def initialize_data_transformer(self):
        """Applies preprocessing and saves the preprocessor object."""
        try:
            target_column = "math_score"
            preprocessor = self.get_data_transformer()
            
            # Fit the preprocessor on the training data
            train_set = self.train.drop(target_column, axis=1)
            preprocessor.fit(train_set)  # Fitting on training data
            
            # Save the fitted preprocessor
            save_object(preprocessor, self.preprocessor_path)

            # Now transform both training and test sets
            train_transformed = preprocessor.transform(train_set)
            test_set = self.test.drop(target_column, axis=1)
            test_transformed = preprocessor.transform(test_set)

            target_train_set = self.train[target_column]
            target_test_set = self.test[target_column]

            train_arr = np.c_[train_transformed, target_train_set]
            test_arr = np.c_[test_transformed, target_test_set]

            return train_arr, test_arr, preprocessor
        except Exception as e:
            raise CustomError(e, sys)


if __name__ == "__main__":
    data_transformer = DataTransformation()
    train_arr, test_arr, preprocessor = data_transformer.initialize_data_transformer()
    print(f"Train Array: {train_arr.shape}, Test Array: {test_arr.shape}")
    print(train_arr)
    model_trainer = ModelTrainer()
    print(model_trainer.initiate_model_trainer(train_arr, test_arr))
