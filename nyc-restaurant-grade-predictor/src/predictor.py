import json
import joblib
import numpy as np
import pandas as pd
import os

# -------------------------------------------------
# Load model + metadata once (cached)
# -------------------------------------------------

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "models", "restaurant_grade_model.pkl")
META_PATH = os.path.join(BASE_DIR, "models", "model_metadata.json")

try:
    model = joblib.load(MODEL_PATH)
except Exception as e:
    raise RuntimeError(f"Could not load model: {e}")

try:
    with open(META_PATH, "r") as f:
        metadata = json.load(f)
except Exception as e:
    raise RuntimeError(f"Could not load metadata JSON: {e}")

FEATURE_COLUMNS = metadata["feature_columns"]
ENCODERS = metadata.get("encoders", {})


# -------------------------------------------------
# Convert restaurant info into model-ready features
# -------------------------------------------------

def build_feature_vector(restaurant_data: dict):
    """
    Transform restaurant data dict into model-ready feature array.

    Expected input:
    {
        "borough": "Queens",
        "zipcode": "11372",
        "cuisine_description": "Latin American",
        "critical_flag_bin": 0,
        "score": 12
    }

    Returns numpy array with encoded features.
    """
    # Encode borough
    borough_val = str(restaurant_data.get("borough", "")).strip().title()
    borough_encoder = ENCODERS.get("borough", {})
    borough_encoded = borough_encoder.get(borough_val, 0)

    # Encode zipcode as numeric
    zipcode_val = restaurant_data.get("zipcode", 0)
    try:
        zipcode_numeric = float(str(zipcode_val).replace(",", ""))
    except (ValueError, TypeError):
        zipcode_numeric = 0

    # Encode cuisine
    cuisine_val = str(restaurant_data.get("cuisine_description", "")).strip().title()
    cuisine_encoder = ENCODERS.get("cuisine_description", {})
    cuisine_encoded = cuisine_encoder.get(cuisine_val, 0)

    # Critical flag (already binary)
    critical_flag = int(restaurant_data.get("critical_flag_bin", 0))

    # Score (numeric)
    score_val = restaurant_data.get("score", 0)
    try:
        score = float(score_val) if score_val is not None else 0
    except (ValueError, TypeError):
        score = 0

    # Return as 2D array for sklearn
    features = np.array([[borough_encoded, zipcode_numeric, cuisine_encoded, critical_flag, score]])
    return features


# -------------------------------------------------
# Prediction function
# -------------------------------------------------

def predict_restaurant_grade(restaurant_data: dict):
    """
    Input: dict with restaurant info
    Output: dict with prediction + probabilities
    """
    X = build_feature_vector(restaurant_data)

    pred = model.predict(X)[0]
    probs = model.predict_proba(X)[0]

    prob_dict = {label: float(p) for label, p in zip(model.classes_, probs)}

    return {
        "grade": pred,
        "probabilities": prob_dict,
        "raw_output": probs.tolist()
    }
