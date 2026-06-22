# Personal Task Manager

## Overview

Personal Task Manager is a full-stack task management application built using FastAPI, SQLite, and Streamlit.

Users can:

* Register and Login
* Create Tasks
* View Tasks
* Update Tasks
* Delete Tasks
* Change Task Status
* Filter Tasks
* View Task Summary Dashboard

This project demonstrates complete CRUD operations, authentication, API integration, and frontend development using Streamlit.

---

## Features

### Authentication

* User Registration
* User Login
* Session Token Management
* Logout

### Task Management

* Create Task
* View All Tasks
* View Task Details
* Update Task
* Delete Task
* Mark Task as Done
* Change Task Status (Pending, In Progress, Done)

### Dashboard

* Total Tasks Count
* Pending Tasks Count
* In Progress Tasks Count
* Done Tasks Count
* Filter by Status
* Filter by Priority
* Select Task by Name

### Additional Features

* Delete Confirmation
* Error Handling
* API Connection Validation
* Task Detail Page
* Edit Task Page

---

## Technologies Used

### Backend

* Python
* FastAPI
* SQLite
* Pydantic

### Frontend

* Streamlit
* Requests
* Pandas

### Version Control

* Git
* GitHub

---

## Project Structure

task-manager/
├── backend/
│ ├── main.py ← FastAPI app, startup, middleware, error handlers
│ ├── database.py ← SQLite connection, init_db(), all DB helper functions
│ ├── auth.py ← password hashing, token generation, get_current_user()
│ ├── schemas.py ← Pydantic models (TaskCreate, TaskUpdate,
TaskResponse...)
│ ├── routers/
│ │ ├── tasks.py ← all /tasks endpoints
│ │ └── users.py ← /auth/register, /auth/login, /auth/me
│ └── .env ← SECRET_KEY (never commit this file)
├── frontend/
│ └── app.py ← entire Streamlit app, all pages
├── requirements.txt ← all pip packages
├── .gitignore
└── README.md

## Installation

### Clone Repository

git clone https://github.com/FARHA-KK/Task_Manager.git

cd Task_Manager

### Install Dependencies

pip install -r requirements.txt

### Run Backend

uvicorn main:app --reload

### Run Frontend

streamlit run app.py

---

## API Endpoints

### Authentication

POST /auth/register

POST /auth/login

GET /auth/me

### Tasks

POST /tasks

GET /tasks

GET /tasks/{id}

PUT /tasks/{id}

PATCH /tasks/{id}/status

DELETE /tasks/{id}

GET /tasks/summary

---

## Future Improvements

* Task Search
* Due Date Reminders
* Dark Mode UI
* User Profile Page
* Task Categories
* Email Notifications

---

## Author

Fathima Farha

B.Tech Computer Science and Engineering (CSE) Student

MEA Engineering College

Passionate about Python, FastAPI, Web Development, and Software Engineering.

This project was developed as part of learning full-stack application development using FastAPI, SQLite, Streamlit, Git, and GitHub.
