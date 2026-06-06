from sqlalchemy.orm import Session

from app.models.customer_model import Customer
from app.models.vip_itinerary_recommendation_model import VipItineraryRecommendation
from app.models.vip_itinerary_schedule_model import VipItinerarySchedule

class RecommendService:
    def __init__(self, db: Session):
        self.db = db

    def get_itinerary_recommendations(self):
        rows = (
            self.db.query(
                Customer.customer_id,
                Customer.full_name,
                VipItineraryRecommendation.recommendation_id,
                VipItineraryRecommendation.summary,
            )
            .join(
                Customer,
                VipItineraryRecommendation.customer_id == Customer.customer_id,
            )
            .order_by(VipItineraryRecommendation.created_at.desc())
            .all()
        )

        return [
            {
                "customer_id": str(row.customer_id),
                "full_name": row.full_name,
                "recommendation_id": str(row.recommendation_id),
                "summary": row.summary,
            }
            for row in rows
        ]
    
    def get_itinerary_schedules(
        self,
        customer_id: str,
        recommendation_id: str,
    ):
        rows = (
            self.db.query(
                VipItinerarySchedule.schedule_id,
                VipItinerarySchedule.recommendation_id,
                VipItinerarySchedule.schedule_date,
                VipItinerarySchedule.schedule_time,
                VipItinerarySchedule.title,
                VipItinerarySchedule.content,
                VipItinerarySchedule.preference,
                VipItinerarySchedule.source_type,
            )
            .join(
                VipItineraryRecommendation,
                VipItinerarySchedule.recommendation_id
                == VipItineraryRecommendation.recommendation_id,
            )
            .filter(
                VipItineraryRecommendation.customer_id
                == customer_id,
                VipItinerarySchedule.recommendation_id
                == recommendation_id,
            )
            .order_by(
                VipItinerarySchedule.schedule_date.desc(),
                VipItinerarySchedule.schedule_time,
            )
            .all()
        )

        return [
            {
                "schedule_id": str(row.schedule_id),
                "recommendation_id": str(
                    row.recommendation_id
                ),
                "schedule_date": row.schedule_date.strftime(
                    "%Y-%m-%d"
                ),
                "schedule_time": row.schedule_time,
                "title": row.title,
                "content": row.content,
                "preference": row.preference,
                "source_type": row.source_type,
            }
            for row in rows
        ]