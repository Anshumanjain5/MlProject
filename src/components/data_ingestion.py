import os
import sys
sys.path.append(rf"{os.getcwd()}\src")
from exception import CustomError
from logger import logging
import pandas as pd
from sklearn.model_selection import train_test_split
from dataclasses import dataclass

@dataclass
class DataPath:
    train_path: str = os.path.join(os.getcwd(),"artifacts","train.csv")
    test_path: str = os.path.join(os.getcwd(),"artifacts","test.csv")
    raw_path: str = os.path.join(os.getcwd(),"artifacts","data.csv")

class DataIngestion:
    def __init__(self):
        self.ingestion_path = DataPath()

    def initiate_data_ingestion(self) -> tuple[str, str]:
        logging.info("Data ingestion initiated...")
        try:
            df = pd.read_csv(rf"{os.getcwd()}\notebook\data\students.csv")
            os.makedirs(os.path.dirname(self.ingestion_path.train_path))

            df.to_csv(self.ingestion_path.raw_path, index=False,header=False)
            logging.info("Train Test Split initiated...")

            train_set,test_set = train_test_split(df,test_size=0.2,random_state=42)
            train_set.to_csv(self.ingestion_path.train_path, index=False, header=False)
            test_set.to_csv(self.ingestion_path.test_path, index=False, header=False)

            logging.info("Data ingestion completed successfully.")
            return (
                self.ingestion_path.train_path,
                self.ingestion_path.test_path
            )
        except Exception as e:
            error = CustomError(e,sys)
            logging.info(error)
            raise error

if __name__ == "__main__":
    data = DataIngestion()
    data.initiate_data_ingestion()