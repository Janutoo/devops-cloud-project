# 🚀 DevOps Cloud Task Manager

A full-stack task management application built with Flask, containerized using Docker, and deployed on AWS EC2.

---

## 🌐 Live Demo

👉 http://YOUR_PUBLIC_IP:5000

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
* AWS EC2
* Linux
* Git
* JavaScript (Fetch API)
* Bootstrap

---

## ⚙️ Features

* ✅ Create tasks
* ✅ View tasks
* ✅ Update task status (done/undone)
* ✅ Delete tasks
* ✅ REST API (GET, POST, PUT, DELETE)
* ✅ Health check endpoint `/health`

---

## 📦 API Endpoints

| Method | Endpoint    | Description     |
| ------ | ----------- | --------------- |
| GET    | /tasks      | Get all tasks   |
| POST   | /tasks      | Create new task |
| PUT    | /tasks/{id} | Update task     |
| DELETE | /tasks/{id} | Delete task     |
| GET    | /health     | Health check    |

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
* Security group configured (ports 22, 5000)
* Public access enabled

---

## 📂 Project Structure

```
app/
 ├── templates/
 │    └── index.html
 ├── app.py
 ├── requirements.txt

dockerfile
README.md
```

---

## 🧠 What I Learned

* How to deploy applications to the cloud (AWS EC2)
* How to containerize applications using Docker
* How to design and implement REST APIs
* How frontend communicates with backend (HTTP/JSON)
* Basics of DevOps workflow

