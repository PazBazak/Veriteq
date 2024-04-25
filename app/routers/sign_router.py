import uuid
from datetime import datetime
from typing import Any

from auth import get_authenticated_account
from blockchain_dal.consts import SupportedBlockchains
from db.models.account import Account
from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field, model_validator
from utils.logger import get_logger

logger = get_logger(__name__)

router = APIRouter(prefix="/sign", tags=["Data Signing"])


class SignData(BaseModel):
    hash: str = Field(default=None, example="8e60a80b015666bd707fac8a6b3b1f8d298b171b63d72a5fed44ccd5323035e3")
    metadata: dict = Field(default=None, example={"item_id": "1234"})
    blockchain: SupportedBlockchains = Field(..., description="The blockchain to use for the transaction")

    # noinspection PyNestedDecorators
    @model_validator(mode="before")
    @classmethod
    def check_card_number_omitted(cls, data: Any) -> Any:
        if not any([data.get("metadata"), data.get("hash")]):
            raise ValueError("Either hash or metadata must be provided")

        return data


class SignDataResponse(BaseModel):
    transaction_id: str
    blockchain: str
    timestamp: str


async def mock_blockchain_store(data: dict) -> dict:
    transaction_id = str(uuid.uuid4())
    blockchain_timestamp = datetime.utcnow().isoformat()

    logger.info(f"Signed data, created a blockchain transaction - {transaction_id}, at {blockchain_timestamp}")

    return {"transaction_id": transaction_id, "blockchain": data.get("blockchain"), "timestamp": blockchain_timestamp}


@router.post("/", response_model=SignDataResponse)
async def sign_data(data: SignData, account: Account = Depends(get_authenticated_account)) -> SignDataResponse:
    logger.info(f"Request received to sign {data}")

    blockchain_response = await mock_blockchain_store(data.dict())

    return SignDataResponse(
        transaction_id=blockchain_response["transaction_id"],
        blockchain=blockchain_response["blockchain"],
        timestamp=blockchain_response["timestamp"],
    )
