from fastapi import UploadFile
import fitz
from app.core.document.base import DocumentHandler


class PDFDocumentHandler(DocumentHandler):
    async def handle(self, document: UploadFile) -> str:
        contents = await document.read()
        pdf_document = fitz.open(stream=contents, filetype="pdf")
        text = ""
        for page_num in range(pdf_document.page_count):
            page = pdf_document.load_page(page_num)
            text += page.get_text()
        return text