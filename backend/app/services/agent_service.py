from typing import List, Tuple
import dotenv
import os

from fastapi import UploadFile
from langchain_ollama.llms import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
from langchain.schema.runnable import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

from app.core.vectorstore import VectorStore
from app.core.document.pdf_document import PDFDocumentHandler
from app.helpers.prompts import KNOWLEDGE_BASE_PROMPT, KNOWLEDGE_BASE_SYSTEM_PROMPT


dotenv.load_dotenv()


class AgentService:
    def __init__(self):
        self.pdf_document_handler = PDFDocumentHandler()
        self.knowledge_base_vectorstore = VectorStore(vectorstore_path=os.getenv("KNOWLEDGE_BASE_VECTORSTORE_PATH"))
        self.llm = OllamaLLM(
            model=os.getenv("LLM_MODEL"),
        )

    async def add_document(self, document: UploadFile) -> bool:
        text = await self.pdf_document_handler.handle(document)
        result = self.knowledge_base_vectorstore.load_data(text)

        return result
    
    def generate(self, prompt: str) -> str:
        retriever = self.knowledge_base_vectorstore.retriever()
        template = ChatPromptTemplate.from_messages([
            ("system", KNOWLEDGE_BASE_SYSTEM_PROMPT),
            ("human", KNOWLEDGE_BASE_PROMPT),
        ])

        rag_chain = (
            {"context": retriever, "question": RunnablePassthrough()}
            | template
            | self.llm
            | StrOutputParser()
        )

        response = rag_chain.invoke(prompt)
        return response


