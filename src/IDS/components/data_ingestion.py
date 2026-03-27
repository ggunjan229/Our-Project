import os
import sys
from src.IDS.exception import CustomException
from src.IDS.logger import logging
import pandas as pd
from src.IDS.utils import read_sql_data
from dataclasses import dataclass


@dataclass
class DataIngestionConfig:
    monday_data_path: str = os.path.join('artifacts', 'monday.csv')
    tue_fri_data_path: str = os.path.join('artifacts', 'tue_fri.csv')


class DataIngestion:
    def __init__(self):
        self.ingestion_config = DataIngestionConfig()

    def initiate_data_ingestion(self):
        try:
            # Read two separate datasets from MySQL
            monday_df, tue_fri_df = read_sql_data()

            logging.info("Reading completed from MySQL database")

            os.makedirs('artifacts', exist_ok=True)

            # Save Monday data separately
            monday_df.to_csv(
                self.ingestion_config.monday_data_path,
                index=False,
                header=True
            )

            # Save Tue-Fri data separately
            tue_fri_df.to_csv(
                self.ingestion_config.tue_fri_data_path,
                index=False,
                header=True
            )

            logging.info("Data ingestion completed successfully")

            return (
                self.ingestion_config.monday_data_path,
                self.ingestion_config.tue_fri_data_path
            )

        except Exception as e:
            raise CustomException(e, sys)