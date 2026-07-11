from extensions import db
from datetime import datetime


class Application(db.Model):

    __tablename__ = "applications"

    id = db.Column(db.Integer, primary_key=True)

    student_id = db.Column(db.Integer, db.ForeignKey("students.id"))

    drive_id = db.Column(db.Integer, db.ForeignKey("drives.id"))

    application_date = db.Column(db.DateTime, default=datetime.utcnow)

    status = db.Column(db.String(20), default="applied")
    # applied / shortlisted / rejected / selected / interview_scheduled

    __table_args__ = (
        db.UniqueConstraint("student_id", "drive_id", name="unique_application"),
    )