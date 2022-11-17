# Third-Party Library
from flask import Flask

# Custom Library
from avionics_dash_server.api.api import avionics_dash_bp


def create_app() -> Flask:
    """Creates a Flask app instance"""

    app = Flask(__name__)

    # Register the application blueprint with the APIs
    app.register_blueprint(avionics_dash_bp)

    return app
