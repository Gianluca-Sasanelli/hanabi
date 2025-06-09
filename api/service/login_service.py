import os
from datetime import UTC, datetime, timedelta

import bcrypt
import dotenv
from jose import jwt
from sqlalchemy import select
from sqlalchemy.orm import Session

from api.models.models import User

dotenv.load_dotenv()
SECRET_KEY = str(os.getenv("SECRET_AUTH_KEY", ""))
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
if not SECRET_KEY:
    raise ValueError("SECRET_AUTH_KEY environment variable is not set")



def main(db: Session, email: str, password: str):
    user = auth_user(db, email, password)
    token_data = {
        "mail": user.email,
        "username": user.username,
        "id": str(user.id),
    }
    access_token = create_access_token(data=token_data)
    return access_token, str(user.id), user.username


def auth_user(db: Session, email: str, password: str):
    query = select(User).where(User.email == email)
    try:
        result =db.execute(query)
    except Exception as e:
        print(e)
        raise ValueError("There's an error in the server, please try again later")
    user = result.scalar_one_or_none()
    is_valid = bcrypt.checkpw(password.encode("utf-8"), user.password.encode("utf-8"))
    if not is_valid:
        raise ValueError("Invalid email or password")
    return user

def create_access_token(data: dict):
    to_encode = data.copy()

    current_time_utc = datetime.now(UTC)
    expire = current_time_utc + (timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))

    to_encode.update({"exp": expire})
    token = jwt.encode(to_encode, SECRET_KEY)
    return token

