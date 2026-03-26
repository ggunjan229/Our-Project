# Hybrid AI-based Intrusion Detection System

An ML/DL powered IDS that detects both known and unknown (zero-day) cyber attacks.

## Stack
- Python, Scikit-learn, TensorFlow, XGBoost
- Flask (backend API)
- HTML/CSS/JS (dashboard)
- SQLite (database)

## Setup
1. conda activate myenv
2. pip install -r requirements.txt
3. Place dataset CSVs in data/raw/
4. Run notebooks in order (01 → 05)
5. python backend/app.py