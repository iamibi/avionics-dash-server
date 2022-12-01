# Third-Party Library
from flask import Blueprint, jsonify, request

# Custom Library
from avionics_dash_server.api.auth.auth import (
    bearer_token_auth,
    generate_token_for_email,
)
from avionics_dash_server.common.constants import App, HttpMethod
from avionics_dash_server.helpers.platform_helper import platform_helper

# Create a blueprint for the project
avionics_dash_bp = Blueprint(name=App.BLUEPRINT, import_name=__name__, url_prefix="/api/v1")


@avionics_dash_bp.route("/", methods=[HttpMethod.GET])
def index():
    return jsonify({"message": "Hello from Avionics Dash API!"})


@avionics_dash_bp.route("/status", methods=[HttpMethod.GET])
def status():
    return jsonify({"message": "Avionics Dash API running...OK"})


@avionics_dash_bp.route("/auth/login", methods=[HttpMethod.POST])
def login_user():
    request_json = request.json

    if "email" not in request_json:
        raise "No email passed"
    token = generate_token_for_email(request_json["email"])

    return jsonify({"token": token}), 201


@avionics_dash_bp.route("/auth/verify", methods=[HttpMethod.GET])
@bearer_token_auth.login_required
def verify():
    return jsonify({"message": "The token is valid!"}), 200


@avionics_dash_bp.route("/auth/register", methods=[HttpMethod.POST])
def register():
    request_json = request.json
    platform_helper.register_user(user_data=request_json["data"])
    return jsonify({}), 201
