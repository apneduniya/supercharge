from fastapi import UploadFile
import json
from app.core.document.base import DocumentHandler


class JSONDocumentHandler(DocumentHandler):
    async def handle(self, document: UploadFile) -> dict:
        contents = await document.read()
        return json.loads(contents)
