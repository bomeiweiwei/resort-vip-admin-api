from sqlalchemy import Column, Unicode, DateTime, Integer, String
from sqlalchemy.dialects.mssql import UNIQUEIDENTIFIER

from app.database import Base


class CustomerServiceRequest(Base):
    __tablename__ = "CustomerServiceRequest"

    customer_service_request_id = Column(
        "CustomerServiceRequestId",
        UNIQUEIDENTIFIER,
        primary_key=True,
    )
    request_no = Column("RequestNo", Unicode(30), nullable=False)
    customer_vip_account_id = Column("CustomerVipAccountId", UNIQUEIDENTIFIER, nullable=False)
    customer_id = Column("CustomerId", UNIQUEIDENTIFIER, nullable=False)
    login_account = Column("LoginAccount", Unicode(10), nullable=False)

    booking_stay_id = Column("BookingStayId", UNIQUEIDENTIFIER, nullable=True)
    room_id = Column("RoomId", Integer, nullable=True)
    room_no = Column("RoomNo", Unicode(20), nullable=True)
    customer_name = Column("CustomerName", Unicode(100), nullable=True)

    message = Column("Message", Unicode(1000), nullable=False)
    language = Column("Language", Unicode(20), nullable=True)
    assigned_department = Column("AssignedDepartment", Unicode(50), nullable=True)

    status = Column("Status", Unicode(20), nullable=False)
    priority_level = Column("PriorityLevel", Unicode(20), nullable=False)
    remark = Column("Remark", Unicode(1000), nullable=True)

    created_at = Column("CreatedAt", DateTime, nullable=False)
    assigned_at = Column("AssignedAt", DateTime, nullable=True)
    completed_at = Column("CompletedAt", DateTime, nullable=True)