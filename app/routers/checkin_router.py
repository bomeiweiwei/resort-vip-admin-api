from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies.auth_dependency import get_current_user
from app.schemas.checkin_schema import (
    CheckInCreateRequest,
    CheckInCreateResponse,
    RoomResponse,
    RoomTypeResponse,
)
from app.services.checkin_service import CheckInService

router = APIRouter()


@router.get("/room-types", response_model=list[RoomTypeResponse])
def get_room_types(
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    service = CheckInService(db)
    return service.get_room_types()


@router.get("/rooms", response_model=list[RoomResponse])
def get_rooms_by_room_type(
    room_type_id: int,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    service = CheckInService(db)
    return service.get_rooms_by_room_type(room_type_id)


@router.post("", response_model=CheckInCreateResponse)
def create_checkin(
    request: CheckInCreateRequest,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    service = CheckInService(db)
    return service.create_checkin(request)


@router.post("/{customer_id}/generate-recommendation")
def generate_recommendation(
    customer_id: str,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    try:
        service = CheckInService(db)

        result = service.generate_recommendation(
            customer_id=customer_id
        )

        return {
            "success": True,
            "message": "AI 推薦產生成功",
            "data": result,
        }

    except ValueError as e:
        raise HTTPException(
            status_code=404,
            detail=str(e),
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"AI 推薦產生失敗：{str(e)}",
        )