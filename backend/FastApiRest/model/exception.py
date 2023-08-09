from pydantic import Field
class ErrorResponse:
    detail: str = Field(..., description="Detail Provided by Server")
    def __init__(self, detail):
        self.detail = detail