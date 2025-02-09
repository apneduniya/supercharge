from abc import ABC, abstractmethod
from fastapi import UploadFile


class DocumentHandler(ABC):
    @abstractmethod
    async def handle(self, document: UploadFile) -> str:
        pass