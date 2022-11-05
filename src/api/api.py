# Third-Party Library
from flask import Blueprint, jsonify

# Custom Library
from src.common.constants import App, HttpMethod

# Create a blueprint for the project
avionics_dash_bp = Blueprint(name=App.BLUEPRINT, import_name=__name__)


@avionics_dash_bp.route("/", methods=[HttpMethod.GET])
def index():
    return jsonify({"message": "Hello from Avionics Dash API!"})


@avionics_dash_bp.route("/v1/status", methods=[HttpMethod.GET])
def status():
    return jsonify({"message": "Avionics Dash API running...OK"})
