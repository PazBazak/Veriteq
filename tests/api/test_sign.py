from tests.base import BaseTest


class TestSignRouter(BaseTest):

    def test_sign_data_successful(self, authenticated_api_key):
        payload = {
            "hash": "8e60a80b015666bd707fac8a6b3b1f8d298b171b63d72a5fed44ccd5323035e3",
            "metadata": {"item_id": "1234"},
        }

        response = self.client.post(
            "/api/latest/sign/", json=payload, headers={"X-API-Key": str(authenticated_api_key.key)}
        )

        assert response.status_code == 200

        data = response.json()

        assert "transaction_id" in data
        assert data["blockchain"] == "Polygon"
        assert "timestamp" in data

    def test_sign_data_validation_error(self):
        # No hash or metadata provided
        payload = {}

        # Send POST request
        response = self.client.post("/sign/", json=payload)

        # Check response status code
        assert response.status_code == 422  # Validation error status code

    def test_sign_data_with_invalid_account(self, mocker):
        # Mock get_authenticated_account to return None or raise an exception
        mocker.patch("path.to.get_authenticated_account", side_effect=Exception("Unauthorized"))

        payload = {"hash": "abc123", "metadata": {"item_id": "5678"}}

        # Send POST request
        response = self.client.post("/sign/", json=payload)

        # Check response status code
        assert response.status_code == 401  # Unauthorized status code
