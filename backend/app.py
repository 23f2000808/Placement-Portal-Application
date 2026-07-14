from flask import Flask
from config import Config
from extensions import db, login_manager, cache, mail
from werkzeug.security import generate_password_hash
from flask_cors import CORS


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    import os

    os.makedirs(
        app.config["UPLOAD_FOLDER"],
        exist_ok=True
    )


    CORS(
    app,
    origins=["http://localhost:5173"],
    supports_credentials=True
)

    # ----------------------------
    # Initialize Extensions
    # ----------------------------
    db.init_app(app)
    login_manager.init_app(app)
    cache.init_app(app)
    mail.init_app(app)
    # ----------------------------
    # Import Models
    # ----------------------------
    from models.user import User
    from models.student import Student
    from models.company import Company
    from models.drive import Drive
    from models.application import Application

    # ----------------------------
    # Import Blueprints
    # ----------------------------
    from routes.auth_routes import auth_bp
    from routes.admin_routes import admin_bp
    from routes.company_routes import company_bp
    from routes.student_routes import student_bp

    # ----------------------------
    # Register Blueprints
    # ----------------------------
    app.register_blueprint(auth_bp, url_prefix="/api")
    app.register_blueprint(admin_bp, url_prefix="/api/admin")
    app.register_blueprint(company_bp, url_prefix="/api/company")
    app.register_blueprint(student_bp, url_prefix="/api/student")

    # ----------------------------
    # Create Database & Default Admin
    # ----------------------------
    with app.app_context():

        db.create_all()

        admin = User.query.filter_by(role="admin").first()

        if admin is None:

            admin = User(
                email="admin@placement.com",
                password=generate_password_hash("admin123"),
                role="admin",
                is_active=True
            )

            db.session.add(admin)
            db.session.commit()

            print("Default Admin Created")
        else:
            print("Default Admin Already Exists")

    return app


# Create Flask Application
app = create_app()


if __name__ == "__main__":
    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True
    )


