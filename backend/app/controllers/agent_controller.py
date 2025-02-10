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

    @agent_router.post("/knowledge-base/upload", status_code=HTTP_201_CREATED, operation_id="add_knowledge_base_document_post")
    async def add_knowledge_basedocument(self, document: UploadFile = File(...)) -> BaseResponse:
        if document.content_type != "application/pdf":
            raise HTTPException(status_code=400, detail="Only PDF files are allowed.")
        
        result = await self.agent_service.add_document(document, "knowledge-base")

        if result:
            return BaseResponse(status="success", message="The document has been added to the agent's knowledge base successfully.")
        else:
            raise HTTPException(status_code=500, detail="An error occurred while adding the document to the agent's knowledge base.")
        
    @agent_router.post("/knowledge-base/generate", status_code=HTTP_200_OK, operation_id="knowledge_base_generate_post")
    async def knowledge_base_generate(self, data: GenerateRequest) -> BaseResponse:
        result = self.agent_service.generate(data.prompt, _for="knowledge-base")

        if result:
            return BaseResponse(status="success", data={"response": result})
        else:
            raise HTTPException(status_code=500, detail="An error occurred while generating the response.")
        
    @agent_router.post("/superteam-member-agent/upload", status_code=HTTP_201_CREATED, operation_id="add_superteam_member_post")
    async def add_superteam_member_document(self, document: UploadFile = File(...)) -> BaseResponse:
        if document.content_type != "application/json":
            raise HTTPException(status_code=400, detail="Only JSON files are allowed.")
        
        result = await self.agent_service.add_document(document, "superteam-member")

        if result:
            return BaseResponse(status="success", message="The document has been added to the superteam member agent successfully.")
        else:
            raise HTTPException(status_code=500, detail="An error occurred while adding the document to the superteam member agent.")
        
    @agent_router.post("/superteam-member-agent/generate", status_code=HTTP_200_OK, operation_id="superteam_member_generate_post")
    async def superteam_member_generate(self, data: GenerateRequest) -> BaseResponse:
        result = self.agent_service.generate(data.prompt, "superteam-member")

        if result:
            return BaseResponse(status="success", data={"response": result})
        else:
            raise HTTPException(status_code=500, detail="An error occurred while generating the response.")



