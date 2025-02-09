from typing import Optional
from pydantic import BaseModel


class GenerateRequest(BaseModel):
    prompt: str



