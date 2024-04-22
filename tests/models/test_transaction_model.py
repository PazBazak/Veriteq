from tests.fake_db import Transaction, TransactionStatus
from uuid import uuid4
import datetime
from tests.base import BaseTest


class TestTransaction(BaseTest):
    def test_create_transaction(self, account, blockchain):
        blockchain_tx = str(uuid4())
        new_transaction = Transaction(
            blockchain_tx_id=blockchain_tx,
            status=TransactionStatus.PENDING,
            account_id=account.id,
            blockchain_id=blockchain.id,
            timestamp=datetime.datetime.now()
        )
        self.db.add(new_transaction)
        self.db.commit()

        transaction = self.db.query(Transaction).filter_by(status=TransactionStatus.PENDING).first()
        assert transaction is not None
        assert transaction.status == TransactionStatus.PENDING
        assert transaction.blockchain_tx_id == blockchain_tx

