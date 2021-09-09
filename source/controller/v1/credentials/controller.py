from abc import ABC
from abc import abstractmethod
from typing import Optional


class CredentialsController(ABC):
    """
    Main class for credentials work.
    All other workers must inherit from this class and implement all methods below.
    """

    def __init__(self):
        pass

    @abstractmethod
    def get(self, credential_id: int) -> Optional[str]:
        pass

    @abstractmethod
    def put(self, credential_data: str) -> int:
        pass

    @abstractmethod
    def delete(self, credential_id: int):
        pass
