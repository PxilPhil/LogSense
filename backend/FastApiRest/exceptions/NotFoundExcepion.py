from fastapi import Request, Response
import logging

from starlette.responses import JSONResponse

logging.basicConfig(filename='app.log', level=logging.ERROR)

class NotFoundException(Exception):
    def __init__(self, code: int = 404, detail: str = "Data was not found or doesn't exist"):
        self.detail = detail
        self.code = code


def custom_not_found_exception_handler(request: Request, exc: NotFoundException):
    logging.error(f"An error occurred: {str(exc.detail)}")
    return JSONResponse(content={"detail": str(exc.detail)}, status_code=int(exc.code))