import datetime
from uuid import uuid4

import pytest
from sqlalchemy.exc import IntegrityError

from tests.base import BaseTest
from db.models import APIKey


class TestAPIKey(BaseTest):

    def test_create_api_key(self, account):
        new_api_key = APIKey(
            account_id=account.id,
        )
        self.db.add(new_api_key)
        self.db.commit()

        api_key = self.db.query(APIKey).filter_by(account_id=account.id).first()
        assert api_key is not None
        assert api_key.key is not None
        assert api_key.account == account

    def test_unique_key_constraint(self, account):
        key_value = uuid4()

        api_key1 = APIKey(account_id=account.id, key=key_value)
        self.db.add(api_key1)
        self.db.commit()

        with pytest.raises(IntegrityError):
            api_key2 = APIKey(account_id=account.id, key=key_value)
            self.db.add(api_key2)
            self.db.commit()

    def test_api_key_expiration_handling(self, account):
        expired_key = APIKey(account_id=account.id, expired_at=datetime.datetime.now() - datetime.timedelta(days=1))
        active_key = APIKey(account_id=account.id, expired_at=None)
        self.db.add(expired_key)
        self.db.add(active_key)
        self.db.commit()

        fetched_expired_key = self.db.query(APIKey).filter_by(id=expired_key.id).first()
        fetched_active_key = self.db.query(APIKey).filter_by(id=active_key.id).first()

        assert fetched_expired_key.expired_at < datetime.datetime.now()
        assert fetched_active_key.expired_at is None
