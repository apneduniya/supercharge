import typing as t
from pydantic import BaseModel


class BaseResponse(BaseModel):
    status: t.Literal["success", "error"]
    message: t.Optional[str] = None
    data: t.Optional[t.Dict[str, t.Any]] = None

