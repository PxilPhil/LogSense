from fastapi import Request, Response
import logging

from starlette.responses import JSONResponse

logging.basicConfig(filename='app.log', level=logging.ERROR)

class WrongConfigurationException(Exception):
    def __init__(self, code: int = 500, detail: str = "Wrong Server Configuration"):
        self.detail = detail
        self.code = code


def custom_wrong_configuration_exception_handler(request: Request, exc: WrongConfigurationException):
    logging.error(f"An error occurred: {str(exc.detail)}")
    return JSONResponse(content={"detail": str(exc.detail)}, status_code=int(exc.code))