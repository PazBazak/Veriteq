from datetime import datetime

from db.models.account import Account
from db.models.api_key import APIKey
from sqlalchemy.orm import Session

from utils.logger import get_logger

logger = get_logger(__name__)


def get_account_from_api_key(session: Session, api_key: str) -> Account:
    """
    Retrieve the account associated with the given API key.
    """
    now = datetime.utcnow()
    api_key_instance = session.query(APIKey).filter(
        APIKey.key == api_key,
        (APIKey.expired_at is None) | (APIKey.expired_at > now)
    ).first()

    if api_key_instance:
        account: Account = api_key_instance.account
        logger.info(f"Verified api_key for account: {account.id}")
        return account

    logger.warning(f"Invalid API Key attempt - {api_key}")

