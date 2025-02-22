from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from marshmallow import ValidationError
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.exc import IntegrityError

from app.schemas import user_schema
from app.db import db, User


bp = Blueprint("user", __name__, url_prefix="/users")

@bp.route("/", methods=["POST"])
def register():
    json_data = request.json
    try:
        data = user_schema.load(json_data)
    except ValidationError as err:
        return jsonify(err.messages), 422

    try:
        new_user = User(
        username = data["username"],
            password = generate_password_hash(data["password"], method="pbkdf2")

        )
        db.session.add(new_user)
        db.session.commit()
    except IntegrityError as err:
        db.session.rollback()
        return jsonify(error="User already exist"), 400
    return jsonify(user_schema.dump(new_user)), 201  


@bp.route("/login", methods=["POST"])
def login():
    json_data = request.json
    try:
        data = user_schema.load(json_data)
    except ValidationError as err:
        return jsonify(err.messages), 422

    user = db.first_or_404(db.select(User).filter_by(username=data["username"]))

    if not check_password_hash(user.password, data["password"]):
        return jsonify(error="Wrong username or password"), 401

    access_token = create_access_token(identity=user.username)
    return jsonify(access_token=access_token)
