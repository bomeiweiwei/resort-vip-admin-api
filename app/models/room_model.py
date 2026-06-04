from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from app.database import Base


class RoomType(Base):
    __tablename__ = "RoomType"
    __table_args__ = {"schema": "dbo"}

    room_type_id = Column("RoomTypeId", Integer, primary_key=True)
    room_type_name = Column("RoomTypeName", String(100), nullable=False)
    description = Column("Description", String(500), nullable=True)
    max_adult_count = Column("MaxAdultCount", Integer, nullable=False)
    max_child_count = Column("MaxChildCount", Integer, nullable=False)
    is_active = Column("IsActive", Boolean, nullable=False)


class Room(Base):
    __tablename__ = "Room"
    __table_args__ = {"schema": "dbo"}

    room_id = Column("RoomId", Integer, primary_key=True)
    room_type_id = Column("RoomTypeId", Integer, ForeignKey("dbo.RoomType.RoomTypeId"))
    room_no = Column("RoomNo", String(20), nullable=False)
    floor_no = Column("FloorNo", Integer, nullable=True)
    is_active = Column("IsActive", Boolean, nullable=False)