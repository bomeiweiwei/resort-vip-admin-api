from fastapi import APIRouter, Depends
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