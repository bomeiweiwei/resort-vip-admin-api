from sqlalchemy import Column, DateTime, ForeignKey, UnicodeText
from sqlalchemy.dialects.mssql import UNIQUEIDENTIFIER
from sqlalchemy.orm import relationship

from app.database import Base


class VipItineraryRecommendation(Base):
    __tablename__ = "VipItineraryRecommendation"

    recommendation_id = Column(
        "RecommendationId",
        UNIQUEIDENTIFIER,
        primary_key=True,
        nullable=False,
    )

    customer_id = Column(
        "CustomerId",
        UNIQUEIDENTIFIER,
        ForeignKey("Customer.CustomerId"),
        nullable=False,
    )

    summary = Column(
        "Summary",
        UnicodeText,
        nullable=True,
    )

    created_at = Column(
        "CreatedAt",
        DateTime,
        nullable=False,
    )