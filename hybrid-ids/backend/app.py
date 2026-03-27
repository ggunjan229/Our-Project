from flask import Flask, jsonify, render_template, send_from_directory
from flask_cors import CORS
import os
import sys
sys.path.append(os.path.dirname(__file__))

from database        import init_db
from routes.predict  import predict_bp
from routes.alerts   import alerts_bp

app = Flask(__name__)
CORS(app)

# Register blueprints
app.register_blueprint(predict_bp, url_prefix='/api')
app.register_blueprint(alerts_bp,  url_prefix='/api')


@app.route('/')
def index():
    return jsonify({
        "service"   : "Hybrid AI Intrusion Detection System",
        "version"   : "1.0.0",
        "status"    : "running",
        "endpoints" : [
            "POST /api/predict",
            "POST /api/predict/batch",
            "GET  /api/alerts",
            "GET  /api/stats",
            "GET  /api/health"
        ]
    })


@app.route('/dashboard')
def dashboard():
    return send_from_directory('../frontend/templates', 'index.html')


@app.route('/static/<path:filename>')
def static_files(filename):
    return send_from_directory('../frontend/static', filename)


if __name__ == '__main__':
    print("=" * 50)
    print("  Hybrid IDS — Backend API")
    print("=" * 50)
    init_db()
    print("Starting Flask server on http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)