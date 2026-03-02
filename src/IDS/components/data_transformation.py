import os
import sys
import pandas as pd
import numpy as np
from dataclasses import dataclass
from sklearn.preprocessing import StandardScaler
from src.IDS.exception import CustomException
from src.IDS.logger import logging
import pickle


@dataclass
class DataTransformationConfig:
    scaler_path: str = os.path.join("artifacts", "scaler.pkl")


class DataTransformation:
    def __init__(self):
        self.config = DataTransformationConfig()

    def transform_monday(self, monday_path):
        try:
            df = pd.read_csv(monday_path)

            df = df.dropna()

            if "Attack" in df.columns:
                df = df.drop("Attack", axis=1)

            scaler = StandardScaler()
            X_scaled = scaler.fit_transform(df)

            with open(self.config.scaler_path, "wb") as f:
                pickle.dump(scaler, f)

            return X_scaled

        except Exception as e:
            raise CustomException(e, sys)

    def transform_tue_fri(self, tue_fri_path):
        try:
            df = pd.read_csv(tue_fri_path)
            df = df.dropna()

            y = df["Attack"].astype(int)
            X = df.drop("Attack", axis=1)

            scaler = StandardScaler()

            with open(self.config.scaler_path, "rb") as f:
                scaler = pickle.load(f)

            X_scaled = scaler.transform(X)

            return X_scaled, y

        except Exception as e:
            raise CustomException(e, sys)