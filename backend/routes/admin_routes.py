from datetime import datetime

from flask import Blueprint, jsonify, current_app, request
from flask_login import login_required, current_user
from sqlalchemy import or_
from models.user import User
from models.drive import Drive
from models.company import Company
from extensions import db, cache
from models.application import Application
from models.student import Student
from services.cache_keys import (
    admin_dashboard_key,
    admin_companies_key,
    admin_students_key,
    admin_drives_key,
    admin_applications_key,
    available_drives_key,
    company_dashboard_key
)
import os
from flask import send_from_directory

admin_bp = Blueprint("admin", __name__)


@admin_bp.route("/dashboard")
@login_required
@cache.cached(
    timeout=120,
    key_prefix=admin_dashboard_key
)
def admin_dashboard():

    print("Admin dashboard fetched from DATABASE")

    # 🔥 ROLE CHECK HERE (NO utils needed)
    if current_user.role != "admin":
        return jsonify({"error": "Unauthorized"}), 403

    total_students = User.query.filter_by(role="student").count()
    total_companies = User.query.filter_by(role="company").count()
    total_drives = Drive.query.count()

    return jsonify({
        "students": total_students,
        "companies": total_companies,
        "drives": total_drives
    })

@admin_bp.route("/approve-company/<int:company_id>", methods=["POST"])
@login_required
#@role_required("admin")
def approve_company(company_id):

    if current_user.role != "admin":
        return jsonify({"error": "Unauthorized"}), 403

    company = Company.query.get(company_id)

    if not company:
        return jsonify({"error": "Company not found"}), 404

    company.approval_status = "approved"
    db.session.commit()
    cache.delete(admin_dashboard_key())
    cache.delete(admin_companies_key())
    cache.delete(company_dashboard_key(company.id))

    return jsonify({"message": "Company approved"})

@admin_bp.route("/reject-company/<int:company_id>", methods=["POST"])
@login_required
def reject_company(company_id):

    if current_user.role != "admin":
        return jsonify({"error": "Unauthorized"}), 403

    company = Company.query.get(company_id)

    if not company:
        return jsonify({"error": "Company not found"}), 404

    if company.approval_status == "approved":
        return jsonify({
            "error": "Approved company cannot be rejected. Blacklist it instead."
        }), 400

    company.approval_status = "rejected"
    db.session.commit()
    cache.delete(admin_dashboard_key())
    cache.delete(admin_companies_key())
    cache.delete(company_dashboard_key(company.id))

    return jsonify({
        "message": "Company rejected successfully"
    }), 200

@admin_bp.route("/blacklist-company/<int:company_id>", methods=["POST"])
@login_required
def blacklist_company(company_id):

    if current_user.role != "admin":
        return jsonify({"error": "Unauthorized"}), 403

    company = Company.query.get(company_id)

    if not company:
        return jsonify({"error": "Company not found"}), 404

    if company.is_blacklisted:
        return jsonify({
            "error": "Company is already blacklisted"
        }), 400

    company.is_blacklisted = True

    # deactivate login
    company.user.is_active = False

    db.session.commit()
    cache.delete(admin_dashboard_key())
    cache.delete(admin_companies_key())
    cache.delete(company_dashboard_key(company.id))
    cache.delete(available_drives_key())

    return jsonify({
        "message": "Company blacklisted successfully"
    }), 200

@admin_bp.route("/approve-drive/<int:drive_id>", methods=["POST"])
@login_required
#@role_required("admin")
def approve_drive(drive_id):

    if current_user.role != "admin":
        return jsonify({"error": "Unauthorized"}), 403

    drive = Drive.query.get(drive_id)

    if not drive:
        return jsonify({"error": "Drive not found"}), 404

    drive.status = "approved"
    db.session.commit()
    cache.delete(admin_dashboard_key())
    cache.delete(admin_drives_key())
    cache.delete(available_drives_key())
    cache.delete(company_dashboard_key(drive.company_id))

    return jsonify({"message": "Drive approved"})

