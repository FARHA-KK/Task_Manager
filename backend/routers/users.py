from fastapi import APIRouter, HTTPException
from database import get_connection
from schemas import UserRegister, UserLogin
from auth import hash_password, verify_password, generate_token, sessions,get_current_user

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)



@router.post("/register")
def register(user: UserRegister):

    conn = get_connection()
    cursor = conn.cursor()

    # check if email exists
    cursor.execute(
        "SELECT * FROM users WHERE email = ?",
        (user.email,)
    )

    existing_user = cursor.fetchone()

    if existing_user:
        conn.close()
        raise HTTPException(status_code=400, detail="Email already exists")

    
    hashed_password = hash_password(user.password)
    cursor.execute(
        """
        INSERT INTO users(email, hashed_password)
        VALUES(?, ?)
        """,
        (user.email, hashed_password)
    )

    conn.commit()
    conn.close()

    return {"message": "User registered successfully"}

@router.post("/login")
def login(user: UserLogin):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM users WHERE email = ?",
        (user.email,)
    )

    db_user = cursor.fetchone()
    conn.close()

    if not db_user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    if not verify_password(user.password, db_user["hashed_password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = generate_token()
    sessions[token] = user.email

    return {
        "token": token,
        "message": "Login successful"
    }

@router.get("/me")
def me(token: str):

    email = get_current_user(token)

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT email FROM users WHERE email = ?",
        (email,)
    )

    user = cursor.fetchone()
    conn.close()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return {
        "email": user["email"]
    }