from sqlalchemy import Column, Integer, String, Boolean, DateTime

from app.database import Base


class Employee(Base):
    __tablename__ = "Employees"
    __table_args__ = {"schema": "dbo"}

    employee_id = Column("EmployeeId", Integer, primary_key=True, index=True)
    employee_code = Column("EmployeeCode", String(20), nullable=False)
    employee_name = Column("EmployeeName", String(50), nullable=False)
    email = Column("Email", String(100), nullable=False)
    password_hash = Column("PasswordHash", String(255), nullable=False)

    role = Column("Role", String(30), nullable=False)
    department = Column("Department", String(50), nullable=True)

    is_active = Column("IsActive", Boolean, nullable=False)

    last_login_at = Column("LastLoginAt", DateTime, nullable=True)
    created_at = Column("CreatedAt", DateTime, nullable=False)
    updated_at = Column("UpdatedAt", DateTime, nullable=True)