from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.routers.employee_router import router as employee_router
from app.routers.auth_router import router as auth_router
from app.routers.checkin_router import router as checkin_router


app = FastAPI(
    title=settings.APP_NAME,
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        settings.FRONTEND_ORIGIN,
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(
    auth_router,
    prefix="/api/auth",
    tags=["Auth"],
)

app.include_router(
    employee_router,
    prefix="/api/employees",
    tags=["Employees"],
)

app.include_router(
    checkin_router,
    prefix="/api/checkins",
    tags=["CheckIn"],
)


@app.get("/")
def root():
    return {
        "message": "Resort VIP Admin API is running",
        "env": settings.APP_ENV,
    }