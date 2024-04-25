import uuid

import pytest

from tests.consts import ACCOUNT_EMAIL
from tests.fake_db import Account, APIKey, Blockchain


class BaseTest:

    @pytest.fixture(autouse=True)
    def setup_method(self, fake_db, fake_client):
        self.db = fake_db
        self.client = fake_client

    @pytest.fixture()
    def account(self):
        account = Account(email=ACCOUNT_EMAIL, auth_id="auth123")
        self.db.add(account)
        self.db.commit()
        yield account

    @pytest.fixture()
    def blockchain(self):
        blockchain = Blockchain(name="Ethereum")
        self.db.add(blockchain)
        self.db.commit()
        yield blockchain

    @pytest.fixture()
    def authenticated_api_key(self, account):
        api_key = APIKey(account_id=account.id, key=uuid.uuid4())
        self.db.add(api_key)
        self.db.commit()
        yield api_key
