from flask_sqlalchemy import SQLAlchemy
from flask import jsonify
from flask_login import LoginManager

db = SQLAlchemy()

login_manager = LoginManager()


@login_manager.unauthorized_handler
def unauthorized():
    return jsonify({"error": "Please login first"}), 401
