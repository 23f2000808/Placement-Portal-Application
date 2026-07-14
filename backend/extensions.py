from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask import jsonify
from flask_caching import Cache
from flask_mail import Mail

mail = Mail()

db = SQLAlchemy()

login_manager = LoginManager()

cache = Cache()


@login_manager.unauthorized_handler
def unauthorized():
    return jsonify({
        "error": "Please login first"
    }), 401