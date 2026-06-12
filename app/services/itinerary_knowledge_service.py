import os
from pathlib import Path

from sqlalchemy import text
from sqlalchemy.orm import Session
from langchain_community.vectorstores import FAISS

from app.ai.embedding_factory import get_embedding_function

from app.config import settings


class ItineraryKnowledgeService:
    def __init__(self, db: Session):
        self.db = db
        self.vector_db = self._load_vector_db()

    def _load_vector_db(self):
        vector_db_dir = Path(
            settings.VECTOR_DB_DIR
        )

        embedding_function = get_embedding_function()

        return FAISS.load_local(
            folder_path=str(vector_db_dir),
            embeddings=embedding_function,
            allow_dangerous_deserialization=True,
        )

    def build_itinerary_by_dates(
        self,
        date_list: list[str],
    ) -> list[dict]:

        itinerary_list = []
        search_plans = self._get_search_plans()

        for date in date_list:
            used_places = set()
            daily_schedules = []

            for plan in search_plans:
                results = self.vector_db.similarity_search_with_score(
                    query=plan["query"],
                    k=20,
                    fetch_k=100,
                    filter=plan["filter"],
                )

                selected_items = []

                for doc, score in results:
                    place_name = doc.metadata.get("place_name")
                    source_file = doc.metadata.get("source_file")

                    if not place_name or not source_file:
                        continue

                    # 同一天不要重複景點
                    if place_name in used_places:
                        continue

                    db_item = self._get_knowledge_item_by_source_file(
                        source_file=source_file,
                    )

                    if db_item is None:
                        continue

                    feature = db_item["feature"] or ""
                    selected_items.append(
                        {
                            "title": db_item["place_name"],
                            "content": feature[:30],
                            "preference": db_item["category"],
                            # "score": float(score),
                        }
                    )

                    used_places.add(place_name)

                    if len(selected_items) >= plan["k"]:
                        break

                daily_schedules.append(
                    {
                        "time": plan["time"],
                        "recommendations": selected_items,
                    }
                )

            itinerary_list.append(
                {
                    "date": date,
                    "schedules": daily_schedules,
                }
            )

        return itinerary_list

    def _get_search_plans(self) -> list[dict]:
        return [
            {
                "time": "09:00",
                "query": "適合早上開始的餐廳或早餐推薦，適合VIP客戶，交通方便",
                "filter": {"category": "餐廳美食"},
                "k": 1,
            },
            {
                "time": "11:00",
                "query": "適合上午安排的渡假村內外景點，行程不要太累，適合親子或家庭",
                "filter": None,
                "k": 2,
            },
            {
                "time": "13:00",
                "query": "適合午餐後安排的景點或室內活動，適合下午時段",
                "filter": None,
                "k": 2,
            },
            {
                "time": "15:00",
                "query": "適合下午茶、輕鬆散步、文化體驗或親子活動的景點",
                "filter": None,
                "k": 2,
            },
            {
                "time": "18:00",
                "query": "適合晚上用餐的餐廳推薦，適合VIP客戶與家庭旅客",
                "filter": {"category": "餐廳美食"},
                "k": 1,
            },
        ]

    def _get_knowledge_item_by_source_file(
        self,
        source_file: str,
    ) -> dict | None:

        sql = text("""
            SELECT
                PlaceName AS place_name,
                Category AS category,
                Feature AS feature
            FROM ResortKnowledgeItem
            WHERE SourceFile = :source_file
              AND IsActive = 1
        """)

        result = self.db.execute(
            sql,
            {
                "source_file": source_file,
            }
        ).mappings().first()

        if result is None:
            return None

        return dict(result)