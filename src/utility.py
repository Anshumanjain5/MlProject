import sys
import os
sys.path.append(rf"{os.getcwd()}\src")
from logger import logging
from exception import CustomError
import pickle
from sklearn.metrics import r2_score

def save_object(obj,path):
    try:
        logging.info(f"Saving object at {path}")
        with open(path, 'wb') as f:
            pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)
            logging.info(f"Object saved successfully at {path}")
    except Exception as e:
        logging.error(f"Error occurred while saving object: {str(e)}")
        raise CustomError(e,sys)
    
def evaluate_models(x_train,y_train,x_test,y_test,models):
    try:
        results = {}
        for i in range(len(list(models))):
            model = list(models.values())[i]
            model.fit(x_train, y_train)
            y_train_pred = model.predict(x_train)
            y_test_pred = model.predict(x_test)
            train_model_score = r2_score(y_train,y_train_pred)
            test_model_score = r2_score(y_test,y_test_pred)
            results[list(models.keys())[i]] = test_model_score
    except Exception as e:
        logging.error(f"Error occurred while evaluating models: {str(e)}")
        raise CustomError(e,sys)
    return results
