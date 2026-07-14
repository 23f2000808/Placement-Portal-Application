import os
import sys
from datetime import date, timedelta

BACKEND_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

def ensure_backend_on_path():
    if BACKEND_DIR not in sys.path:
        sys.path.insert(0, BACKEND_DIR)


ensure_backend_on_path()

from tasks.celery_app import celery


def get_flask_app():
    ensure_backend_on_path()

    from app import app as flask_app

    return flask_app


@celery.task
def close_expired_drives():
    app = get_flask_app()

    from extensions import db
    from models.drive import Drive

    with app.app_context():

        expired = Drive.query.filter(
            Drive.deadline < date.today(),
            Drive.status == "approved"
        ).all()

        count = 0

        for drive in expired:
            drive.status = "closed"
            count += 1

        db.session.commit()

        print("=" * 60)
        print(f"{count} expired drives closed.")
        print("=" * 60)

        return count


@celery.task
def send_deadline_reminders():

    app = get_flask_app()

    from models.drive import Drive
    from models.student import Student
    from services.email_service import send_email

    with app.app_context():

        today = date.today()
        reminder_date = today + timedelta(days=3)

        drives = Drive.query.filter(
            Drive.status == "approved",
            Drive.deadline >= today,
            Drive.deadline <= reminder_date
        ).all()

        if not drives:
            print("No upcoming deadlines.")
            return 0

        students = Student.query.all()

        total_sent = 0

        for drive in drives:

            for student in students:

                if (
                    student.department != drive.eligibility_branch
                ):
                    continue

                if (
                    student.cgpa < drive.eligibility_cgpa
                ):
                    continue

                if (
                    student.graduation_year != drive.eligibility_year
                ):
                    continue

                send_email(

                    subject="Placement Drive Reminder",

                    recipients=[student.user.email],

                    body=f"""
Hello {student.name},

A placement drive is closing soon.

Company:
{drive.company.company_name}

Role:
{drive.job_title}

Deadline:
{drive.deadline}

Eligibility

Department:
{drive.eligibility_branch}

Minimum CGPA:
{drive.eligibility_cgpa}

Graduation Year:
{drive.eligibility_year}

Please login to the Placement Portal and apply before the deadline.

Best of luck!

Placement Portal
"""
                )

                total_sent += 1

                print(
                    f"Reminder sent to {student.user.email}"
                )

        print(
            f"\nTotal emails sent: {total_sent}"
        )

        return total_sent