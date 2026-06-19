from uuid import uuid4

from sqlalchemy import text
from sqlalchemy.orm import Session
from app.services.nlp_service import nlp_service


class ItineraryRecommendationService:

    def __init__(self, db: Session):
        self.db = db

    def save_recommendation(
        self,
        customer_id: str,
        ai_result: dict,
        language: str
    ) -> str:

        recommendation_id = str(uuid4())

        summary_translated_reply = nlp_service.translate_reply(
            text=ai_result.get("summary"),
            target_language=language,
        )

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
                "summary": summary_translated_reply,
            },
        )

        for day in ai_result.get("itinerary", []):

            schedule_date = day["date"]

            for schedule in day.get("schedules", []):
                title_translated_reply = nlp_service.translate_reply(
                    text=schedule["title"],
                    target_language=language,
                )
                content_translated_reply = nlp_service.translate_reply(
                    text=schedule["content"],
                    target_language=language,
                )

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
                        "title": title_translated_reply,
                        "content": content_translated_reply,
                        "preference": schedule.get("preference"),
                        "source_type": schedule.get("source_type"),
                    },
                )

        self.db.commit()

        return recommendation_id