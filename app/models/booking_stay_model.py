from sqlalchemy import Column, Unicode, Integer, String, Date, DateTime, Boolean, ForeignKey
from sqlalchemy.dialects.mssql import UNIQUEIDENTIFIER

from app.database import Base
from sqlalchemy import text


class BookingStay(Base):
    __tablename__ = "BookingStay"
    __table_args__ = {"schema": "dbo"}

    booking_stay_id = Column("BookingStayId", UNIQUEIDENTIFIER, primary_key=True,server_default=text("NEWSEQUENTIALID()"))
    customer_id = Column("CustomerId", UNIQUEIDENTIFIER, nullable=False)
    room_id = Column("RoomId", Integer, nullable=False)
    check_in_date = Column("CheckInDate", Date, nullable=False)
    check_out_date = Column("CheckOutDate", Date, nullable=False)
    adult_count = Column("AdultCount", Integer, nullable=False)
    child_count = Column("ChildCount", Integer, nullable=False)
    has_parking = Column("HasParking", Boolean, nullable=False)
    license_plate_no = Column("LicensePlateNo", Unicode(20), nullable=True)
    created_at = Column("CreatedAt", DateTime, nullable=False)
    updated_at = Column("UpdatedAt", DateTime, nullable=False)


class BookingStayNote(Base):
    __tablename__ = "BookingStayNote"
    __table_args__ = {"schema": "dbo"}

    booking_stay_note_id = Column("BookingStayNoteId", UNIQUEIDENTIFIER, primary_key=True,server_default=text("NEWSEQUENTIALID()"))
    booking_stay_id = Column("BookingStayId", UNIQUEIDENTIFIER, ForeignKey("dbo.BookingStay.BookingStayId"))
    note_type = Column("NoteType", Unicode(50), nullable=True)
    note_content = Column("NoteContent", Unicode(500), nullable=False)
    created_at = Column("CreatedAt", DateTime, nullable=False)