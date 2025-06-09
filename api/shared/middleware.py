import uuid
from fastapi import Depends, Request
from sqlalchemy.orm import Session
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi.security import OAuth2PasswordBearer
from api.shared.db_connections import get_postgres_session
from jose import jwt, ExpiredSignatureError, JWTError
from api.shared.responses import AuthenticationError
from api.repository import UserRepository
from api.models.models import User
import os


SECRET_KEY = str(os.getenv("SECRET_AUTH_KEY", ""))
ALGORITHM = "HS256"


async def verify_token(request: Request, db: Session = Depends(get_postgres_session)):
    token = request.cookies.get("access_token")
    print("The token is", token)
    if not token:
        raise AuthenticationError("The token is not found")
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except ExpiredSignatureError:
        raise AuthenticationError("The token has expired")
    except JWTError:
        raise AuthenticationError("The token is invalid")
    user_id = payload.get("id")
    if not user_id or not isinstance(user_id, str):
        raise AuthenticationError("The token is invalid")
    user_repo = UserRepository(db = db)
    user = user_repo.get_by_id(user_id)
    if not user:
        raise AuthenticationError("The user was not found by the middleware")
    return user

