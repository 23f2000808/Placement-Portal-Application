import os
import csv
from datetime import datetime

from tasks.celery_app import celery
from tasks.reminder_tasks import get_flask_app


@celery.task
def generate_monthly_report():

    app = get_flask_app()

    with app.app_context():

        from models.student import Student
        from models.company import Company
        from models.drive import Drive
        from models.application import Application

        report = {
            "Generated On": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "Total Students": Student.query.count(),
            "Total Companies": Company.query.count(),
            "Total Drives": Drive.query.count(),
            "Approved Drives": Drive.query.filter_by(status="approved").count(),
            "Closed Drives": Drive.query.filter_by(status="closed").count(),
            "Applications": Application.query.count(),
            "Selected": Application.query.filter_by(status="selected").count(),
            "Rejected": Application.query.filter_by(status="rejected").count(),
            "Shortlisted": Application.query.filter_by(status="shortlisted").count(),
            "Applied": Application.query.filter_by(status="applied").count(),
        }

        reports_folder = os.path.join(
            app.root_path,
            "reports"
        )

        os.makedirs(reports_folder, exist_ok=True)

        filename = (
            f"placement_report_"
            f"{datetime.now().strftime('%Y_%m_%d_%H_%M_%S')}.csv"
        )

        filepath = os.path.join(
            reports_folder,
            filename
        )

        with open(
            filepath,
            "w",
            newline="",
            encoding="utf-8"
        ) as csvfile:

            writer = csv.writer(csvfile)

            writer.writerow(["Metric", "Value"])

            for key, value in report.items():
                writer.writerow([key, value])

        print("=" * 60)
        print("MONTHLY REPORT GENERATED")
        print(filepath)
        print("=" * 60)

        return filepath