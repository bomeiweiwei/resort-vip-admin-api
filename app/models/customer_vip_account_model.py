from sqlalchemy import Column, Unicode, String, Boolean, DateTime, ForeignKey, text
from sqlalchemy.dialects.mssql import UNIQUEIDENTIFIER

from app.database import Base


class CustomerVipAccount(Base):
    __tablename__ = "CustomerVipAccount"
    __table_args__ = {"schema": "dbo"}

    customer_vip_account_id = Column(
        "CustomerVipAccountId",
        UNIQUEIDENTIFIER,
        primary_key=True,
        server_default=text("NEWSEQUENTIALID()"),
    )

    customer_id = Column(
        "CustomerId",
        UNIQUEIDENTIFIER,
        ForeignKey("dbo.Customer.CustomerId"),
        nullable=False,
    )

    login_account = Column("LoginAccount", Unicode(10), nullable=False)
    password_hash = Column("PasswordHash", Unicode(255), nullable=False)

    is_active = Column("IsActive", Boolean, nullable=False)
    expire_at = Column("ExpireAt", DateTime, nullable=False)
    last_login_at = Column("LastLoginAt", DateTime, nullable=True)

    created_at = Column(
        "CreatedAt",
        DateTime,
        nullable=False,
        server_default=text("SYSDATETIME()"),
    )

    updated_at = Column(
        "UpdatedAt",
        DateTime,
        nullable=False,
        server_default=text("SYSDATETIME()"),
    )