from io import StringIO
import csv

from flask import make_response


def export_applications_csv(drive):

    output = StringIO()

    writer = csv.writer(output)

    writer.writerow([
        "Student Name",
        "Email",
        "Department",
        "CGPA",
        "Graduation Year",
        "Status"
    ])

    for application in drive.applications:

        student = application.student

        writer.writerow([
            student.name,
            student.user.email,
            student.department,
            student.cgpa,
            student.graduation_year,
            application.status
        ])

    response = make_response(output.getvalue())

    response.headers[
        "Content-Disposition"
    ] = f"attachment; filename=drive_{drive.id}_applications.csv"

    response.headers[
        "Content-Type"
    ] = "text/csv"

    return response