# Third-Party Library
from flask import Flask, jsonify
from werkzeug import exceptions

# Custom Library
from avionics_dash_server.common import exceptions as exs


def api_errors(app: Flask) -> None:
    @app.errorhandler(exceptions.BadRequest)
    def bad_request_error(e):
        return jsonify({"error": "Bad Request"}), 400

    @app.errorhandler(exceptions.Unauthorized)
    def unauthorized_error(e):
        return jsonify({"error": "Unauthorized"}), 401

    @app.errorhandler(exs.ValidationError)
    def validation_error(e):
        return jsonify({"error": "Validation Failed! Bad Request"}), 400

    @app.errorhandler(exceptions.Forbidden)
    def forbidden_error(e):
        return jsonify({"error": "Forbidden"}), 403

    @app.errorhandler(exs.AuthenticationError)
    def authentication_error(e):
        return jsonify({"error": "Authentication Failed!"}), 401
