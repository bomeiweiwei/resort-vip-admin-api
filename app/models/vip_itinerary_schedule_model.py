from sqlalchemy import Column, Date, String, ForeignKey, Unicode
from sqlalchemy.dialects.mssql import UNIQUEIDENTIFIER

from app.database import Base


class VipItinerarySchedule(Base):
    __tablename__ = "VipItinerarySchedule"

    schedule_id = Column(
        "ScheduleId",
        UNIQUEIDENTIFIER,
        primary_key=True,
    )

    recommendation_id = Column(
        "RecommendationId",
        UNIQUEIDENTIFIER,
        ForeignKey(
            "VipItineraryRecommendation.RecommendationId"
        ),
        nullable=False,
    )

    schedule_date = Column(
        "ScheduleDate",
        Date,
        nullable=False,
    )

    schedule_time = Column(
        "ScheduleTime",
        String(5),
        nullable=False,
    )

    title = Column(
        "Title",
        Unicode(200),
        nullable=False,
    )

    content = Column(
        "Content",
        Unicode,
        nullable=True,
    )

    preference = Column(
        "Preference",
        Unicode(100),
        nullable=True,
    )

    source_type = Column(
        "SourceType",
        Unicode(50),
        nullable=True,
    )