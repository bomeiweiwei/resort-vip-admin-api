from sqlalchemy import Column, Unicode, Integer, String, Boolean, DateTime

from app.database import Base


class Employee(Base):
    __tablename__ = "Employees"
    __table_args__ = {"schema": "dbo"}

    employee_id = Column("EmployeeId", Integer, primary_key=True, index=True)
    employee_code = Column("EmployeeCode", Unicode(20), nullable=False)
    employee_name = Column("EmployeeName", Unicode(50), nullable=False)
    email = Column("Email", Unicode(100), nullable=False)
    password_hash = Column("PasswordHash", Unicode(255), nullable=False)

    role = Column("Role", Unicode(30), nullable=False)
    department = Column("Department", Unicode(50), nullable=True)

    is_active = Column("IsActive", Boolean, nullable=False)

    last_login_at = Column("LastLoginAt", DateTime, nullable=True)
    created_at = Column("CreatedAt", DateTime, nullable=False)
    updated_at = Column("UpdatedAt", DateTime, nullable=True)