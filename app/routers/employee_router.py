from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.employee_schema import EmployeeResponse
from app.services.employee_service import EmployeeService

from app.dependencies.auth_dependency import get_current_user

router = APIRouter()


@router.get("", response_model=list[EmployeeResponse])
def get_employees(
    current_user=Depends(get_current_user), db: Session = Depends(get_db)
):
    service = EmployeeService(db)
    return service.get_employees()
