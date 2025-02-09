from typing import List

from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi_restful.cbv import cbv
from starlette.status import HTTP_201_CREATED, HTTP_204_NO_CONTENT, HTTP_200_OK

from app.models.base import BaseResponse
from app.models.agent import GenerateRequest
from app.services.agent_service import AgentService


agent_router = APIRouter()


@cbv(agent_router)
class AgentController:
    def __init__(self):
        self.agent_service = AgentService()

    @agent_router.post("/knowledge-base/upload", status_code=HTTP_201_CREATED, operation_id="add_document_post")
    async def add_document(self, document: UploadFile = File(...)) -> BaseResponse:
        if document.content_type != "application/pdf":
            raise HTTPException(status_code=400, detail="Only PDF files are allowed.")
        
        result = await self.agent_service.add_document(document)

        if result:
            return BaseResponse(status="success", message="The document has been added to the agent's knowledge base successfully.")
        else:
            raise HTTPException(status_code=500, detail="An error occurred while adding the document to the agent's knowledge base.")
        
    @agent_router.post("/generate", status_code=HTTP_200_OK, operation_id="generate_post")
    async def generate(self, data: GenerateRequest) -> BaseResponse:
        result = self.agent_service.generate(data.prompt)

        if result:
            return BaseResponse(status="success", data={"response": result})
        else:
            raise HTTPException(status_code=500, detail="An error occurred while generating the response.")



