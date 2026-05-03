import hashlib
from datetime import datetime
from models import User, Calculation

def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

def register_user(username: str, password: str) -> tuple[bool, str]:
    if User.select().where(User.username == username).exists():
        return False, "Username already taken"
    User.create(username=username, password_hash=hash_password(password))
    return True, "Register successfully"

def login_user(username: str, password: str):
    try:
        user = User.get(User.username == username)
        if user.password_hash == hash_password(password):
            return user
        return None
    except User.DoesNotExist:
        return None
    

def save_calculation(user_id: int, expression: str, result: str):
    Calculation.create(
        user=user_id,
        expression=expression,
        result=result,
        created_at=datetime.now()
    )


def get_history(user_id: int):
    return (Calculation
            .select()
            .where(Calculation.user == user_id)
            .order_by(Calculation.created_at.desc()))