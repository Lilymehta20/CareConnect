# CareConnect — Django MVP

A starter healthcare appointment platform built with Python, Django, Supabase PostgreSQL and SQLite fallback.

## Included
- Patient, doctor and administrator roles
- Registration and login
- Doctor profiles and specialization search
- Appointment booking, cancellation and doctor status updates
- Patient medical records and doctor prescriptions
- Admin verification workflow for doctor profiles
- Feedback submission
- Django admin panel

## Run locally
```bash
python -m venv venv
# Windows:
venv\\Scripts\\activate
# macOS/Linux:
source venv/bin/activate

pip install -r requirements.txt
python manage.py makemigrations clinic
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```
Open http://127.0.0.1:8000/

Local development enables Django's debug mode by default so `runserver` serves the admin static files. On Vercel it defaults to off; set the `DEBUG` environment variable explicitly to override either default.

## Supabase database setup

CareConnect uses Supabase PostgreSQL when `SUPABASE_DB_URL` or `DATABASE_URL` is set. Otherwise, it uses SQLite.

Windows PowerShell:
```powershell
$env:SUPABASE_DB_URL="postgresql://postgres.[project-ref]:[password]@aws-0-[region].pooler.supabase.com:6543/postgres"
python manage.py migrate
python manage.py runserver
```

The fallback database alias is `sqlite_fallback`. The application uses `default`; setting `SUPABASE_DB_URL` removes the need for SQLite while preserving the local SQLite database for fallback/local use.

Register a doctor account, then use the Django admin (`/admin/`) to mark the doctor's profile as verified. Patients can then find and book that doctor.

## Demo workflow
1. Register as a doctor and complete the doctor profile.
2. Sign in to `/admin/` using your superuser and verify the doctor.
3. Register as a patient, search for a doctor and book an appointment.
4. The doctor can accept/complete appointments and add a prescription.
5. Patients can view their appointments, records and prescriptions.

## Important production work still required
This is an educational MVP, not a production-ready medical system. Before real deployment, add HTTPS, secure hosting, audit logs, consent management, encryption and backups, stronger access controls, rate limiting, validated file uploads, privacy/legal review, and tested database migrations. Payment, real-time chat, video calls, AI recommendations, SMS/email reminders and external lab integrations are intentionally left as integration points; do not collect real patient data in this demo.
