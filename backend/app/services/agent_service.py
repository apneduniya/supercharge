import typing as t
import dotenv
import os

from fastapi import UploadFile
from langchain_ollama.llms import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
from langchain.schema.runnable import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

from app.core.vectorstore import VectorStore
from app.core.document.pdf_document import PDFDocumentHandler
from app.core.document.json_document import JSONDocumentHandler
from app.helpers.prompts import KNOWLEDGE_BASE_PROMPT, KNOWLEDGE_BASE_SYSTEM_PROMPT, SUPERTEAM_MEMBER_PROMPT, SUPERTEAM_MEMBER_SYSTEM_PROMPT


dotenv.load_dotenv()


class AgentService:
    # types
    _for_type = t.Literal["knowledge-base", "superteam-member"]

    def __init__(self):
        self.pdf_document_handler = PDFDocumentHandler()
        self.json_document_handler = JSONDocumentHandler()
        self.knowledge_base_vectorstore = VectorStore(vectorstore_path=os.getenv("KNOWLEDGE_BASE_VECTORSTORE_PATH"))
        self.superteam_member_vectorstore = VectorStore(vectorstore_path=os.getenv("SUPERTEAM_MEMBER_VECTORSTORE_PATH"))

        self.llm = OllamaLLM(
            model=os.getenv("LLM_MODEL"),
        )

    async def add_document(self, document: UploadFile, _for: _for_type) -> bool:
        match _for:
            case "knowledge-base":
                text_data = await self.pdf_document_handler.handle(document)
                result = self.knowledge_base_vectorstore.load_data(text_data, file_type="text")
            case "superteam-member":
                json_data = await self.json_document_handler.handle(document)
                result = self.superteam_member_vectorstore.load_data(json_data, file_type="json")
            case _:
                raise ValueError("Invalid value for _for")

        return result
    
    def generate(self, prompt: str, _for: _for_type) -> str:
        match _for:
            case "knowledge-base":
                retriever = self.knowledge_base_vectorstore.retriever()
                template = ChatPromptTemplate.from_messages([
                    ("system", KNOWLEDGE_BASE_SYSTEM_PROMPT),
                    ("human", KNOWLEDGE_BASE_PROMPT),
                ])
            case "superteam-member":
                retriever = self.superteam_member_vectorstore.retriever(top_k=10)
                template = ChatPromptTemplate.from_messages([
                    ("system", SUPERTEAM_MEMBER_SYSTEM_PROMPT),
                    ("human", SUPERTEAM_MEMBER_PROMPT),
                ])
            case _:
                raise ValueError("Invalid value for _for")

        rag_chain = (
            {"context": retriever, "question": RunnablePassthrough()}
            | template
            | self.llm
            | StrOutputParser()
        )

        response = rag_chain.invoke(prompt)
        return response


