from langchain_core.documents import Document
from langchain_community.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.embeddings import Embeddings
import dotenv
import os


dotenv.load_dotenv()


class VectorStore:
    def __init__(self, embeddings: Embeddings = None, vectorstore_path: str = None):
        self.embeddings = embeddings or HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"  # Lightweight, fast
        )
        self.vectorstore_path = vectorstore_path
        if not self.vectorstore_path:
            raise ValueError("Vectorstore path is required")

    def load_data(self, text: str) -> bool:
        try:
            document = Document(page_content=text)

            text_splitter = RecursiveCharacterTextSplitter()
            splits = text_splitter.split_documents([document])

            vectorstore = FAISS.from_documents(splits, self.embeddings)

            vectorstore.save_local(self.vectorstore_path)
            return True

        except Exception as e:
            print(e)
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
