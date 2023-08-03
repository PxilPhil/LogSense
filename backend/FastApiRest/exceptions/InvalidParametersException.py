from fastapi import Request, Response
import logging

from starlette.responses import JSONResponse

logging.basicConfig(filename='app.log', level=logging.ERROR)

class InvalidParametersException(Exception):
    def __init__(self, code: int = 400, detail: str = "Wrong Parameters sent."):
        self.detail = detail
        self.code = code


def custom_invalid_parameter_exception_handler(request: Request, exc: InvalidParametersException):
    logging.error(f"An error occurred: {str(exc.detail)}")
    return JSONResponse(content={"detail": str(exc.detail)}, status_code=int(exc.code))