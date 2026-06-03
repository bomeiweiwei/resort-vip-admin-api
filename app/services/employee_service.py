from sqlalchemy.orm import Session

from app.models.employee_model import Employee


class EmployeeService:
    def __init__(self, db: Session):
        self.db = db

    def get_employees(self) -> list[Employee]:
        return (
            self.db.query(Employee)
            .order_by(Employee.employee_id)
            .all()
        )