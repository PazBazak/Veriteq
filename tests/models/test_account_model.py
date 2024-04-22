import pytest
from tests.fake_db import Account
from sqlalchemy.exc import IntegrityError

from tests.base import BaseTest


class TestAccount(BaseTest):

    @pytest.mark.parametrize("invalid_email", ["invalid_email", "valid@example.com", "", None])
    def test_email_validation(self, invalid_email):
        valid_account = Account(email="valid@example.com", auth_id="auth123")
        self.db.add(valid_account)
        self.db.commit()

        with pytest.raises(Exception):
            invalid_account = Account(email=invalid_email, auth_id="auth123")
            self.db.add(invalid_account)
            self.db.commit()

    def test_empty_auth_id(self):
        with pytest.raises(IntegrityError):
            incomplete_account = Account(email="valid@example.com", auth_id=None)
            self.db.add(incomplete_account)
            self.db.commit()
