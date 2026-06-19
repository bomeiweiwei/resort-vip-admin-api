from sqlalchemy import Column, DateTime, ForeignKey, text
from sqlalchemy.dialects.mssql import UNIQUEIDENTIFIER
from sqlalchemy.types import NVARCHAR

from app.database import Base


class CustomerVipLoginToken(Base):
    __tablename__ = "CustomerVipLoginToken"
    __table_args__ = {"schema": "dbo"}

    token_id = Column(
        "TokenId",
        UNIQUEIDENTIFIER,
        primary_key=True,
        server_default=text("NEWSEQUENTIALID()"),
    )

    customer_vip_account_id = Column(
        "CustomerVipAccountId",
        UNIQUEIDENTIFIER,
        ForeignKey("dbo.CustomerVipAccount.CustomerVipAccountId"),
        nullable=False,
    )

    token_hash = Column(
        "TokenHash",
        NVARCHAR(255),
        nullable=False,
    )

    expire_at = Column(
        "ExpireAt",
        DateTime,
        nullable=False,
    )

    used_at = Column(
        "UsedAt",
        DateTime,
        nullable=True,
    )

    created_at = Column(
        "CreatedAt",
        DateTime,
        nullable=False,
        server_default=text("SYSDATETIME()"),
    )