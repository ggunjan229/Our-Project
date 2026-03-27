import numpy as np
import pandas as pd
import joblib
import os

model_path = os.path.join(os.path.dirname(__file__), "../../models/saved/")

scaler           = joblib.load(model_path + "scaler.pkl")
selected_features = joblib.load(model_path + "selected_features.pkl")

def preprocess_input(data: dict) -> np.ndarray:
    """
    Takes raw input dict, aligns to selected features,
    scales and returns numpy array ready for prediction.
    """
    df = pd.DataFrame([data])

    # Add missing columns with 0
    for col in selected_features:
        if col not in df.columns:
            df[col] = 0.0

    df = df[selected_features]
    df = df.fillna(0.0)
    df = df.replace([np.inf, -np.inf], 0.0)

    scaled = scaler.transform(df)
    return scaled


def preprocess_batch(records: list) -> np.ndarray:
    """
    Takes a list of raw input dicts and returns
    a batch numpy array ready for prediction.
    """
    df = pd.DataFrame(records)

    for col in selected_features:
        if col not in df.columns:
            df[col] = 0.0

    df = df[selected_features]
    df = df.fillna(0.0)
    df = df.replace([np.inf, -np.inf], 0.0)

    scaled = scaler.transform(df)
    return scaled