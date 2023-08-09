from fastapi import Request, Response
import logging

from starlette.responses import JSONResponse

logging.basicConfig(filename='app.log', level=logging.ERROR)

class WrongLoginException(Exception):
    def __init__(self, code: int = 400, detail: str = "Wrong Login"):
        self.detail = detail
        self.code = code


def custom_wrong_login_exception_handler(request: Request, exc: WrongLoginException):
    logging.error(f"An error occurred: {str(exc.detail)}")
    return JSONResponse(content={"detail": str(exc.detail)}, status_code=int(exc.code))