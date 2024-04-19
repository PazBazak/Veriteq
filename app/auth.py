from db.crud.api_key import get_account_from_api_key
from db.database import Session, get_db
from fastapi import Depends, HTTPException, Security, status
from fastapi.security import APIKeyHeader

api_key_header = APIKeyHeader(name="X-API-Key")


def get_authenticated_account(session: Session = Depends(get_db), api_key_header_value: str = Security(api_key_header)):
    if account := get_account_from_api_key(session, api_key_header_value):
        return account

    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing or invalid API key")
