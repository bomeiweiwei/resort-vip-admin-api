from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.customer_service_request_schema import (
    CustomerServiceReqDetail,
    CustomerServiceReqListItem,
)
from app.services.customer_service_request_service import (
    customer_service_request_service,
)

from app.dependencies.auth_dependency import get_current_user

router = APIRouter()

@router.get(
    "/customer-service-req-list",
    response_model=List[CustomerServiceReqListItem],
)
def get_customer_service_req_list(
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return customer_service_request_service.get_all(db)


@router.get(
    "/customer-service-req-detail/{customer_service_request_id}",
    response_model=CustomerServiceReqDetail,
)
def get_customer_service_req_detail(
    customer_service_request_id: UUID,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return customer_service_request_service.get_by_id(
        db,
        customer_service_request_id,
    )