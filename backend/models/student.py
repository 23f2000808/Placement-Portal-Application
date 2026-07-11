from extensions import db


class Student(db.Model):

    __tablename__ = "students"

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))

    name = db.Column(db.String(100))

    department = db.Column(db.String(100))

    cgpa = db.Column(db.Float)

    graduation_year = db.Column(db.Integer)

    resume_path = db.Column(db.String(200))

    applications = db.relationship("Application", backref="student")