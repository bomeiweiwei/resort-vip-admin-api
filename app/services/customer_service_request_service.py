from uuid import UUID

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.customer_service_request_model import CustomerServiceRequest


class CustomerServiceRequestService:
    def get_all(self, db: Session):
        return (
            db.query(CustomerServiceRequest)
            .order_by(CustomerServiceRequest.created_at.desc())
            .all()
        )

    def get_by_id(self, db: Session, customer_service_request_id: UUID):
        data = (
            db.query(CustomerServiceRequest)
            .filter(
                CustomerServiceRequest.customer_service_request_id
                == customer_service_request_id
            )
            .first()
        )

        if data is None:
            raise HTTPException(
                status_code=404,
                detail="找不到客服需求資料",
            )

        return data


customer_service_request_service = CustomerServiceRequestService()