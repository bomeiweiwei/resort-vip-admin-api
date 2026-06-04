from uuid import uuid4

from sqlalchemy import text
from sqlalchemy.orm import Session


class ItineraryRecommendationService:

    def __init__(self, db: Session):
        self.db = db

    def save_recommendation(
        self,
        customer_id: str,
        ai_result: dict,
    ) -> str:

        recommendation_id = str(uuid4())

        self.db.execute(
            text("""
                INSERT INTO VipItineraryRecommendation
                (
                    RecommendationId,
                    CustomerId,
                    Summary
                )
                VALUES
                (
                    :recommendation_id,
                    :customer_id,
                    :summary
                )
            """),
            {
                "recommendation_id": recommendation_id,
                "customer_id": customer_id,
                "summary": ai_result.get("summary"),
            },
        )

        for day in ai_result.get("itinerary", []):

            schedule_date = day["date"]

            for schedule in day.get("schedules", []):

                self.db.execute(
                    text("""
                        INSERT INTO VipItinerarySchedule
                        (
                            RecommendationId,
                            ScheduleDate,
                            ScheduleTime,
                            Title,
                            Content,
                            Preference,
                            SourceType
                        )
                        VALUES
                        (
                            :recommendation_id,
                            :schedule_date,
                            :schedule_time,
                            :title,
                            :content,
                            :preference,
                            :source_type
                        )
                    """),
                    {
                        "recommendation_id": recommendation_id,
                        "schedule_date": schedule_date,
                        "schedule_time": schedule["time"],
                        "title": schedule["title"],
                        "content": schedule["content"],
                        "preference": schedule.get("preference"),
                        "source_type": schedule.get("source_type"),
                    },
                )

        self.db.commit()

        return recommendation_id