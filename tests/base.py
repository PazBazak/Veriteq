import pytest


class BaseTest:

    @pytest.fixture(autouse=True)
    def setup_method(self, fake_db):
        self.db = fake_db
