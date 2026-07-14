from datetime import date

from models.company import Company
from models.student import Student
from flask import Blueprint, request, jsonify, current_app
from flask_login import login_required, current_user

from extensions import db, cache
from models.application import Application
from models.drive import Drive

from services.cache_keys import (
    student_dashboard_key,
    student_applications_key,
    available_drives_key
)

import os

from werkzeug.utils import secure_filename
student_bp = Blueprint("student", __name__)

def allowed_file(filename):

    return (
        "." in filename and
        filename.rsplit(".",1)[1].lower()
        in current_app.config["ALLOWED_EXTENSIONS"]
    )


@student_bp.route("/dashboard", methods=["GET"])
@login_required
@cache.cached(
    timeout=120,
    key_prefix=lambda:
        student_dashboard_key(current_user.id)
)
def student_dashboard():

    print("Student dashboard fetched from DATABASE")

    # Only students can access this route
    if current_user.role != "student":
        return jsonify({"error": "Unauthorized"}), 403

    student = current_user.student

    # Safety check
    if not student:
        return jsonify({
            "error": "Student profile not found"
        }), 404

    total_applications = Application.query.filter_by(
        student_id=student.id
    ).count()

    return jsonify({
        "name": student.name,
        "email": current_user.email,
        "department": student.department,
        "cgpa": student.cgpa,
        "graduation_year": student.graduation_year,
        "resume_uploaded": bool(student.resume_path),
        "total_applications": total_applications
    }), 200


@student_bp.route("/profile", methods=["GET"])
@login_required
def get_student_profile():

    if current_user.role != "student":
        return jsonify({
            "error": "Unauthorized access"
        }), 403

    student = current_user.student

    if not student:
        return jsonify({
            "error": "Student profile not found"
        }), 404

    return jsonify({
        "name": student.name,
        "email": current_user.email,
        "department": student.department,
        "cgpa": student.cgpa,
        "graduation_year": student.graduation_year,
        "resume_uploaded": bool(student.resume_path)
    }), 200


@student_bp.route("/profile", methods=["PUT"])
@login_required
def update_student_profile():

    if current_user.role != "student":
        return jsonify({
            "error": "Unauthorized access"
        }), 403

    student = current_user.student

    if not student:
        return jsonify({
            "error": "Student profile not found"
        }), 404

    data = request.get_json(silent=True)

    if not data:
        return jsonify({
            "error": "Invalid request body"
        }), 400

    name = data.get("name")
    department = data.get("department")
    cgpa = data.get("cgpa")
    graduation_year = data.get("graduation_year")

    if not name or not str(name).strip():
        return jsonify({
            "error": "Name is required"
        }), 400

    if not department or not str(department).strip():
        return jsonify({
            "error": "Department is required"
        }), 400

    try:
        cgpa = float(cgpa)
    except (TypeError, ValueError):
        return jsonify({
            "error": "CGPA must be a valid number"
        }), 400

    if cgpa < 0 or cgpa > 10:
        return jsonify({
            "error": "CGPA must be between 0 and 10"
        }), 400

    try:
        graduation_year = int(graduation_year)
    except (TypeError, ValueError):
        return jsonify({
            "error": "Graduation year must be a valid number"
        }), 400

    if graduation_year < 2000 or graduation_year > 2100:
        return jsonify({
            "error": "Enter a valid graduation year"
        }), 400

    student.name = str(name).strip()
    student.department = str(department).strip()
    student.cgpa = cgpa
    student.graduation_year = graduation_year

    try:
        db.session.commit()
        cache.delete(
            student_dashboard_key(current_user.id)
        )
    except Exception:
        db.session.rollback()

        return jsonify({
            "error": "Unable to update profile"
        }), 500

    return jsonify({
        "message": "Profile updated successfully",
        "student": {
            "name": student.name,
            "email": current_user.email,
            "department": student.department,
            "cgpa": student.cgpa,
            "graduation_year": student.graduation_year,
            "resume_uploaded": bool(student.resume_path)
        }
    }), 200


@student_bp.route("/drives", methods=["GET"])
@login_required
@cache.cached(
    timeout=300,
    key_prefix=available_drives_key()
)
def get_available_drives():

    if current_user.role != "student":
        return jsonify({"error": "Unauthorized"}), 403

    drives = Drive.query.filter(
        Drive.status == "approved",
        Drive.deadline >= date.today()
    ).all()

    result = []

    for drive in drives:

        # Only show drives from active, approved companies
        if (
            drive.company.approval_status != "approved"
            or drive.company.is_blacklisted
            or not drive.company.user.is_active
        ):
            continue

        result.append({
            "id": drive.id,
            "company_name": drive.company.company_name,
            "job_title": drive.job_title,
            "eligibility_branch": drive.eligibility_branch,
            "eligibility_cgpa": drive.eligibility_cgpa,
            "eligibility_year": drive.eligibility_year,
            "deadline": drive.deadline.isoformat()
        })

    return jsonify(result), 200

