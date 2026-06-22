from fastapi import APIRouter, HTTPException
from database import get_connection
from schemas import (
    TaskCreate,
    TaskUpdate,
    TaskStatusUpdate
)
from auth import get_current_user
from typing import Optional

router = APIRouter(
prefix="/tasks",
tags=["Tasks"]
)

# ==========================

# CREATE TASK

# ==========================

@router.post("/", status_code=201)
def create_task(task: TaskCreate, token: str):
    email = get_current_user(token)

    allowed_priorities = [
    "low",
    "medium",
    "high"
    ]

    if task.priority not in allowed_priorities:
        raise HTTPException(
            status_code=400,
            detail="Priority must be low, medium or high"
        )

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
    """
    INSERT INTO tasks
    (
        title,
        description,
        priority,
        status,
        due_date,
        owner_email
    )
    VALUES (?, ?, ?, ?, ?, ?)
    """,
    (
        task.title,
        task.description,
        task.priority,
        task.status,
        task.due_date,
        email
    )
)

    conn.commit()
    conn.close()

    return {
        "message": "Task created successfully"
    }


# ==========================

# GET ALL TASKS

# ==========================

@router.get("/")
def get_tasks(
    token: str,
    status: Optional[str] = None,
    priority: Optional[str] = None
    ):


    email = get_current_user(token)

    conn = get_connection()
    cursor = conn.cursor()

    if status and priority:

        cursor.execute(
        """
        SELECT * FROM tasks
        WHERE owner_email=?
        AND status=?
        AND priority=?
        """,
        (email, status, priority)
        )

    elif status:

        cursor.execute(
        """
        SELECT * FROM tasks
        WHERE owner_email=?
        AND status=?
        """,
        (email, status)
        )

    elif priority:

     cursor.execute(
        """
        SELECT * FROM tasks
        WHERE owner_email=?
        AND priority=?
        """,
        (email, priority)
        )

    else:

        cursor.execute(
        """
        SELECT * FROM tasks
        WHERE owner_email=?
        """,
        (email,)
        )

    tasks = cursor.fetchall()

    conn.close()

    return [dict(task) for task in tasks]


# ==========================

# TASK SUMMARY

# ==========================

@router.get("/summary")
def task_summary(token: str):


    email = get_current_user(token)

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
    """
    SELECT COUNT(*) AS total
    FROM tasks
    WHERE owner_email=?
    """,
    (email,)
    )
    total = cursor.fetchone()["total"]

    cursor.execute(
    """
    SELECT COUNT(*) AS pending
    FROM tasks
    WHERE owner_email=?
    AND status='pending'
    """,
    (email,)
    )
    pending = cursor.fetchone()["pending"]

    cursor.execute(
    """
    SELECT COUNT(*) AS in_progress
    FROM tasks
    WHERE owner_email=?
    AND status='in-progress'
    """,
    (email,)
    )
    in_progress = cursor.fetchone()["in_progress"]

    cursor.execute(
    """
    SELECT COUNT(*) AS done
    FROM tasks
    WHERE owner_email=?
    AND status='done'
    """,
    (email,)
    )
    done = cursor.fetchone()["done"]

    conn.close()

    return {
    "total": total,
    "pending": pending,
    "in_progress": in_progress,
    "done": done
    }


# ==========================

# GET ONE TASK

# ==========================

@router.get("/{task_id}")
def get_task(task_id: int, token: str):


    email = get_current_user(token)

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
    "SELECT * FROM tasks WHERE id=?",
    (task_id,)
    )

    task = cursor.fetchone()

    if not task:
        conn.close()
        raise HTTPException(
        status_code=404,
        detail="Task not found"
        )

    if task["owner_email"] != email:
        conn.close()
        raise HTTPException(
        status_code=403,
        detail="Not allowed"
        )

    conn.close()

    return dict(task)


# ==========================

# UPDATE FULL TASK

# ==========================

@router.put("/{task_id}")
def update_task(
    task_id: int,
    task: TaskUpdate,
    token: str
):


    email = get_current_user(token)

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM tasks WHERE id=?",
    (task_id,)
    )

    existing = cursor.fetchone()

    if not existing:
        conn.close()
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    if existing["owner_email"] != email:
        conn.close()
        raise HTTPException(
            status_code=403,
            detail="Not allowed"
        )

    cursor.execute(
                         """
                        UPDATE tasks
                        SET title=?,
                        description=?,
                        priority=?,
                        status=?,
                        due_date=?
                         WHERE id=?
                        """,
        (
            task.title,
            task.description,
            task.priority,
            task.status,
            task.due_date,
            task_id
        )
    )

    conn.commit()
    conn.close()

    return {
    "message": "Task updated successfully"
    }


# ==========================

# UPDATE STATUS ONLY

# ==========================

@router.patch("/{task_id}/status")
def update_task_status(
    task_id: int,
    status_data: TaskStatusUpdate,
    token: str
    ):


    email = get_current_user(token)

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
                        "SELECT * FROM tasks WHERE id=?",
    (task_id,)
    )

    task = cursor.fetchone()

    if not task:
        conn.close()
        raise HTTPException(
                                status_code=404,
                                detail="Task not found"
        )

    if task["owner_email"] != email:
        conn.close()
        raise HTTPException(
                            status_code=403,
                            detail="Forbidden"
        )

    allowed_status = [
    "pending",
    "in-progress",
    "done"
    ]

    if status_data.status not in allowed_status:
        conn.close()
        raise HTTPException(
                status_code=400,
                detail="Invalid status"
        )

    cursor.execute(
                    """
                    UPDATE tasks
                    SET status=?
                     WHERE id=?
                     """,
        (
                status_data.status,
                task_id
        )
    )

    conn.commit()
    conn.close()

    return {
                "message": "Task status updated successfully"
    }


# ==========================

# DELETE TASK

# ==========================

@router.delete("/{task_id}")
def delete_task(
    task_id: int,
    token: str
    ):


    email = get_current_user(token)

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
                "SELECT * FROM tasks WHERE id=?",
                    (task_id,)
        )

    task = cursor.fetchone()

    if not task:
        conn.close()
        raise HTTPException(
            status_code=404,
            detail="Task not found"
    )

    if task["owner_email"] != email:
        conn.close()
        raise HTTPException(
            status_code=403,
            detail="Not allowed"
        )

    cursor.execute(
        "DELETE FROM tasks WHERE id=?",
        (task_id,)
    )

    conn.commit()
    conn.close()

    return {
        "message": "Task deleted successfully"
    }

