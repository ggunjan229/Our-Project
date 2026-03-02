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
    logging.info("Reading data from mysql database")
    try:
        mydb = pymysql.connect(
            host=host,
            user=user,
            password=password,
            database=db
        )
        logging.info("Connection established",mydb)
        df1 = pd.read_sql_query("Select* from tuetofri_ids", mydb)
        df2 = pd.read_sql_query("Select* from mon_ids", mydb)
        print(df1.head())
        print(df2.head())


        return df1, df2
    
    except Exception as ex:
        raise CustomException(ex)   