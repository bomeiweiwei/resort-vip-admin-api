from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.auth_schema import LoginRequest, LoginResponse
from app.services.auth_service import AuthService


router = APIRouter()


@router.post("/login", response_model=LoginResponse)
def login(
    request: LoginRequest,
    db: Session = Depends(get_db),
):
    service = AuthService(db)
    return service.login(request)