@student_bp.route("/drives/<int:drive_id>", methods=["GET"])
@login_required
def get_drive_details(drive_id):
 
    if current_user.role != "student":
        return jsonify({
            "error": "Unauthorized access"
        }), 403

    student = Student.query.filter_by(
        user_id=current_user.id
    ).first()

    if not student:
        return jsonify({
            "error": "Student profile not found"
        }), 404

    drive = Drive.query.get(drive_id)

    if not drive:
        return jsonify({
            "error": "Drive not found"
        }), 404

    if drive.status != "approved":
        return jsonify({
            "error": "This drive is not available"
        }), 403

    company = Company.query.get(drive.company_id)

    existing_application = Application.query.filter_by(
        student_id=student.id,
        drive_id=drive.id
    ).first()

    return jsonify({
        "id": drive.id,
        "company_name": (
            company.company_name
            if company
            else "Unknown Company"
        ),
        "job_title": drive.job_title,
        "job_description": drive.job_description,
        "eligibility_branch": drive.eligibility_branch,
        "eligibility_cgpa": drive.eligibility_cgpa,
        "eligibility_year": drive.eligibility_year,
        "deadline": drive.deadline.isoformat(),

        "has_applied": existing_application is not None,

        "application_status": (
            existing_application.status
            if existing_application
            else None
        )
    }), 200


@student_bp.route("/drives/<int:drive_id>/apply", methods=["POST"])
@login_required
def apply_for_drive(drive_id):

    # 1. Only students can apply
    if current_user.role != "student":
        return jsonify({
            "error": "Only students can apply for placement drives"
        }), 403

    # 2. Find student profile
    student = Student.query.filter_by(
        user_id=current_user.id
    ).first()

    if not student:
        return jsonify({
            "error": "Student profile not found"
        }), 404

    # 3. Find the drive
    drive = Drive.query.get(drive_id)

    if not drive:
        return jsonify({
            "error": "Drive not found"
        }), 404

    # 4. Drive must be approved
    if drive.status != "approved":
        return jsonify({
            "error": "This drive is not open for applications"
        }), 400

    # 5. Company must still be approved
    company = Company.query.get(drive.company_id)

    if not company:
        return jsonify({
            "error": "Company not found"
        }), 404

    if company.approval_status != "approved":
        return jsonify({
            "error": "This company is not currently approved"
        }), 400

    # 6. Deadline must not have passed
    if drive.deadline < date.today():
        return jsonify({
            "error": "Application deadline has passed"
        }), 400

    # 7. Prevent duplicate applications
    existing_application = Application.query.filter_by(
        student_id=student.id,
        drive_id=drive.id
    ).first()

    if existing_application:
        return jsonify({
            "error": "You have already applied for this drive"
        }), 409

    # 8. Branch eligibility
    if student.department.strip().lower() != \
            drive.eligibility_branch.strip().lower():

        return jsonify({
            "error": (
                f"You are not eligible. "
                f"Required branch: {drive.eligibility_branch}"
            )
        }), 400

    # 9. CGPA eligibility
    if student.cgpa < drive.eligibility_cgpa:
        return jsonify({
            "error": (
                f"You are not eligible. Minimum CGPA required: "
                f"{drive.eligibility_cgpa}"
            )
        }), 400

    # 10. Graduation year eligibility
    if student.graduation_year != drive.eligibility_year:
        return jsonify({
            "error": (
                f"You are not eligible. Required graduation year: "
                f"{drive.eligibility_year}"
            )
        }), 400

    # 11. Create application
    application = Application(
        student_id=student.id,
        drive_id=drive.id,
        status="applied"
    )

    db.session.add(application)
    db.session.commit()

    cache.delete(
        student_dashboard_key(current_user.id)
    )

    cache.delete(
        student_applications_key(current_user.id)
    )

    cache.delete(
        available_drives_key()
    )

    return jsonify({
        "message": "Application submitted successfully",
        "application_id": application.id,
        "status": application.status
    }), 201

@student_bp.route("/applications", methods=["GET"])
@login_required
@cache.cached(
    timeout=120,
    key_prefix=lambda:
        student_applications_key(current_user.id)
)
def get_student_applications():

    if current_user.role != "student":
        return jsonify({
            "error": "Unauthorized access"
        }), 403

    student = Student.query.filter_by(
        user_id=current_user.id
    ).first()

    if not student:
        return jsonify({
            "error": "Student profile not found"
        }), 404

    applications = (
        Application.query
        .filter_by(student_id=student.id)
        .order_by(Application.application_date.desc())
        .all()
    )

    result = []

    for application in applications:

        drive = Drive.query.get(application.drive_id)

        if not drive:
            continue

        company = Company.query.get(drive.company_id)

        result.append({
            "id": application.id,
            "company_name": (
                company.company_name
                if company
                else "Unknown Company"
            ),
            "drive_id": drive.id,
            "job_title": drive.job_title,
            "application_date": (
                application.application_date.isoformat()
                if application.application_date
                else None
            ),
            "status": application.status
        })

    return jsonify(result), 200

@student_bp.route("/resume", methods=["POST"])
@login_required
def upload_resume():

    if current_user.role != "student":
        return jsonify({
            "error": "Unauthorized access"
        }), 403

    student = current_user.student

    if not student:
        return jsonify({
            "error": "Student profile not found"
        }), 404

    if "resume" not in request.files:
        return jsonify({
            "error": "No file uploaded"
        }), 400

    file = request.files["resume"]

    if file.filename == "":
        return jsonify({
            "error": "Please select a file"
        }), 400

    if not allowed_file(file.filename):
        return jsonify({
            "error": "Only PDF files are allowed"
        }), 400

    filename = secure_filename(
        f"resume_student_{student.id}.pdf"
    )

    filepath = os.path.join(
        current_app.config["UPLOAD_FOLDER"],
        filename
    )

    file.save(filepath)

    student.resume_path = filename

    db.session.commit()
    cache.delete(
        student_dashboard_key(current_user.id)
    )

    return jsonify({
        "message": "Resume uploaded successfully",
        "resume_path": filename
    }), 200

