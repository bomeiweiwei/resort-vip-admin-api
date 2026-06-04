from datetime import datetime
from pydantic import BaseModel, ConfigDict, EmailStr


class EmployeeResponse(BaseModel):
    employee_id: int
    employee_code: str
    employee_name: str
    email: str
    role: str
    department: str | None
    is_active: bool
    last_login_at: datetime | None
    created_at: datetime
    updated_at: datetime | None

    model_config = ConfigDict(from_attributes=True)

class EmployeeCreateRequest(BaseModel):
    employee_code: str
    employee_name: str
    email: EmailStr
    password: str
    role: str
    department: str | None = None