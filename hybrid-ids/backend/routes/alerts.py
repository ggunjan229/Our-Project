from flask import Blueprint, jsonify, request
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "../"))

from database import get_recent_alerts, get_stats

alerts_bp = Blueprint('alerts', __name__)


@alerts_bp.route('/alerts', methods=['GET'])
def get_alerts():
    limit = request.args.get('limit', 50, type=int)
    alerts = get_recent_alerts(limit=limit)
    return jsonify({
        "status" : "success",
        "count"  : len(alerts),
        "alerts" : alerts
    }), 200


@alerts_bp.route('/stats', methods=['GET'])
def get_statistics():
    stats = get_stats()
    return jsonify({
        "status" : "success",
        "stats"  : stats
    }), 200


@alerts_bp.route('/health', methods=['GET'])
def health_check():
    return jsonify({
        "status"  : "healthy",
        "service" : "Hybrid IDS API",
        "version" : "1.0.0"
    }), 200