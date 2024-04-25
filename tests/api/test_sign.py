import pytest
from blockchain_dal.consts import SupportedBlockchains

from tests.base import BaseTest


class TestSignRouter(BaseTest):

    @pytest.mark.parametrize(
        "payload",
        [
            {
                "hash": "8e60a80b015666bd707fac8a6b3b1f8d298b171b63d72a5fed44ccd5323035e3",
                "blockchain": SupportedBlockchains.Ethereum.value,
            },
            {"metadata": {"item_id": "1234"}, "blockchain": SupportedBlockchains.Ethereum.value},
            {
                "hash": "8e60a80b015666bd707fac8a6b3b1f8d298b171b63d72a5fed44ccd5323035e3",
                "metadata": {"item_id": "1234"},
                "blockchain": SupportedBlockchains.Ethereum.value,
            },
        ],
        ids=["hash only", "metadata only", "metadata and hash"],
    )
    def test_successful(self, authenticated_api_key, payload):
        response = self.client.post(
            "/api/latest/sign/", json=payload, headers={"X-API-Key": str(authenticated_api_key.key)}
        )

        assert response.status_code == 200

        data = response.json()

        assert "transaction_id" in data
        assert data["blockchain"] == SupportedBlockchains.Ethereum.value
        assert "timestamp" in data

    @pytest.mark.parametrize(
        "invalid_payload",
        [
            {},
            {"metadata": "not dict", "blockchain": SupportedBlockchains.Ethereum.value},
            {
                "metadata": {"item_id": "1234"},
                "hash": "8e60a80b015666bd707fac8a6b3b1f8d298b171b63d72a5fed44ccd5323035e3",
            },
        ],
        ids=["Empty", "Invalid metadata", "Missing blockchain"],
    )
    def test_validation_error(self, authenticated_api_key, invalid_payload):
        response = self.client.post(
            "/api/latest/sign/", json=invalid_payload, headers={"X-API-Key": str(authenticated_api_key.key)}
        )

        assert response.status_code == 422  # Validation error status code  todo - use constants

    def test_unauthenticated_fails(self):
        payload = {
            "hash": "8e60a80b015666bd707fac8a6b3b1f8d298b171b63d72a5fed44ccd5323035e3",
            "metadata": {"item_id": "1234"},
        }

        response = self.client.post("/api/latest/sign/", json=payload)

        assert response.status_code == 403
