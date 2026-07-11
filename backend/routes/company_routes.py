from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from extensions import db
from models.company import Company
from models.drive import Drive
from models.application import Application
from models.student import Student
from models.user import User
from datetime import datetime
from services.csv_export import export_applications_csv

company_bp = Blueprint("company", __name__)

@company_bp.route("/create-drive", methods=["POST"])
@login_required
def create_drive():

    if current_user.role != "company":
        return jsonify({"error": "Unauthorized"}), 403

    company = current_user.company

    # Prevent blacklisted companies from creating drives
    if company.is_blacklisted:
        return jsonify({
            "error": "Your company has been blacklisted. You cannot create placement drives."
        }), 403

    # ❗ Check approval
    if company.approval_status != "approved":
        return jsonify({"error": "Company not approved yet"}), 403

    data = request.get_json()

    # ----------------------------
    # Validate required fields
    # ----------------------------
    required_fields = [
        "job_title",
        "job_description",
        "eligibility_branch",
        "eligibility_cgpa",
        "eligibility_year",
        "deadline"
    ]

    for field in required_fields:
        if field not in data or data[field] == "":
            return jsonify({
                "error": f"{field} is required"
            }), 400

    deadline = datetime.strptime(data["deadline"], "%Y-%m-%d").date()

    # ----------------------------
    # Create Drive
    # ----------------------------
    drive = Drive(
        company_id=company.id,
        job_title=data["job_title"],
        job_description=data["job_description"],
        eligibility_branch=data["eligibility_branch"],
        eligibility_cgpa=data["eligibility_cgpa"],
        eligibility_year=data["eligibility_year"],
        deadline=deadline,
        status="pending"
    )

    db.session.add(drive)

    # ----------------------------
    # Commit once
    # ----------------------------
    db.session.commit()

    return jsonify({"message": "Drive created, waiting for admin approval"})

@company_bp.route("/drives/<int:drive_id>/applications", methods=["GET"])
@login_required
def get_drive_applications(drive_id):

    # Only company users can access this API
    if current_user.role != "company":
        return jsonify({
            "error": "Unauthorized access"
        }), 403

    # Find logged-in company's profile
    company = Company.query.filter_by(
        user_id=current_user.id
    ).first()

    if not company:
        return jsonify({
            "error": "Company profile not found"
        }), 404

    # Find the requested drive
    drive = Drive.query.get(drive_id)

    if not drive:
        return jsonify({
            "error": "Drive not found"
        }), 404

    # Important security rule:
    # a company can view applicants only for its own drive
    if drive.company_id != company.id:
        return jsonify({
            "error": "You cannot view applications for another company's drive"
        }), 403

    applications = (
        Application.query
        .filter_by(drive_id=drive.id)
        .order_by(Application.application_date.desc())
        .all()
    )

    result = []

    for application in applications:

        student = Student.query.get(application.student_id)

        if not student:
            continue

        user = User.query.get(student.user_id)

        result.append({
            "application_id": application.id,
            "student_id": student.id,
            "student_name": student.name,
            "email": user.email if user else None,
            "department": student.department,
            "cgpa": student.cgpa,
            "graduation_year": student.graduation_year,
            "resume_uploaded": bool(student.resume_path),
            "application_date": (
                application.application_date.isoformat()
                if application.application_date
                else None
            ),
            "status": application.status
        })

    return jsonify({
        "drive": {
            "id": drive.id,
            "job_title": drive.job_title,
            "status": drive.status
        },
        "total_applications": len(result),
        "applications": result
    }), 200

