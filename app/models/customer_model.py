from sqlalchemy import Column, Unicode, String, Date, DateTime, SmallInteger
from sqlalchemy.dialects.mssql import UNIQUEIDENTIFIER

from app.database import Base
from sqlalchemy import text

class Customer(Base):
    __tablename__ = "Customer"
    __table_args__ = {"schema": "dbo"}

    customer_id = Column("CustomerId", UNIQUEIDENTIFIER, primary_key=True,server_default=text("NEWSEQUENTIALID()"))
    full_name = Column("FullName", Unicode(100), nullable=False)
    gender_id = Column("GenderId", SmallInteger, nullable=False)
    birth_date = Column("BirthDate", Date, nullable=True)
    country_code = Column("CountryCode", Unicode(10), nullable=False)
    mobile_phone = Column("MobilePhone", Unicode(30), nullable=True)
    phone = Column("Phone", Unicode(30), nullable=True)
    email = Column("Email", Unicode(100), nullable=True)
    created_at = Column("CreatedAt", DateTime, nullable=False)
    updated_at = Column("UpdatedAt", DateTime, nullable=False)