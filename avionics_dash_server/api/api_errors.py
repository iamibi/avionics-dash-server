# Third-Party Library
from flask import Flask, jsonify
from werkzeug import exceptions

# Custom Library
from avionics_dash_server.common import exceptions as exs


def api_errors(app: Flask) -> None:
    @app.errorhandler(exceptions.BadRequest)
    def bad_request_error(e):
        return jsonify({"error": "Bad Request", "error_message": str(e)}), 400

    @app.errorhandler(exceptions.Unauthorized)
    def unauthorized_error(e):
        return jsonify({"error": "Unauthorized", "error_message": str(e)}), 401

    @app.errorhandler(exs.ValidationError)
    def validation_error(e):
        return jsonify({"error": "Validation Failed! Bad Request", "error_message": str(e)}), 400

    @app.errorhandler(exceptions.Forbidden)
    def forbidden_error(e):
        return jsonify({"error": "Forbidden", "error_message": str(e)}), 403

    @app.errorhandler(exs.AuthenticationError)
    def authentication_error(e):
        return jsonify({"error": "Authentication Failed!", "error_message": str(e)}), 401
