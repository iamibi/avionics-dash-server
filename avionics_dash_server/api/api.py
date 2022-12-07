# Third-Party Library
from flask import Blueprint, jsonify, request

# Custom Library
from avionics_dash_server.common import exceptions as exs
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

    if "email" not in request_json or "password" not in request_json:
        return jsonify({"error": "Required credentials were not found!"}), 400

    if platform_helper.authenticate_user(email=request_json["email"], password=request_json["password"]) is True:
        token = generate_token_for_email(request_json["email"])
        return jsonify({"token": token}), 201
    raise exs.AuthenticationError


@avionics_dash_bp.route("/auth/register", methods=[HttpMethod.POST])
def register():
    request_json = request.json
    user = platform_helper.register_user(user_data=request_json["data"])
    return jsonify({"data": user}), 201


@avionics_dash_bp.route("/users/<string:user_id>", methods=[HttpMethod.GET])
@bearer_token_auth.login_required
def get_user(user_id: str):
    if user_id in {None, ""}:
        return jsonify({"error": "User ID not passed"}), 400

    user = platform_helper.get_user(user_id=user_id)
    return jsonify({"data": user}), 200


@avionics_dash_bp.route("/users/<string:user_id>/courses", methods=[HttpMethod.GET])
@bearer_token_auth.login_required
def get_courses_for_user_id(user_id: str):
    if user_id in {None, ""}:
        return jsonify({"error": "User ID not passed"}), 400

    courses = platform_helper.get_courses_for_user_id(user_id=user_id)
    return jsonify({"data": courses}), 200


@avionics_dash_bp.route("/courses/<string:course_id>/add/<string:user_id>", methods=[HttpMethod.PUT])
def add_course_to_user_id(course_id: str, user_id: str):
    if course_id in {None, ""} or user_id in {None, ""}:
        return jsonify({"error": "Invalid UserId or CourseId passed!"}), 400

    platform_helper.update_user_with_course(user_id=user_id, course_id=course_id)
    return jsonify({}), 204


@avionics_dash_bp.route("/courses/<string:course_id>", methods=[HttpMethod.GET])
@bearer_token_auth.login_required
def get_course(course_id: str):
    if course_id in {None, ""}:
        return jsonify({"error": "Course ID not passed!"}), 400

    course = platform_helper.get_course(course_id=course_id)
    return jsonify({"data": course}), 200


@avionics_dash_bp.route("/modules/<string:module_id>", methods=[HttpMethod.GET])
@bearer_token_auth.login_required
def get_module(module_id: str):
    if module_id in {None, ""}:
        return jsonify({"error": "Module ID not passed!"}), 400

    module = platform_helper.get_module(module_id=module_id)
    return jsonify({"data": module}), 200


@avionics_dash_bp.route("/assignments/<string:assignment_id>", methods=[HttpMethod.GET])
def get_assignment(assignment_id: str):
    if assignment_id in {None, ""}:
        return jsonify({"error": "Module ID not passed!"}), 400

    assignment = platform_helper.get_assignment(assignment_id=assignment_id)
    return jsonify({"data": assignment}), 200
