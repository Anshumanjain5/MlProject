import os
import sys
sys.path.append(rf"{os.getcwd()}\src")
from dataclasses import dataclass
from catboost import CatBoostRegressor
from sklearn.ensemble import (
    AdaBoostRegressor,
    GradientBoostingRegressor,
    RandomForestRegressor,
)
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
from sklearn.tree import DecisionTreeRegressor
from sklearn.neighbors import KNeighborsRegressor
from xgboost import XGBRegressor
from exception import CustomError
from logger import logging
from utility import save_object, evaluate_models

@dataclass
class ModelTrainConfig:
    trained_model_path = os.path.join("artifacts","model.pkl")

class ModelTrainer:
    def __init__(self):
        self.model_config = ModelTrainConfig()
    
    def initiate_model_trainer(self, train_array, test_array):
        logging.info("Model training initiated...")
        try:
            X_train, y_train, X_test, y_test = (
                train_array[:, :-1],
                train_array[:, -1],
                test_array[:, :-1],
                test_array[:, -1],
            )
            models = {
                "Linear Regression": LinearRegression(),
                "Decision Tree": DecisionTreeRegressor(),
                "Random Forest": RandomForestRegressor(),
                "AdaBoost": AdaBoostRegressor(),
                "Gradient Boosting": GradientBoostingRegressor(),
                "K Neighbors": KNeighborsRegressor(),
                "XGBoost": XGBRegressor(),
                "CatBoost": CatBoostRegressor(verbose=False),
            }

            model_report: dict = evaluate_models(
                x_train=X_train, y_train=y_train, x_test=X_test, y_test=y_test, models=models
            )

            logging.debug(f"Model Report: {model_report}")
            best_model_score = max(sorted(model_report.values()))
            best_model_name = list(model_report.keys())[list(model_report.values()).index(best_model_score)]
            best_model = models[best_model_name]

            if best_model_score < 0.6:
                logging.error("Model performance is not satisfactory. Consider tuning hyperparameters or selecting different models.")
                raise CustomError("Model performance is not satisfactory. Consider tuning hyperparameters or selecting different models.", sys)

            logging.info("Model training completed successfully.")
            logging.info(f"Best model: {best_model_name}\tScore: {best_model_score}")

            save_object(best_model, self.model_config.trained_model_path)
            prediction = best_model.predict(X_test)
            r2_square = r2_score(y_test, prediction)

            return r2_square
        except Exception as e:
            error = CustomError(e, sys)
            logging.exception(error)
            raise error

        
