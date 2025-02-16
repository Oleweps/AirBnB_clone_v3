#!/usr/bin/python3
""" module to handle all User object RESTFul Api actions
"""
from api.v1.views import app_views as api_views

from flask import jsonify, request, abort

from models import storage
from models.user import User

import hashlib


@api_views.route("/users",
                 methods=["GET"], strict_slashes=False)
def users():
    """ Retrives all users
    """
    users = [user.to_dict() for user in
             storage.all(User).values()]

    return jsonify(users)


@api_views.route("/users/<user_id>",
                 methods=["GET"], strict_slashes=False)
def user(user_id):
    """ Retrieve User by id
    """
    user = storage.get(User, user_id)

    if user is None:
        return abort(404)

    return jsonify(user.to_dict())


@api_views.route("/users/<user_id>",
                 methods=["DELETE"], strict_slashes=False)
def delete_user(user_id):
    """ Deletes User object
    """
    user = storage.get(User, user_id)

    if user is None:
        return abort(404)

    storage.delete(user)
    storage.save()

    return jsonify({}), 200


@api_views.route("/users",
                 methods=["POST"], strict_slashes=False)
def create_user():
    """ create new User
    """
    data = request.get_json()

    if data is None:
        return jsonify({"error": "Not a JSON"}), 400

    if data.get("email") is None:
        return jsonify({"error": "Missing email"}), 400

    if data.get("password") is None:
        return jsonify({"error": "Missing password"}), 400

    # hash user password
    data["password"] = hashlib.md5(data["password"].encode()).hexdigest()
    user = User(**data)
    user.save()

    return jsonify(user.to_dict()), 201


@api_views.route("/users/<user_id>",
                 methods=["PUT"], strict_slashes=False)
def update_user(user_id):
    """ Updates a User object
    """
    user = storage.get(User, user_id)
    data = request.get_json()

    if user is None:
        return abort(404)

    if data is None:
        return jsonify({"error": "Not a JSON"}), 400

    ignore_keys = ["id", "email", "created_at", "updated_at"]

    # hash user password
    if data.get("password"):
        data["password"] = hashlib.md5(kwargs["password"].encode()).hexdigest()

    for key, val in data.items():
        if key not in ignore_keys:
            setattr(user, key, val)
            user.save()

    return jsonify(user.to_dict()), 200
