from .controller import CredentialsController
from controller.v1.encryption import encrypt_string
from controller.v1.encryption import decrypt_string
from models.utils import get_db_session
from models import Secret

from typing import Optional


class SQLiteController(CredentialsController):

    def __init__(self):
        self.db_session = get_db_session()
        super(SQLiteController, self).__init__()

    def put(self, credential_data: str) -> int:
        encrypted_data = encrypt_string(credential_data)
        secret = Secret(secret=encrypted_data)
        self.db_session.add(secret)
        self.db_session.commit()
        return secret.id

    def get(self, credential_id: int) -> Optional[str]:
        row = self.db_session.query(Secret).filter_by(id=credential_id).first()
        return decrypt_string(row.secret)

    def delete(self, credential_id: int):
        self.db_session.query(Secret).filter_by(id=credential_id).delete()
