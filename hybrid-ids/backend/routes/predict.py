from flask import Blueprint, request, jsonify
import json
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "../"))

from utils.preprocess import preprocess_input, preprocess_batch
from utils.predictor  import predict_single, predict_batch
from database         import save_alert

predict_bp = Blueprint('predict', __name__)


@predict_bp.route('/predict', methods=['POST'])
def predict():
    """Single prediction endpoint"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No input data provided"}), 400

        X = preprocess_input(data)
        result = predict_single(X)
        save_alert(result, raw_input=json.dumps(data))

        return jsonify({
            "status" : "success",
            "result" : result
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@predict_bp.route('/predict/batch', methods=['POST'])
def predict_batch_endpoint():
    """Batch prediction endpoint"""
    try:
        data = request.get_json()
        if not data or "records" not in data:
            return jsonify({"error": "Provide a 'records' list"}), 400

        records = data["records"]
        X = preprocess_batch(records)
        results = predict_batch(X)

        for r in results:
            save_alert(r)

        attack_count = sum(1 for r in results if r["is_attack"])

        return jsonify({
            "status"        : "success",
            "total"         : len(results),
            "attacks_found" : attack_count,
            "results"       : results
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500