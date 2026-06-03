from pydantic import BaseModel


class LoginRequest(BaseModel):
    email: str
    password: str


class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    employee_id: int
    employee_code: str
    employee_name: str
    email: str
    role: str