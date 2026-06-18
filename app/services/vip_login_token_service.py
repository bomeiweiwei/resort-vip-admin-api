import secrets
from datetime import datetime, timedelta

from app.models.customer_vip_login_token_model import (
    CustomerVipLoginToken,
)

from app.utils.security import get_password_hash


class VipLoginTokenService:

    @staticmethod
    def create_token(
        db,
        customer_vip_account_id,
    ) -> str:

        plain_token = secrets.token_urlsafe(48)

        token_hash = get_password_hash(
            plain_token
        )

        db_token = CustomerVipLoginToken(
            customer_vip_account_id=customer_vip_account_id,
            token_hash=token_hash,
            expire_at=datetime.now() + timedelta(hours=1),
            created_at=datetime.now(),
        )

        db.add(db_token)

        return plain_token