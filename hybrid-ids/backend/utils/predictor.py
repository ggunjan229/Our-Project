import numpy as np
import joblib
import json
import os
from tensorflow import keras

model_path = os.path.join(os.path.dirname(__file__), "../../models/saved/")

# Load all models once at startup
print("Loading models...")
rf_binary    = joblib.load(model_path + "rf_binary.pkl")
xgb_binary   = joblib.load(model_path + "xgb_binary.pkl")
rf_multi     = joblib.load(model_path + "rf_multi.pkl")
meta_learner = joblib.load(model_path + "meta_learner.pkl")
autoencoder  = keras.models.load_model(model_path + "autoencoder_final.keras")
threshold    = joblib.load(model_path + "autoencoder_threshold.pkl")
le           = joblib.load(model_path + "label_encoder.pkl")

with open(model_path + "system_config.json") as f:
    config = json.load(f)

print("✅ All models loaded and ready")


def predict_single(X: np.ndarray) -> dict:
    """
    Run hybrid prediction on a single sample.
    Returns full prediction breakdown.
    """
    # --- Individual model predictions ---
    rf_prob  = float(rf_binary.predict_proba(X)[:, 1][0])
    xgb_prob = float(xgb_binary.predict_proba(X)[:, 1][0])

    recon    = autoencoder.predict(X, verbose=0)
    mse      = float(np.mean(np.power(X - recon, 2)))
    ae_prob  = float(min(mse / (threshold * 3), 1.0))

    # --- Meta-learner fusion ---
    meta_input  = np.array([[rf_prob, xgb_prob, ae_prob]])
    hybrid_prob = float(meta_learner.predict_proba(meta_input)[:, 1][0])
    is_attack   = int(hybrid_prob >= 0.5)

    # --- Attack type (if attack detected) ---
    attack_type = "BENIGN"
    if is_attack:
        multi_pred  = rf_multi.predict(X)[0]
        attack_type = str(le.inverse_transform([multi_pred])[0])

    # --- Severity scoring ---
    severity = "LOW"
    if hybrid_prob >= 0.85:
        severity = "CRITICAL"
    elif hybrid_prob >= 0.70:
        severity = "HIGH"
    elif hybrid_prob >= 0.50:
        severity = "MEDIUM"

    return {
        "is_attack"        : bool(is_attack),
        "attack_type"      : attack_type,
        "severity"         : severity,
        "hybrid_confidence": round(hybrid_prob * 100, 2),
        "model_breakdown"  : {
            "random_forest" : round(rf_prob * 100, 2),
            "xgboost"       : round(xgb_prob * 100, 2),
            "autoencoder"   : round(ae_prob * 100, 2),
        },
        "reconstruction_error": round(mse, 6),
        "threshold"           : round(float(threshold), 6),
    }


def predict_batch(X: np.ndarray) -> list:
    """
    Run hybrid prediction on a batch of samples.
    Returns list of prediction dicts.
    """
    results = []
    for i in range(len(X)):
        result = predict_single(X[i:i+1])
        results.append(result)
    return results

# Add this import at the top of predictor.py
import shap as shap_lib

# Load SHAP explainer
try:
    shap_explainer = joblib.load(model_path + "shap_explainer.pkl")
    print("✅ SHAP explainer loaded")
except:
    shap_explainer = None
    print("⚠️  SHAP explainer not found")


def explain_prediction(X: np.ndarray, top_n: int = 10) -> list:
    """
    Returns top N features that influenced this prediction
    with their SHAP values and direction (pushing toward attack or benign)
    """
    if shap_explainer is None:
        return []

    selected_features = joblib.load(model_path + "selected_features.pkl")

    import pandas as pd
    X_df = pd.DataFrame(X, columns=selected_features)

    shap_vals = shap_explainer.shap_values(X_df)
    sv = shap_vals[1][0] if isinstance(shap_vals, list) else shap_vals[0]

    explanation = []
    for feat, val in zip(selected_features, sv):
        explanation.append({
            "feature"   : feat,
            "shap_value": round(float(val), 6),
            "direction" : "→ ATTACK" if val > 0 else "→ BENIGN",
            "impact"    : "HIGH"   if abs(val) > 0.1
                          else "MEDIUM" if abs(val) > 0.02
                          else "LOW"
        })

    explanation.sort(key=lambda x: abs(x["shap_value"]), reverse=True)
    return explanation[:top_n]