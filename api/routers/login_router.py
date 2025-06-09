from fastapi import APIRouter, Depends, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from sqlalchemy.orm import Session

from api.service.login_service import main
from api.shared.db_connections import get_postgres_session
from api.shared.middleware import verify_token
from api.models.models import User

class LoginRequest(BaseModel):
    email: str
    password: str

class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

router = APIRouter(prefix="/login", tags=["authentication"])

@router.post("/")
async def login(login_data: LoginRequest, request: Request, db: Session = Depends(get_postgres_session)):
    token, user_id, username = main(db, login_data.email, login_data.password)
    request.state.user_id = user_id
    response = JSONResponse(content={"username": username})
    response.set_cookie(key="access_token", value=token, httponly=False, secure=False, max_age=7*24*60*60, samesite="Lax", domain=None)
    return response

@router.get("/")
async def get_user(request: Request, db: Session = Depends(get_postgres_session), user: User = Depends(verify_token)):
    return JSONResponse(content={"username": user.username})