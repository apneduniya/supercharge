import dotenv
import os

from core.server.base import BaseAPIService
from core.helpers.api import ApiRouter

dotenv.load_dotenv()
API_URL = os.getenv("API_URL")


class AgentAPI(BaseAPIService):
    def __init__(self):
        super().__init__(
            service_name="agent",
            base_url=API_URL,
        )

    def generate(self, prompt: str) -> dict:
        try:
            self.check_rate_limit()
            data = {
                "prompt": prompt
            }

            response = self.post(ApiRouter.GENERATE, data=data)
            return response["data"]["response"]
        
        except Exception as e:
            return str(e)




