from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.employee_model import Employee
from app.schemas.employee_schema import EmployeeCreateRequest
from app.utils.security import get_password_hash

from datetime import datetime


class EmployeeService:
    def __init__(self, db: Session):
        self.db = db

    def get_employees(self) -> list[Employee]:
        return (
            self.db.query(Employee)
            .order_by(Employee.employee_id)
            .all()
        )
    
    def create_employee(self, request: EmployeeCreateRequest) -> Employee:
        exists_employee_code = (
            self.db.query(Employee)
            .filter(Employee.employee_code == request.employee_code)
            .first()
        )

        if exists_employee_code:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="員工編號已存在",
            )

        exists_email = (
            self.db.query(Employee)
            .filter(Employee.email == request.email)
            .first()
        )

        if exists_email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email 已存在",
            )

        employee = Employee(
            employee_code=request.employee_code,
            employee_name=request.employee_name,
            email=request.email,
            password_hash=get_password_hash(request.password),
            role=request.role,
            department=request.department,
            is_active=True,
            created_at=datetime.now(),
        )

        self.db.add(employee)
        self.db.commit()
        self.db.refresh(employee)

        return employee