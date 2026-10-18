"""
Intelligent Market Research Assistant
Main Flask Application Entry Point

Built with: IBM Bob + IBM Cloud + IBM Granite (granite-3-8b-instruct)
"""

import os
from flask import Flask, send_from_directory
from flask_cors import CORS
from backend.config import FLASK_SECRET_KEY
from backend.routes import api


def create_app():
    app = Flask(__name__, static_folder="frontend/static", static_url_path="/static")
    app.secret_key = FLASK_SECRET_KEY

    # Enable CORS for all routes
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    # Register API blueprint
    app.register_blueprint(api)

    # Serve frontend
    @app.route("/")
    def index():
        return send_from_directory("frontend", "index.html")

    @app.route("/<path:path>")
    def serve_static(path):
        try:
            return send_from_directory("frontend", path)
        except Exception:
            return send_from_directory("frontend", "index.html")

    return app


if __name__ == "__main__":
    app = create_app()
    port = int(os.environ.get("PORT", 5000))
    print(f"\n{'='*60}")
    print(f"  Intelligent Market Research Assistant")
    print(f"  Powered by IBM Granite (granite-3-8b-instruct)")
    print(f"  Running on http://localhost:{port}")
    print(f"{'='*60}\n")
    # use_reloader=False keeps a single stable process (required for background mode)
    app.run(debug=False, host="0.0.0.0", port=port, use_reloader=False, threaded=True)
