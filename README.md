# Placement Portal Application

A full-stack Placement Portal built using **Flask**, **Vue.js**, **SQLite**, **Redis**, and **Celery**. The portal streamlines the campus placement process by allowing students to apply for placement drives, companies to manage recruitment, and administrators to oversee the entire placement workflow.

---

## Features

### Authentication
- Student Registration & Login
- Company Registration & Login
- Admin Login
- Role-based Authentication & Authorization

### Student Module
- View available placement drives
- Eligibility checking before applying
- Apply for placement drives
- Upload resume (PDF)
- Update profile
- View application history

### Company Module
- Register company account
- Create placement drives
- View applicants
- Shortlist, Reject, or Select students
- Export applicant list to CSV

### Admin Module
- Approve/Reject company registrations
- Approve/Reject placement drives
- Search students
- Search companies
- Blacklist students
- Blacklist companies
- View system reports
- Download monthly placement reports

---

## Advanced Features

### Redis Caching
- Dashboard caching
- Student dashboard caching
- Company dashboard caching
- Admin dashboard caching
- Automatic cache invalidation after updates

### Celery Background Tasks
- Automatically closes expired placement drives
- Sends reminder emails to eligible students before application deadlines
- Generates monthly placement reports

### Report Generation
- Monthly reports generated automatically
- Reports stored as CSV files
- Download reports from Admin Dashboard

### Email Notifications
- Gmail SMTP integration
- Reminder emails sent to eligible students for upcoming placement drive deadlines

---

## Tech Stack

### Backend
- Flask
- SQLAlchemy
- Flask-Login
- Flask-Caching
- Flask-Mail
- Celery
- Redis

### Frontend
- Vue.js 3
- Vue Router
- Axios
- Bootstrap 5

### Database
- SQLite

---

## Project Structure

```text
backend/
│
├── app.py
├── config.py
├── extensions.py
├── requirements.txt
├── models/
├── routes/
├── services/
│   ├── cache_keys.py
│   └── email_service.py
├── tasks/
├── uploads/
├── reports/
└── database/

frontend/
│
├── src/
│   ├── views/
│   ├── router/
│   ├── services/
│   └── components/
├── package.json
├── package-lock.json
└── requirements.txt
```

---

## Installation

### Clone Repository

```bash
git clone <https://github.com/23f2000808/Placement-Portal-Application.git>
cd Placement_Portal_Application_23f2000808
```

---

### Backend Setup

Create Virtual Environment

From the project root:

```bash
cd backend
python -m venv venv
```

Activate

Windows

```bash
.\venv\Scripts\activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

---

### Frontend Setup

From the project root:

```bash
cd frontend
npm install
npm run dev
```

---

### Run Backend

From the project root:

```bash
cd backend
.\venv\Scripts\activate
python app.py
```

Backend runs on:

```text
http://localhost:5000
```

Frontend runs on:

```text
http://localhost:5173
```

---

## Redis Setup

Run Redis using Docker

```bash
docker run -d --name placement-redis -p 6379:6379 redis
```

Verify

```bash
docker exec -it placement-redis redis-cli ping
```

Expected

```
PONG
```

---

## Celery Worker

From the project root:

```bash
cd backend
.\venv\Scripts\activate
celery -A tasks.celery_app.celery worker --pool=solo --loglevel=info
```

---

## Celery Beat

From the project root:

```bash
cd backend
.\venv\Scripts\activate
celery -A tasks.celery_app.celery beat --loglevel=info
```

Run the project with separate terminals for:

- Redis
- Flask backend
- Vue frontend
- Celery worker
- Celery beat

---

## Email Configuration

Create a `.env` file inside the backend directory.

```env
MAIL_USERNAME=your_email@gmail.com
MAIL_PASSWORD=your_16_character_google_app_password
```

Google App Password is required.

---

## Scheduled Tasks

### Daily Reminder

- Runs automatically every day
- Finds placement drives approaching their deadline
- Sends reminder emails to eligible students

---

### Automatic Drive Closure

- Automatically closes expired placement drives

---

### Monthly Report

- Runs automatically on the first day of every month
- Generates placement statistics
- Stores report in the `reports/` folder
- Reports are downloadable from the Admin Dashboard

---

## Caching

Redis is used to cache frequently accessed data:

- Student Dashboard
- Company Dashboard
- Admin Dashboard
- Company Applications
- Student Applications

Cache is automatically invalidated whenever data changes.

---

## API Highlights

### Authentication

```
POST /api/login
POST /api/register/student
POST /api/register/company
POST /api/logout
```

### Student

```
GET  /api/student/dashboard
GET  /api/student/drives
GET  /api/student/drives/<id>
POST /api/student/drives/<id>/apply
GET  /api/student/applications
POST /api/student/resume
PUT  /api/student/profile
```

### Company

```
POST /api/company/create-drive
GET  /api/company/dashboard
GET  /api/company/drives/<id>/applications
GET  /api/company/drives/<id>/export
```

### Admin

```
GET  /api/admin/dashboard
GET  /api/admin/companies
GET  /api/admin/students
POST /api/admin/approve-company/<id>
POST /api/admin/approve-drive/<id>
GET  /api/admin/reports
GET  /api/admin/reports/<filename>
```

---

## Future Improvements

- JWT Authentication
- Interview Scheduling
- Notification Center
- Placement Analytics Dashboard
- Cloud Deployment (Azure/AWS)
- PostgreSQL Support

---

## Author

**Deepak Kumar Pathak**


---

## License

This project was developed as part of the Modern Application Development II course and is intended for educational purposes.
