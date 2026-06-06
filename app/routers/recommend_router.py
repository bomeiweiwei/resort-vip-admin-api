from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies.auth_dependency import get_current_user
from app.schemas.recommend_schema import (
    ItineraryRecommendationResponse,
    ItineraryScheduleResponse,
)
from app.services.recommend_service import RecommendService

router = APIRouter()


@router.get(
    "/itinerary",
    response_model=list[ItineraryRecommendationResponse],
)
def get_itinerary_recommendations(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    service = RecommendService(db)
    return service.get_itinerary_recommendations()

@router.get(
    "/itinerary/{customer_id}/{recommendation_id}/schedules",
    response_model=list[ItineraryScheduleResponse],
)
def get_itinerary_schedules(
    customer_id: str,
    recommendation_id: str,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    service = RecommendService(db)

    return service.get_itinerary_schedules(
        customer_id=customer_id,
        recommendation_id=recommendation_id,
    )