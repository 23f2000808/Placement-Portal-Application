from flask import Blueprint, request, jsonify
from extensions import db
from models.user import User
from models.student import Student
from models.company import Company
from flask_login import login_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash


auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/register/student", methods=["POST"])
def register_student():

    data = request.get_json()

    # ----------------------------
    # Validate required fields
    # ----------------------------
    required_fields = [
        "email",
        "password",
        "name",
        "department",
        "cgpa",
        "graduation_year"
    ]

    for field in required_fields:
        if field not in data or data[field] == "":
            return jsonify({
                "error": f"{field} is required"
            }), 400

    # ----------------------------
    # Check duplicate email
    # ----------------------------
    existing_user = User.query.filter_by(email=data["email"]).first()

    if existing_user:
        return jsonify({
            "error": "Email already exists"
        }), 409

    # ----------------------------
    # Hash password
    # ----------------------------
    hashed_password = generate_password_hash(data["password"])

    # ----------------------------
    # Create User
    # ----------------------------
    user = User(
        email=data["email"],
        password=hashed_password,
        role="student"
    )

    db.session.add(user)
    db.session.flush()

    # ----------------------------
    # Create Student
    # ----------------------------
    student = Student(
        user_id=user.id,
        name=data["name"],
        department=data["department"],
        cgpa=data["cgpa"],
        graduation_year=data["graduation_year"]
    )

    db.session.add(student)

    # ----------------------------
    # Commit once
    # ----------------------------
    db.session.commit()

    return jsonify({
        "message": "Student registered successfully"
    }), 201

@auth_bp.route("/register/company", methods=["POST"])
def register_company():

    data = request.get_json()

    # ----------------------------
    # Validate required fields
    # ----------------------------
    required_fields = [
        "email",
        "password",
        "company_name",
        "hr_contact",
        "website"
    ]

    for field in required_fields:
        if field not in data or data[field] == "":
            return jsonify({
                "error": f"{field} is required"
            }), 400

    # ----------------------------
    # Check duplicate email
    # ----------------------------
    existing_user = User.query.filter_by(email=data["email"]).first()

    if existing_user:
        return jsonify({
            "error": "Email already exists"
        }), 409

    # ----------------------------
    # Hash password
    # ----------------------------
    hashed_password = generate_password_hash(data["password"])

    # ----------------------------
    # Create User
    # ----------------------------
    user = User(
        email=data["email"],
        password=hashed_password,
        role="company"
    )

    db.session.add(user)
    db.session.flush()

    # ----------------------------
    # Create Company
    # ----------------------------
    company = Company(
        user_id=user.id,
        company_name=data["company_name"],
        hr_contact=data["hr_contact"],
        website=data["website"]
    )

    db.session.add(company)

    # ----------------------------
    # Commit once
    # ----------------------------
    db.session.commit()

    return jsonify({
        "message": "Company registered (pending approval)"
    }), 201

@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.json

    user = User.query.filter_by(email=data["email"]).first()

    if not user:
        return jsonify({"error": "Invalid email"}), 401

    if not check_password_hash(user.password, data["password"]):
        return jsonify({"error": "Invalid password"}), 401

    if not user.is_active:
        return jsonify({
            "error": "Account has been deactivated. Contact admin."
        }), 403

    login_user(user)

    return jsonify({
        "message": "Login successful",
        "role": user.role
    })

@auth_bp.route("/logout", methods=["POST"])
def logout():
    logout_user()
    return jsonify({"message": "Logged out"})
