from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.employee_model import Employee
from app.schemas.auth_schema import LoginRequest, LoginResponse
from app.utils.security import verify_password, create_access_token


class AuthService:
    def __init__(self, db: Session):
        self.db = db

    def login(self, request: LoginRequest) -> LoginResponse:
        employee = (
            self.db.query(Employee)
            .filter(Employee.email == request.email)
            .first()
        )

        if employee is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="帳號或密碼錯誤",
            )

        if not employee.is_active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="此帳號已停用",
            )

        if not verify_password(request.password, employee.password_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="帳號或密碼錯誤",
            )

        access_token = create_access_token(
            data={
                "sub": employee.email,
                "employee_id": employee.employee_id,
                "role": employee.role,
            }
        )

        return LoginResponse(
            access_token=access_token,
            employee_id=employee.employee_id,
            employee_code=employee.employee_code,
            employee_name=employee.employee_name,
            email=employee.email,
            role=employee.role,
        )