from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.employee_schema import EmployeeResponse
from app.services.employee_service import EmployeeService


router = APIRouter()


@router.get("", response_model=list[EmployeeResponse])
def get_employees(db: Session = Depends(get_db)):
    service = EmployeeService(db)
    return service.get_employees()