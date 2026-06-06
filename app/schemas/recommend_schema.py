from pydantic import BaseModel


class ItineraryRecommendationResponse(BaseModel):
    customer_id: str
    full_name: str
    recommendation_id: str
    summary: str | None = None

class ItineraryScheduleResponse(BaseModel):
    schedule_id: str
    recommendation_id: str
    schedule_date: str
    schedule_time: str
    title: str
    content: str | None
    preference: str | None
    source_type: str | None