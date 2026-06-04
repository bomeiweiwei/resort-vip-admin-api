from datetime import datetime, timedelta, time
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.customer_model import Customer
from app.models.room_model import Room, RoomType
from app.models.booking_stay_model import BookingStay, BookingStayNote
from app.schemas.checkin_schema import CheckInCreateRequest

from app.models.customer_vip_account_model import CustomerVipAccount
from app.utils.account_generator import generate_login_account, generate_initial_password
from app.utils.security import get_password_hash

from app.services.vip_prompt_service import VipPromptService

import json
from app.prompts.prompt_builder import build_vip_system_prompt, build_vip_user_prompt

from app.services.itinerary_knowledge_service import ItineraryKnowledgeService
from app.utils.date_helper import build_date_list

class CheckInService:
    def __init__(self, db: Session):
        self.db = db

    def get_room_types(self):
        return (
            self.db.query(RoomType)
            .filter(RoomType.is_active == True)
            .order_by(RoomType.room_type_id)
            .all()
        )

    def get_rooms_by_room_type(self, room_type_id: int):
        return (
            self.db.query(Room)
            .filter(Room.room_type_id == room_type_id)
            .filter(Room.is_active == True)
            .order_by(Room.room_no)
            .all()
        )
    
    def _generate_unique_vip_account(self) -> str:
        for _ in range(10):
            account = generate_login_account()

            exists = (
                self.db.query(CustomerVipAccount)
                .filter(CustomerVipAccount.login_account == account)
                .first()
            )

            if exists is None:
                return account

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="VIP帳號產生失敗，請重試",
        )

    def create_checkin(self, request: CheckInCreateRequest):
        if request.check_out_date <= request.check_in_date:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="退房日期必須晚於入住日期",
            )

        room = (
            self.db.query(Room)
            .filter(Room.room_id == request.room_id)
            .filter(Room.room_type_id == request.room_type_id)
            .filter(Room.is_active == True)
            .first()
        )

        if room is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="房型與房號不符合或房間不存在",
            )

        now = datetime.now()

        customer = Customer(
            full_name=request.full_name,
            gender_id=request.gender_id,
            birth_date=request.birth_date,
            country_code=request.country_code,
            mobile_phone=request.mobile_phone,
            phone=request.phone,
            email=request.email,
            created_at=now,
            updated_at=now,
        )

        self.db.add(customer)
        self.db.flush()

        booking = BookingStay(
            customer_id=customer.customer_id,
            room_id=request.room_id,
            check_in_date=request.check_in_date,
            check_out_date=request.check_out_date,
            adult_count=request.adult_count,
            child_count=request.child_count,
            has_parking=request.has_parking,
            license_plate_no=request.license_plate_no,
            created_at=now,
            updated_at=now,
        )

        self.db.add(booking)
        self.db.flush()

        for note in request.notes:
            if note.note_content.strip():
                self.db.add(
                    BookingStayNote(
                        booking_stay_id=booking.booking_stay_id,
                        note_type=note.note_type,
                        note_content=note.note_content,
                        created_at=now,
                    )
                )

        vip_login_account = self._generate_unique_vip_account()
        vip_initial_password = generate_initial_password()

        expire_at = datetime.combine(
            request.check_out_date + timedelta(days=1),
            time(23, 59, 59),
        )

        # 1. 建立 VIP check-in 資料
        vip_account = CustomerVipAccount(
            customer_id=customer.customer_id,
            login_account=vip_login_account,
            password_hash=get_password_hash(vip_initial_password),
            is_active=True,
            expire_at=expire_at,
            updated_at=now,
        )

        self.db.add(vip_account)
        self.db.flush()

        # 2. 取得 SQL 組 prompt 所需資料
        prompt_service = VipPromptService(self.db)

        prompt_data = prompt_service.get_customer_prompt_data(
            str(customer.customer_id)
        )

        date_list = build_date_list(
            check_in_date=prompt_data["check_in_date"],
            stay_days=prompt_data["stay_days"],
        )

        # 3. 根據客戶與住宿資料，查詢向量資料庫
        itinerary_knowledge_service = ItineraryKnowledgeService(self.db)

        knowledge_context = itinerary_knowledge_service.build_itinerary_by_dates(
            date_list=date_list,
        )

        # 4. 組 prompt
        system_prompt = build_vip_system_prompt()

        user_prompt = build_vip_user_prompt(
            data=prompt_data,
            knowledge_context=json.dumps(
                knowledge_context,
                ensure_ascii=False,
                indent=2,
                default=str,
            ),
        )

        print("========== system_prompt ==========")
        print(system_prompt)

        print("========== user_prompt ==========")
        print(user_prompt)

        
        self.db.commit()

        return {
            "customer_id": str(customer.customer_id),
            "booking_stay_id": str(booking.booking_stay_id),
        }