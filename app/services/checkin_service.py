from datetime import datetime
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.customer_model import Customer
from app.models.room_model import Room, RoomType
from app.models.booking_stay_model import BookingStay, BookingStayNote
from app.schemas.checkin_schema import CheckInCreateRequest


class CheckInService:
    def __init__(self, db: Session):
        self.db = db

    def get_room_types(self):
        return (
            self.db.query(RoomType)
            .filter(RoomType.is_active == True)
            .order_by(RoomType.room_type_id)
            .all()
        )

    def get_rooms_by_room_type(self, room_type_id: int):
        return (
            self.db.query(Room)
            .filter(Room.room_type_id == room_type_id)
            .filter(Room.is_active == True)
            .order_by(Room.room_no)
            .all()
        )

    def create_checkin(self, request: CheckInCreateRequest):
        if request.check_out_date <= request.check_in_date:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="退房日期必須晚於入住日期",
            )

        room = (
            self.db.query(Room)
            .filter(Room.room_id == request.room_id)
            .filter(Room.room_type_id == request.room_type_id)
            .filter(Room.is_active == True)
            .first()
        )

        if room is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="房型與房號不符合或房間不存在",
            )

        now = datetime.now()

        customer = Customer(
            full_name=request.full_name,
            gender_id=request.gender_id,
            birth_date=request.birth_date,
            country_code=request.country_code,
            mobile_phone=request.mobile_phone,
            phone=request.phone,
            email=request.email,
            created_at=now,
            updated_at=now,
        )

        self.db.add(customer)
        self.db.flush()

        booking = BookingStay(
            customer_id=customer.customer_id,
            room_id=request.room_id,
            check_in_date=request.check_in_date,
            check_out_date=request.check_out_date,
            adult_count=request.adult_count,
            child_count=request.child_count,
            has_parking=request.has_parking,
            license_plate_no=request.license_plate_no,
            created_at=now,
            updated_at=now,
        )

        self.db.add(booking)
        self.db.flush()

        for note in request.notes:
            if note.note_content.strip():
                self.db.add(
                    BookingStayNote(
                        booking_stay_id=booking.booking_stay_id,
                        note_type=note.note_type,
                        note_content=note.note_content,
                        created_at=now,
                    )
                )

        self.db.commit()

        return {
            "customer_id": str(customer.customer_id),
            "booking_stay_id": str(booking.booking_stay_id),
        }