@company_bp.route(
    "/applications/<int:application_id>/status",
    methods=["PUT"]
)
@login_required
def update_application_status(application_id):

    # Only companies can update application status
    if current_user.role != "company":
        return jsonify({
            "error": "Unauthorized access"
        }), 403

    company = Company.query.filter_by(
        user_id=current_user.id
    ).first()

    if not company:
        return jsonify({
            "error": "Company profile not found"
        }), 404

    application = Application.query.get(application_id)

    if not application:
        return jsonify({
            "error": "Application not found"
        }), 404

    drive = Drive.query.get(application.drive_id)

    if not drive:
        return jsonify({
            "error": "Drive not found"
        }), 404

    # Security: company can update only its own drive applications
    if drive.company_id != company.id:
        return jsonify({
            "error": "You cannot manage another company's application"
        }), 403

    data = request.get_json()

    if not data or "status" not in data:
        return jsonify({
            "error": "Status is required"
        }), 400

    new_status = data["status"].strip().lower()

    allowed_statuses = [
        "applied",
        "shortlisted",
        "interview_scheduled",
        "selected",
        "rejected"
    ]

    if new_status not in allowed_statuses:
        return jsonify({
            "error": "Invalid application status"
        }), 400

    application.status = new_status

    db.session.commit()

    return jsonify({
        "message": "Application status updated successfully",
        "application_id": application.id,
        "status": application.status
    }), 200

@company_bp.route("/dashboard", methods=["GET"])
@login_required
def company_dashboard():

    if current_user.role != "company":
        return jsonify({
            "error": "Unauthorized access"
        }), 403

    company = Company.query.filter_by(
        user_id=current_user.id
    ).first()

    if not company:
        return jsonify({
            "error": "Company profile not found"
        }), 404

    drives = (
        Drive.query
        .filter_by(company_id=company.id)
        .order_by(Drive.created_at.desc())
        .all()
    )

    upcoming_drives = []
    closed_drives = []

    for drive in drives:
        application_count = Application.query.filter_by(
            drive_id=drive.id
        ).count()

        drive_data = {
            "id": drive.id,
            "job_title": drive.job_title,
            "deadline": (
                drive.deadline.isoformat()
                if drive.deadline
                else None
            ),
            "status": drive.status,
            "total_applications": application_count
        }

        if drive.status == "closed":
            closed_drives.append(drive_data)
        else:
            upcoming_drives.append(drive_data)

    return jsonify({
        "company": {
            "id": company.id,
            "company_name": company.company_name,
            "email": current_user.email,
            "hr_contact": company.hr_contact,
            "website": company.website,
            "approval_status": company.approval_status
        },

        "total_drives": len(drives),

        "upcoming_drives": upcoming_drives,
        "closed_drives": closed_drives

    }), 200

@company_bp.route("/drives/<int:drive_id>/complete", methods=["PUT"])
@login_required
def complete_drive(drive_id):

    if current_user.role != "company":
        return jsonify({
            "error": "Unauthorized access"
        }), 403

    company = Company.query.filter_by(
        user_id=current_user.id
    ).first()

    if not company:
        return jsonify({
            "error": "Company profile not found"
        }), 404

    drive = Drive.query.get(drive_id)

    if not drive:
        return jsonify({
            "error": "Drive not found"
        }), 404

    # Company can manage only its own drive
    if drive.company_id != company.id:
        return jsonify({
            "error": "You cannot manage another company's drive"
        }), 403

    if drive.status == "closed":
        return jsonify({
            "error": "Drive is already closed"
        }), 409

    # Only an approved drive can be completed
    if drive.status != "approved":
        return jsonify({
            "error": "Only approved drives can be marked as complete"
        }), 400

    drive.status = "closed"

    db.session.commit()

    return jsonify({
        "message": "Drive marked as complete",
        "drive_id": drive.id,
        "status": drive.status
    }), 200

@company_bp.route(
    "/drives/<int:drive_id>/export",
    methods=["GET"]
)
@login_required
def export_drive_csv(drive_id):

    if current_user.role != "company":
        return jsonify({
            "error": "Unauthorized"
        }),403

    drive = Drive.query.get_or_404(drive_id)

    if drive.company_id != current_user.company.id:
        return jsonify({
            "error":"Access denied"
        }),403

    return export_applications_csv(drive)