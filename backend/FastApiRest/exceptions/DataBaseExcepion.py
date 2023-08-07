from fastapi import Request, Response
import logging

from starlette.responses import JSONResponse

logging.basicConfig(filename='app.log', level=logging.ERROR)

#TODO: handle general exeptions by logging

class DataBaseException(Exception):
    def __init__(self, code: int = 500, detail: str = "There was an issue with the database."):
        self.detail = detail
        self.code = code


def custom_database_exception_handler(request: Request, exc: DataBaseException):
    logging.error(f"An error occurred: {str(exc.detail)}")
    return JSONResponse(content={"detail": str(exc.detail)}, status_code=int(exc.code))