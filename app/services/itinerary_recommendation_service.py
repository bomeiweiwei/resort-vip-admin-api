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

        # 先一次查出景點經緯度與地址
        knowledge_items = self.db.execute(
            text("""
                SELECT
                    PlaceName,
                    Latitude,
                    Longitude,
                    Address,
                    PicUrl
                FROM ResortKnowledgeItem
                WHERE IsActive = 1
            """)
        ).mappings().all()

        knowledge_map = {
            item["PlaceName"]: item
            for item in knowledge_items
        }

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
                original_title = schedule["title"]

                knowledge_item = knowledge_map.get(original_title)

                # 如果找不到對應景點，給綠舞渡假村預設值，避免 NOT NULL 欄位寫入失敗
                latitude = knowledge_item["Latitude"] if knowledge_item else 24.702904
                longitude = knowledge_item["Longitude"] if knowledge_item else 121.818930
                address = knowledge_item["Address"] if knowledge_item else "宜蘭縣五結鄉錦眾村五濱路二段459號"
                picurl = knowledge_item["PicUrl"] if knowledge_item else "/static/images/empty.png"

                title_translated_reply = nlp_service.translate_reply(
                    text=original_title,
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
                            SourceType,
                            Latitude,
                            Longitude,
                            Address,
                            PicUrl
                        )
                        VALUES
                        (
                            :recommendation_id,
                            :schedule_date,
                            :schedule_time,
                            :title,
                            :content,
                            :preference,
                            :source_type,
                            :latitude,
                            :longitude,
                            :address,
                            :picurl
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
                        "latitude": latitude,
                        "longitude": longitude,
                        "address": address,
                        "picurl": picurl
                    },
                )

        self.db.commit()

        return recommendation_id