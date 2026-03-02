import os
import sys
from src.IDS.exception import CustomException
from src.IDS.logger import logging
import pandas as pd
import pymysql
import pickle
from dotenv import load_dotenv

load_dotenv()
host = os.getenv("host")
user = os.getenv("user")
password = os.getenv("password")
db = os.getenv("db")


def read_sql_data():
    logging.info("Reading data from MySQL database")
    try:
        mydb = pymysql.connect(
            host=host,
            user=user,
            password=password,
            database=db
        )
        logging.info("Connection established")

        tue_fri_df = pd.read_sql_query("SELECT * FROM tuetofri_ids", mydb)
        monday_df = pd.read_sql_query("SELECT * FROM mon_ids", mydb)

        logging.info(f"Tue-Fri Shape: {tue_fri_df.shape}")
        logging.info(f"Monday Shape: {monday_df.shape}")

        return monday_df, tue_fri_df

    except Exception as ex:
        raise CustomException(ex, sys)