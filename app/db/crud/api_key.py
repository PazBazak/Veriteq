import uuid
from datetime import datetime
from typing import Optional

from db.models.account import Account
from db.models.api_key import APIKey
from sqlalchemy import or_
from sqlalchemy.orm import Session
from utils.logger import get_logger

logger = get_logger(__name__)


def get_account_from_api_key(session: Session, api_key: str) -> Optional[Account]:
    api_key_as_uuid = uuid.UUID(api_key)

    now = datetime.utcnow()
    api_key_instance = (
        session.query(APIKey)
        .filter(APIKey.key == api_key_as_uuid, or_(APIKey.expired_at.is_(None), APIKey.expired_at > now))
        .first()
    )

    if api_key_instance:
        account: Account = api_key_instance.account
        logger.info(f"Verified api_key for account: {account.id}")
        return account

    logger.warning(f"Invalid API Key attempt - {api_key}")
