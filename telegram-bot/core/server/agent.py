import typing as t

import dotenv
import os

from core.server.base import BaseAPIService
from core.helpers.api import ApiRouter

dotenv.load_dotenv()
API_URL = os.getenv("API_URL")


class AgentAPI(BaseAPIService):
    # types
    _for_type = t.Literal["knowledge-base", "superteam-member"]

    def __init__(self):
        super().__init__(
            service_name="agent",
            base_url=API_URL,
        )

    def generate(self, prompt: str, _for: _for_type) -> dict:
        try:
            self.check_rate_limit()
            data = {
                "prompt": prompt
            }

            if _for == "knowledge-base":
                response = self.post(ApiRouter.KNOWLEDGE_BASE_GENERATE, data=data)
            elif _for == "superteam-member":
                response = self.post(ApiRouter.SUPERTEAM_MEMBER_AGENT_GENERATE, data=data)
            else:
                raise ValueError("Invalid _for_type value")

            return response["data"]["response"]
        
        except Exception as e:
            return str(e)




