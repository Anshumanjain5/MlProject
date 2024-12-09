import sys
import os
sys.path.append(rf"{os.getcwd()}\src")
from logger import logging
from exception import CustomError
import pickle

def save_object(obj,path):
    try:
        logging.info(f"Saving object at {path}")
        with open(path, 'wb') as f:
            pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)
            logging.info(f"Object saved successfully at {path}")
    except Exception as e:
        logging.error(f"Error occurred while saving object: {str(e)}")
        raise CustomError(e,sys)