@admin_bp.route("/reject-drive/<int:drive_id>", methods=["POST"])
@login_required
def reject_drive(drive_id):

    if current_user.role != "admin":
        return jsonify({"error": "Unauthorized"}), 403

    drive = Drive.query.get(drive_id)

    if not drive:
        return jsonify({"error": "Drive not found"}), 404

    drive.status = "rejected"

    db.session.commit()
    cache.delete(admin_dashboard_key())
    cache.delete(admin_drives_key())
    cache.delete(company_dashboard_key(drive.company_id))

    return jsonify({
        "message": "Drive rejected successfully"
    }), 200

@admin_bp.route("/close-drive/<int:drive_id>", methods=["POST"])
@login_required
def close_drive(drive_id):

    if current_user.role != "admin":
        return jsonify({"error": "Unauthorized"}), 403

    drive = Drive.query.get(drive_id)

    if not drive:
        return jsonify({"error": "Drive not found"}), 404

    drive.status = "closed"

    db.session.commit()
    cache.delete(admin_dashboard_key())
    cache.delete(admin_drives_key())
    cache.delete(available_drives_key())
    cache.delete(company_dashboard_key(drive.company_id))

    return jsonify({
        "message": "Drive closed successfully"
    }), 200

@admin_bp.route("/companies", methods=["GET"])
@login_required
@cache.cached(
    timeout=120,
    key_prefix=admin_companies_key,
    unless=lambda: bool(request.args.get("search", "").strip())
)
def get_companies():

    if current_user.role != "admin":
        return jsonify({"error": "Unauthorized"}), 403

    search = request.args.get("search", "").strip()

    query = Company.query

    if search:
        query = query.filter(
            or_(
                Company.company_name.ilike(f"%{search}%"),
                Company.user.has(User.email.ilike(f"%{search}%"))
            )
        )

    companies = query.all()

    result = []

    for company in companies:

        result.append({
            "id": company.id,
            "company_name": company.company_name,
            "hr_contact": company.hr_contact,
            "website": company.website,
            "approval_status": company.approval_status
        })

    return jsonify(result), 200

@admin_bp.route("/company/<int:company_id>", methods=["GET"])
@login_required
def get_company(company_id):

    if current_user.role != "admin":
        return jsonify({"error": "Unauthorized"}), 403

    company = Company.query.get(company_id)

    if not company:
        return jsonify({"error": "Company not found"}), 404

    return jsonify({
        "id": company.id,
        "company_name": company.company_name,
        "email": company.user.email,
        "hr_contact": company.hr_contact,
        "website": company.website,
        "approval_status": company.approval_status
    }), 200

@admin_bp.route("/drives", methods=["GET"])
@login_required
@cache.cached(
    timeout=120,
    key_prefix=admin_drives_key
)
def get_drives():

    if current_user.role != "admin":
        return jsonify({"error": "Unauthorized"}), 403

    drives = Drive.query.all()

    result = []

    for drive in drives:

        result.append({
            "id": drive.id,
            "company": drive.company.company_name,
            "job_title": drive.job_title,
            "deadline": str(drive.deadline),
            "status": drive.status
        })

    return jsonify(result), 200

@admin_bp.route("/drive/<int:drive_id>", methods=["GET"])
@login_required
def get_drive(drive_id):

    if current_user.role != "admin":
        return jsonify({"error": "Unauthorized"}), 403

    drive = Drive.query.get(drive_id)

    if not drive:
        return jsonify({"error": "Drive not found"}), 404

    return jsonify({
        "id": drive.id,
        "company": drive.company.company_name,
        "job_title": drive.job_title,
        "job_description": drive.job_description,
        "eligibility_branch": drive.eligibility_branch,
        "eligibility_cgpa": drive.eligibility_cgpa,
        "eligibility_year": drive.eligibility_year,
        "deadline": str(drive.deadline),
        "status": drive.status
    }), 200

