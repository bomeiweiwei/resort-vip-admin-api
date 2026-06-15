from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.dialects.mssql import UNIQUEIDENTIFIER

from app.database import Base


class CustomerServiceRequest(Base):
    __tablename__ = "CustomerServiceRequest"

    customer_service_request_id = Column(
        "CustomerServiceRequestId",
        UNIQUEIDENTIFIER,
        primary_key=True,
    )
    request_no = Column("RequestNo", String(30), nullable=False)
    customer_vip_account_id = Column("CustomerVipAccountId", UNIQUEIDENTIFIER, nullable=False)
    customer_id = Column("CustomerId", UNIQUEIDENTIFIER, nullable=False)
    login_account = Column("LoginAccount", String(10), nullable=False)

    booking_stay_id = Column("BookingStayId", UNIQUEIDENTIFIER, nullable=True)
    room_id = Column("RoomId", Integer, nullable=True)
    room_no = Column("RoomNo", String(20), nullable=True)
    customer_name = Column("CustomerName", String(100), nullable=True)

    message = Column("Message", String(1000), nullable=False)
    language = Column("Language", String(20), nullable=True)
    assigned_department = Column("AssignedDepartment", String(50), nullable=True)

    status = Column("Status", String(20), nullable=False)
    priority_level = Column("PriorityLevel", String(20), nullable=False)
    remark = Column("Remark", String(1000), nullable=True)

    created_at = Column("CreatedAt", DateTime, nullable=False)
    assigned_at = Column("AssignedAt", DateTime, nullable=True)
    completed_at = Column("CompletedAt", DateTime, nullable=True)