from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class CustomerServiceReqListItem(BaseModel):
    customer_service_request_id: UUID
    request_no: str
    room_no: Optional[str] = None
    customer_name: Optional[str] = None
    message: str
    assigned_department: Optional[str] = None
    status: str
    priority_level: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class CustomerServiceReqDetail(BaseModel):
    customer_service_request_id: UUID
    request_no: str

    customer_vip_account_id: UUID
    customer_id: UUID
    login_account: str

    booking_stay_id: Optional[UUID] = None
    room_id: Optional[int] = None
    room_no: Optional[str] = None
    customer_name: Optional[str] = None

    message: str
    language: Optional[str] = None
    assigned_department: Optional[str] = None
    status: str
    priority_level: str
    remark: Optional[str] = None

    created_at: datetime
    assigned_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)