@admin_bp.route("/students", methods=["GET"])
@login_required
@cache.cached(
    timeout=120,
    key_prefix=admin_students_key,
    unless=lambda: bool(request.args.get("search", "").strip())
)
def get_students():

    if current_user.role != "admin":
        return jsonify({"error": "Unauthorized"}), 403

    search = request.args.get("search", "").strip()

    query = Student.query

    if search:
        query = query.filter(
            or_(
                Student.name.ilike(f"%{search}%"),
                Student.user.has(User.email.ilike(f"%{search}%"))
            )
        )

    students = query.all()

    result = []

    for student in students:

        result.append({
            "id": student.id,
            "name": student.name,
            "email": student.user.email,
            "department": student.department,
            "cgpa": student.cgpa,
            "graduation_year": student.graduation_year,
            "active": student.user.is_active
        })

    return jsonify(result), 200

@admin_bp.route("/student/<int:student_id>", methods=["GET"])
@login_required
def get_student(student_id):

    if current_user.role != "admin":
        return jsonify({"error": "Unauthorized"}), 403

    student = Student.query.get(student_id)

    if not student:
        return jsonify({"error": "Student not found"}), 404

    return jsonify({
        "id": student.id,
        "name": student.name,
        "email": student.user.email,
        "department": student.department,
        "cgpa": student.cgpa,
        "graduation_year": student.graduation_year,
        "active": student.user.is_active
    }), 200

@admin_bp.route("/blacklist-student/<int:student_id>", methods=["POST"])
@login_required
def blacklist_student(student_id):

    if current_user.role != "admin":
        return jsonify({"error": "Unauthorized"}), 403

    student = Student.query.get(student_id)

    if not student:
        return jsonify({"error": "Student not found"}), 404

    if not student.user.is_active:
        return jsonify({
            "error": "Student is already deactivated"
        }), 400

    student.user.is_active = False

    db.session.commit()
    cache.delete(admin_students_key())
    cache.delete(admin_dashboard_key())

    return jsonify({
        "message": "Student deactivated successfully"
    }), 200

@admin_bp.route("/blacklist-user/<int:user_id>", methods=["POST"])
@login_required
#@role_required("admin")
def blacklist_user(user_id):

    user = User.query.get(user_id)

    if not user:
        return jsonify({"error": "User not found"}), 404

    user.is_active = False

    # If company → also cancel drives
    if user.role == "company":
        company = user.company

        if company:
            company.is_blacklisted = True

            for drive in company.drives:
                drive.status = "closed"

    db.session.commit()

    return jsonify({"message": "User blacklisted"})

@admin_bp.route("/applications")
@login_required
@cache.cached(
    timeout=120,
    key_prefix=admin_applications_key
)
def get_applications():

    if current_user.role != "admin":
        return jsonify({"error": "Unauthorized"}), 403

    apps = Application.query.all()

    data = []

    for a in apps:
        data.append({
            "student": a.student.name,
            "drive": a.drive.job_title,
            "status": a.status
        })

    return jsonify(data), 200

@admin_bp.route("/reports", methods=["GET"])
@login_required
def get_reports():

    if current_user.role != "admin":
        return jsonify({"error": "Unauthorized"}), 403

    reports_folder = os.path.join(
        current_app.root_path,
        "reports"
    )

    os.makedirs(reports_folder, exist_ok=True)

    reports = []

    for file in os.listdir(reports_folder):

        if file.endswith(".csv"):

            filepath = os.path.join(
                reports_folder,
                file
            )

            reports.append({

                "filename": file,

                "size": round(
                    os.path.getsize(filepath) / 1024,
                    2
                ),

                "created_at": datetime.fromtimestamp(
                    os.path.getctime(filepath)
                ).strftime("%d-%m-%Y %H:%M")

            })

    reports.sort(
        key=lambda x: x["created_at"],
        reverse=True
    )

    return jsonify(reports)

@admin_bp.route("/reports/<filename>", methods=["GET"])
@login_required
def download_report(filename):

    if current_user.role != "admin":
        return jsonify({"error": "Unauthorized"}), 403

    reports_folder = os.path.join(
        current_app.root_path,
        "reports"
    )

    return send_from_directory(
        reports_folder,
        filename,
        as_attachment=True
    )
