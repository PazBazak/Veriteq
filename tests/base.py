import pytest
from tests.fake_db import Account, Blockchain
from tests.consts import ACCOUNT_EMAIL


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
