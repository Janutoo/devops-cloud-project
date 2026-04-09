# 🚀 DevOps Cloud Task Manager

A full-stack task management application built with Flask, containerized using Docker, and deployed on AWS EC2.

---

## 🌐 Live Demo

👉 http://YOUR_PUBLIC_IP:8080

(Replace `YOUR_PUBLIC_IP` with your AWS EC2 instance's public IP address)

---

## 🧠 Project Overview

This project demonstrates a complete DevOps workflow:

* Building a REST API with Python (Flask)
* Creating a frontend UI using JavaScript and Bootstrap
* Containerizing the application with Docker
* Deploying the app on AWS EC2
* Configuring networking and security (ports, public access)

---

## 🛠️ Tech Stack

* Python (Flask)
* Docker
* Kubernetes (planned)
* Terraform (planned)
* AWS EC2
* Linux
* Git
* JavaScript (Fetch API)
* Bootstrap

---

## ⚙️ Features

* ✅ User authentication (login/logout)
* ✅ Session management with Flask-Login
* ✅ User-specific task management
* ✅ Create tasks
* ✅ View tasks
* ✅ Update task status (done/undone)
* ✅ Delete tasks
* ✅ REST API (GET, POST, PUT, DELETE)
* ✅ Health check endpoint `/health`

---

## 📦 API Endpoints

| Method | Endpoint       | Description          | Authentication |
| ------ | -------------- | -------------------- | -------------- |
| GET    | /              | Home page            | Required       |
| GET    | /login         | Login page           | N/A            |
| POST   | /login         | Login user           | N/A            |
| GET    | /logout        | Logout user          | Required       |
| GET    | /api/tasks     | Get user's tasks     | Required       |
| POST   | /api/tasks     | Create new task      | Required       |
| PUT    | /api/tasks/{id}| Update task status   | Required       |
| DELETE | /api/tasks/{id}| Delete task          | Required       |
---

## 🔐 Authentication System

The application includes a complete user authentication system:

* **Session-based authentication** using Flask-Login
* **Automatic user creation** on first login
* **Protected routes** requiring authentication
* **User-specific data isolation** - each user sees only their own tasks
* **Secure logout** functionality

Users can log in with any username, and the system will create an account automatically if it doesn't exist.

---

## 🐳 Run Locally (Docker)

```bash
docker build -t task-api .
docker run -p 5000:5000 task-api
```

---

## ☁️ Deployment (AWS)

The application is deployed on an AWS EC2 instance:

* Ubuntu server
* Docker installed
* Security group configured (ports 22, 8080)
* Public access enabled

---

## 📂 Project Structure

```
.
├── app/
│   ├── templates/
│   │   ├── index.html          (Main task manager UI)
│   │   ├── login.html          (Login page)
│   │   └── members.html        (Members page)
│   ├── app.py                   (Flask application)
│   └── requirements.txt         (Python dependencies)
├── docker/
│   └── (Docker-related files - planned)
├── k8s/
│   └── (Kubernetes manifests - planned)
├── terraform/
│   └── (Infrastructure as Code - planned)
├── dockerfile                    (Docker image definition)
├── .gitignore                    (Git ignore rules)
└── README.md                     (Project documentation)
```


## 🧠 What I Learned

* How to deploy applications to the cloud (AWS EC2)
* How to containerize applications using Docker
* How to design and implement REST APIs
* How frontend communicates with backend (HTTP/JSON)
* How to implement user authentication and session management
* How to build user-specific features with data isolation
* Basics of DevOps workflow

---

## 🚀 Future Enhancements

* **Kubernetes Deployment**: Container orchestration with K8s manifests
* **Infrastructure as Code**: Automated provisioning with Terraform
* **CI/CD Pipeline**: Automated testing and deployment
* **Database Integration**: Persistent data storage
* **Monitoring**: Application performance and health monitoring