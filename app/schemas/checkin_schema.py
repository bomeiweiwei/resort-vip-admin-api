from datetime import date
from pydantic import BaseModel, EmailStr


class RoomTypeResponse(BaseModel):
    room_type_id: int
    room_type_name: str


class RoomResponse(BaseModel):
    room_id: int
    room_no: str


class SpecialNoteRequest(BaseModel):
    note_type: str | None = None
    note_content: str


class CheckInCreateRequest(BaseModel):
    full_name: str
    gender_id: int
    birth_date: date | None = None
    country_code: str
    mobile_phone: str | None = None
    phone: str | None = None
    email: EmailStr | None = None

    room_type_id: int
    room_id: int
    check_in_date: date
    check_out_date: date
    adult_count: int
    child_count: int

    has_parking: bool
    license_plate_no: str | None = None

    notes: list[SpecialNoteRequest] = []


class CheckInCreateResponse(BaseModel):
    customer_id: str
    booking_stay_id: str
    vip_login_account: str
    vip_initial_password: str
    vip_login_url: str
    vip_magic_login_url: str