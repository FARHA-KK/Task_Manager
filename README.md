# Personal Task Manager

## Overview

Personal Task Manager is a full-stack task management application developed using FastAPI, SQLite, and Streamlit. The application enables users to securely manage their daily tasks through an intuitive and user-friendly interface.

Users can register, log in, create tasks, update task details, track progress, manage priorities, and monitor task completion through a dashboard. The project demonstrates full-stack development concepts including authentication, CRUD operations, API integration, database management, and frontend-backend communication.

---

## Features

### Authentication

* User Registration
* User Login
* Session-Based Authentication
* Logout with Confirmation
* Email and Password Validation

### Task Management

* Create New Tasks
* View All Tasks
* View Individual Task Details
* Update Existing Tasks
* Delete Tasks with Confirmation
* Change Task Status
* Mark Tasks as Done
* Set Task Priority
* Manage Due Dates

### Dashboard

* Total Tasks Count
* Pending Tasks Count
* In Progress Tasks Count
* Completed Tasks Count
* Filter Tasks by Status
* Filter Tasks by Priority
* Select Tasks from Dropdown List

### Additional Features

* Task Detail Page
* Edit Task Page
* Error Handling
* API Connection Validation
* User-Friendly Interface

---

## Tech Stack

| Technology   | Purpose                     |
| ------------ | --------------------------- |
| Python 3.11+ | Programming Language        |
| FastAPI      | Backend API Framework       |
| SQLite       | Database Management         |
| Streamlit    | Frontend User Interface     |
| Requests     | API Communication           |
| Pandas       | Data Processing and Display |
| Pydantic     | Data Validation             |
| Git & GitHub | Version Control             |

---

## Project Structure

```text
task_manager/
│
├── backend/
│   ├── main.py
│   ├── database.py
│   ├── auth.py
│   ├── schemas.py
│   └── routers/
│       └── tasks.py
│
├── frontend/
│   └── app.py
│
├── requirements.txt
├── .gitignore
└── README.md
```

---

## Installation and Setup

### 1. Clone the Repository

```bash
git clone https://github.com/FARHA-KK/Task_Manager.git
cd Task_Manager
```

### 2. Create a Virtual Environment

#### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

#### Linux / macOS

```bash
python -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file inside the backend folder:

```env
SECRET_KEY=your_secret_key
```

### 5. Run the Backend Server

```bash
cd backend
uvicorn main:app --reload
```

Backend URL:

```text
http://127.0.0.1:8000
```

### 6. Run the Frontend Application

Open a new terminal:

```bash
cd frontend
streamlit run app.py
```

Frontend URL:

```text
http://localhost:8501
```

---

## API Endpoints

| Method | Endpoint           | Authentication Required | Description                      |
| ------ | ------------------ | ----------------------- | -------------------------------- |
| POST   | /auth/register     | No                      | Register a new user              |
| POST   | /auth/login        | No                      | Authenticate user                |
| POST   | /tasks/            | Yes                     | Create a task                    |
| GET    | /tasks/            | Yes                     | Retrieve all tasks               |
| GET    | /tasks/{id}        | Yes                     | Retrieve a specific task         |
| PUT    | /tasks/{id}        | Yes                     | Update task details              |
| PATCH  | /tasks/{id}/status | Yes                     | Update task status               |
| DELETE | /tasks/{id}        | Yes                     | Delete a task                    |
| GET    | /tasks/summary     | Yes                     | Retrieve task summary statistics |

---
## Future Enhancements

* Task Search Functionality
* Due Date Notifications
* Dark Mode Theme
* Task Categories and Labels
* User Profile Management
* Email Notifications
* Data Export (CSV/PDF)

---

## Author

**Fathima Farha**

B.Tech Computer Science and Engineering (CSE)
MEA Engineering College

Interested in Full-Stack Development, Python, FastAPI, Streamlit, and Software Engineering.


