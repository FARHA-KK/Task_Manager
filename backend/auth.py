import uuid
import bcrypt
from fastapi import HTTPException

def get_current_user(token: str):
    if token not in sessions:
        raise HTTPException(
            status_code=401,
            detail="Invalid token"
        )
    return sessions[token]

sessions = {}


def hash_password(password: str):
    return bcrypt.hashpw(
        password.encode(),
        bcrypt.gensalt()
    ).decode()


def verify_password(password: str, hashed_password: str):
    return bcrypt.checkpw(
        password.encode(),
        hashed_password.encode()
    )


def generate_token():
    return str(uuid.uuid4())