from fastapi import Request, Response
import logging

from starlette.responses import JSONResponse

logging.basicConfig(filename='app.log', level=logging.ERROR)

class DataBaseInsertException(Exception):
    def __init__(self, code: int = 500, detail: str = "Issue inserting in Table."):
        self.detail = detail
        self.code = code


def custom_database_insert_exception_handler(request: Request, exc: DataBaseInsertException):
    logging.error(f"An error occurred: {str(exc.detail)}")
    return JSONResponse(content={"detail": str(exc.detail)}, status_code=int(exc.code))
