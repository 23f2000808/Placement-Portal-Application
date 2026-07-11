import os


class Config:
    SECRET_KEY = os.environ.get(
    "SECRET_KEY",
    "placement-portal-secret-key"
)

    #SQLALCHEMY_DATABASE_URI = "sqlite:///database/db.sqlite3"
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))

    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(BASE_DIR, "database", "db.sqlite3")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    REDIS_URL = "redis://localhost:6379/0"
    CACHE_TYPE = "RedisCache"
    CACHE_REDIS_URL = REDIS_URL

    CELERY_BROKER_URL = REDIS_URL
    CELERY_RESULT_BACKEND = REDIS_URL

    UPLOAD_FOLDER = os.path.join(
        BASE_DIR,
        "uploads",
        "resumes"
    )

    ALLOWED_EXTENSIONS = {"pdf"}