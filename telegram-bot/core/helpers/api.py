from enum import Enum



class ApiError(Exception):
    def __init__(self, code, message, details=None):
        super().__init__(message)
        self.code = code
        self.details = details


class ApiRouter(Enum):
    """
    Enum for API routers.
    """
    GENERATE = "agent/generate"


