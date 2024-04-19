import pytest
from tests.fake_db import Account
from sqlalchemy.exc import IntegrityError

from tests.base import BaseTest


class TestAccount(BaseTest):

    def test_email_validation(self):
        valid_account = Account(email="valid@example.com", auth_id="auth123")
        self.db.add(valid_account)
        self.db.commit()

        with pytest.raises(AssertionError):
            invalid_account = Account(email="invalidemail", auth_id="auth124")
            self.db.add(invalid_account)
            self.db.commit()

    def test_unique_email_constraint(self):
        account1 = Account(email="unique@example.com", auth_id="auth125")
        self.db.add(account1)
        self.db.commit()

        account2 = Account(email="unique@example.com", auth_id="auth126")
        self.db.add(account2)
        with pytest.raises(IntegrityError):
            self.db.commit()

    def test_non_nullable_fields(self):
        with pytest.raises(IntegrityError):
            incomplete_account = Account(email="test2@example.com")  # Missing auth_id
            self.db.add(incomplete_account)
            self.db.commit()

    def test_timestamps_on_create_and_update(self):
        account = Account(email="time@example.com", auth_id="auth127")
        self.db.add(account)
        self.db.commit()

        initial_created_at = account.created_at
        initial_updated_at = account.updated_at

        # Simulate an update
        account.email = "timeupdate@example.com"
        self.db.commit()

        assert account.created_at == initial_created_at
        assert account.updated_at > initial_updated_at
