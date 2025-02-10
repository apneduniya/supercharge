import typing as t

from langchain_core.documents import Document
from langchain_community.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.embeddings import Embeddings
import dotenv
import os
import json

from app.helpers.supeteam_member_json_structure import generate_member_metadata, generate_member_content


dotenv.load_dotenv()


class VectorStore:
    file_type_type = t.Literal["json", "text"]

    def __init__(self, embeddings: Embeddings = None, vectorstore_path: str = None):
        self.embeddings = embeddings or HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"  # Lightweight, fast
        )
        self.vectorstore_path = vectorstore_path
        if not self.vectorstore_path:
            raise ValueError("Vectorstore path is required")

    def load_data(self, content: str | dict, file_type: file_type_type = "text") -> bool:
        try:
            if file_type == "text":
                document = Document(page_content=content)

                text_splitter = RecursiveCharacterTextSplitter()
                splits = text_splitter.split_documents([document])

                vectorstore = FAISS.from_documents(splits, self.embeddings)
                vectorstore.save_local(self.vectorstore_path)
                
            elif file_type == "json":
                documents = []

                for person in content:
                    document = Document(
                        page_content=generate_member_content(person),
                        metadata=generate_member_metadata(person)
                    )
                    documents.append(document)
                
                vector_store = FAISS.from_documents(documents, self.embeddings)
                vector_store.save_local(self.vectorstore_path)

            else:
                raise ValueError(f"Unsupported file type: {file_type}")

            return True

        except Exception as e:
            print(f"Error in loading data in vector store: {e}")  # Improved error message
            return False

    def load_knowledge_base(self) -> FAISS:
        try:
            db = FAISS.load_local(
                self.vectorstore_path, self.embeddings, allow_dangerous_deserialization=True)
            return db

        except Exception as e:
            raise e

    def retriever(self, top_k: int = 5):
        try:
            db = self.load_knowledge_base()
            retriever = db.as_retriever(
                search_type="similarity",  # Default search type
                search_kwargs={"k": top_k}  # Number of documents to retrieve
            )

            return retriever

        except Exception as e:
            raise e
        
    def similarity_search(self, query: str, top_k: int = 5):
        try:
            db = self.load_knowledge_base()
            retriever = db.as_retriever(
                search_type="similarity",
                search_kwargs={"k": top_k}
            )

            results = retriever.search(query)
            return results

        except Exception as e:
            raise e
