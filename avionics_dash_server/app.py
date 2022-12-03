# Third-Party Library
from flask import Flask

# Custom Library
from avionics_dash_server.api.api import avionics_dash_bp
from avionics_dash_server.api.api_errors import api_errors


def create_app() -> Flask:
    """Creates a Flask app instance"""

    flask_app = Flask(__name__)

    # Register the application blueprint with the APIs
    flask_app.register_blueprint(avionics_dash_bp)

    # Register API error handler
    api_errors(flask_app)

    return flask_app


# Return app
app = create_app()
