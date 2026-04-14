# TaskFlow

TaskFlow is a Flask-based task manager with authentication, calendar-based planning, smart filtering, recurring tasks, project grouping, and notes/attachments.

## Overview

This project includes:

- Flask backend with session auth (Flask-Login)
- Modern dashboard UI (Bootstrap + custom CSS)
- Theme switcher (Ocean, Light, Midnight)
- Calendar with due-date visualization and filtering
- Task metadata: priority, project, tags, recurrence, notes, attachment URL

Important: data is stored in memory (Python lists). After app restart, users and tasks are reset.

## Current Features

- Login/logout with automatic user creation on first login
- User-scoped task ownership in the UI
- Create/update/delete tasks
- Due date support + calendar badges
- Productivity views: All, Today, This Week, Overdue
- Project filter + search + sorting
- Recurring tasks: daily, weekly, monthly
- Notes (comments) per task
- Attachment link per task
- Members page with completed task summary
- Health endpoint: /health

## Tech Stack

- Python 3.11
- Flask 3.1.3
- Flask-Login
- Bootstrap 5.3
- Vanilla JavaScript
- Docker

## Project Structure

```text
.
├── dockerfile
├── README.md
└── app/
		├── app.py
		├── requirements.txt
		├── static/
		│   └── css/
		│       └── style.css
		└── templates/
				├── base.html
				├── index.html
				├── login.html
				└── members.html
```

## Run Locally (Python)

### Windows PowerShell

```powershell
cd d:\devops-cloud-project
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r app\requirements.txt
python app\app.py
```

### Git Bash

```bash
cd /d/devops-cloud-project
python -m venv venv
source venv/Scripts/activate
pip install -r app/requirements.txt
python app/app.py
```

App URL: http://127.0.0.1:5000

## Run with Docker

```bash
docker build -f dockerfile -t taskflow .
docker run --rm -p 5000:5000 taskflow
```

## CI/CD

This repository now includes simple GitHub Actions workflows:

- CI workflow: [.github/workflows/ci.yml](.github/workflows/ci.yml)
- CD workflow: [.github/workflows/cd.yml](.github/workflows/cd.yml)

### CI

The CI pipeline runs on every push to `main` and `develop`, and on each pull request. It does the minimum expected for a small project:

- installs Python dependencies
- validates Python syntax
- starts the Flask app and checks `/health`
- builds the Docker image

### CD

The CD pipeline runs on push to `main`. It does the minimum deploy flow:

- logs in to GitHub Container Registry (`ghcr.io`)
- builds the Docker image from [dockerfile](dockerfile)
- pushes the image
- connects to your server over SSH
- pulls the newest image and restarts the container

Published image format:

```text
ghcr.io/<owner>/<repo>/taskflow:latest
ghcr.io/<owner>/<repo>/taskflow:sha-<commit>
```

### Required GitHub secrets

- `DEPLOY_HOST` - server IP or domain
- `DEPLOY_USER` - SSH user on the server
- `DEPLOY_SSH_KEY` - private SSH key used by GitHub Actions
- `GHCR_USERNAME` - GitHub username used for container registry login
- `GHCR_TOKEN` - GitHub token or PAT with permission to pull packages from GHCR

### What this gives you

- `CI` = build + basic test
- `CD` = Docker image publish + deploy on server

This is enough to say that the project has a real basic CI/CD pipeline.

## Authentication

- Open /login
- Use any username
- Password is currently hardcoded: passat

This is a development setup, not production security.

## API Reference

All /api endpoints require authenticated session cookie.

### GET /api/tasks

Returns all tasks currently stored in memory.

### POST /api/tasks

Create task.

Example body:

```json
{
	"title": "Release checklist",
	"priority": "High",
	"due_date": "2026-04-15",
	"project": "Product",
	"tags": "release, deployment",
	"recurrence": "weekly",
	"attachment_url": "https://example.com/spec",
	"initial_note": "Prepare rollback plan"
}
```

### PUT /api/tasks/<id>

Update any subset of fields:

- done
- title
- priority (Low, Medium, High)
- due_date (YYYY-MM-DD)
- project
- tags (string CSV or array)
- recurrence (none, daily, weekly, monthly)
- attachment_url
- comment (adds a note)

If a recurring task is marked done for the first time, next occurrence is auto-created.

### DELETE /api/tasks/<id>

Delete task by ID.

### GET /health

Returns:

```json
{"status": "ok"}
```

## Known Limitations

- No persistent database yet
- No registration/password hashing
- No file upload storage (attachment is URL-only)
- No background scheduler/notifications

## Suggested Next Steps

- Add SQLite/PostgreSQL + migrations
- Add proper auth (hashed passwords, registration, roles)
- Add test suite (API + UI flow)
- Add CI/CD pipeline and deployment automation