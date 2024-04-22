import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from main import app  # Import your FastAPI app
from db.models.account import Account
from tests.base import BaseTest
from unittest.mock import MagicMock


class TestSignRouter(BaseTest):

    def test_sign_data_successful(self):
        # Prepare payload
        payload = {
            "hash": "8e60a80b015666bd707fac8a6b3b1f8d298b171b63d72a5fed44ccd5323035e3",
            "metadata": {"item_id": "1234"}
        }

        # Send POST request
        response = self.client.post("/sign/", json=payload)

        # Check response status code
        assert response.status_code == 200

        # Check response data
        data = response.json()
        assert 'transaction_id' in data
        assert 'blockchain' in data
        assert data['blockchain'] == "Polygon"
        assert 'timestamp' in data

    def test_sign_data_validation_error(self):
        # No hash or metadata provided
        payload = {}

        # Send POST request
        response = self.client.post("/sign/", json=payload)

        # Check response status code
        assert response.status_code == 422  # Validation error status code

    def test_sign_data_with_invalid_account(self, mocker):
        # Mock get_authenticated_account to return None or raise an exception
        mocker.patch('path.to.get_authenticated_account', side_effect=Exception("Unauthorized"))

        payload = {
            "hash": "abc123",
            "metadata": {"item_id": "5678"}
        }

        # Send POST request
        response = self.client.post("/sign/", json=payload)

        # Check response status code
        assert response.status_code == 401  # Unauthorized status code