import csv
import os
from datetime import datetime

from tasks.celery_app import celery
from tasks.reminder_tasks import get_flask_app


@celery.task
def export_student_applications(student_id):

    app = get_flask_app()

    with app.app_context():

        from models.student import Student
        from models.application import Application
        from services.email_service import send_email

        student = Student.query.get(student_id)

        if not student:
            return

        reports_folder = os.path.join(
            app.root_path,
            "reports"
        )

        os.makedirs(
            reports_folder,
            exist_ok=True
        )

        filename = (
            f"student_{student.id}_applications_"
            f"{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        )

        filepath = os.path.join(
            reports_folder,
            filename
        )

        applications = (
            Application.query
            .filter_by(student_id=student.id)
            .all()
        )

        with open(
            filepath,
            "w",
            newline="",
            encoding="utf-8"
        ) as file:

            writer = csv.writer(file)

            writer.writerow([
                "Student ID",
                "Company Name",
                "Drive Title",
                "Application Status",
                "Application Date"
            ])

            for application in applications:

                drive = application.drive

                writer.writerow([
                    student.id,
                    drive.company.company_name,
                    drive.job_title,
                    application.status,
                    application.application_date
                ])

        html = f"""
        <html>

        <body style="font-family: Arial;">

        <h2>Placement Application Export</h2>

        <p>Hello <b>{student.name}</b>,</p>

        <p>
        Your application history has been exported successfully.
        </p>

        <p>
        The CSV file is attached with this email.
        </p>

        <table
        border="1"
        cellpadding="8"
        style="border-collapse:collapse;"
        >

        <tr>

        <td><b>Student</b></td>

        <td>{student.name}</td>

        </tr>

        <tr>

        <td><b>Total Applications</b></td>

        <td>{len(applications)}</td>

        </tr>

        <tr>

        <td><b>Generated On</b></td>

        <td>{datetime.now().strftime("%d-%m-%Y %H:%M")}</td>

        </tr>

        </table>

        <br>

        <p>

        Thank you for using the Placement Portal.

        </p>

        </body>

        </html>
        """

        send_email(
        subject="Placement Application Export Ready",
        recipients=[student.user.email],
        html=html,
        attachment_path=filepath
    )

        print(f"CSV generated for {student.user.email}")

        return filepath