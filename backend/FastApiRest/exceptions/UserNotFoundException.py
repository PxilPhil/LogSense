from fastapi import Request, Response
import logging

from starlette.responses import JSONResponse

logging.basicConfig(filename='app.log', level=logging.ERROR)

class UserNotFoundException(Exception):
    def __init__(self, code: int = 500, detail: str = "User not found."):
        self.detail = detail
        self.code = code


def custom_user_not_found_exception_handler(request: Request, exc: UserNotFoundException):
    logging.error(f"An error occurred: {str(exc.detail)}")
    return JSONResponse(content={"detail": str(exc.detail)}, status_code=int(exc.code))