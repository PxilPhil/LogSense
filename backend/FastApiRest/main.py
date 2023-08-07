from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from fastapi import FastAPI, HTTPException

from api.data import data
#from api.group import group
from api.pc import pc
from api.user import user
from api.application import application
from exceptions.DataBaseExcepion import DataBaseException, custom_database_exception_handler
from exceptions.NotFoundExcepion import NotFoundException, custom_not_found_exception_handler
from exceptions.WrongConfigurationException import WrongConfigurationException, custom_wrong_configuration_exception_handler
from exceptions.WrongLoginException import WrongLoginException, custom_wrong_login_exception_handler
from exceptions.InvalidParametersException import InvalidParametersException, custom_invalid_parameter_exception_handler
from exceptions.DataBaseInsertExcepion import DataBaseInsertException, custom_database_insert_exception_handler

app = FastAPI()

tags_metadata = [
    {
        "name": "Data",
        "description": "Operations related to the Data sent by the Agent",
    },
    {
        "name": "PC",
        "description": "Operations related to the PCs of an User",
    },
    {
        "name": "User",
        "description": "Operations related to the User",
    },
    {
        "name": "Application",
        "description": "Operations related to the Applications of an PC",
    },
    {
        "name": "Group",
        "description": "Operations related to Groups",
    }
]

# TODO: Add origin of angular application
origins = [
    "http://localhost:4200",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user, tags=["User"], prefix="/user")
#app.include_router(group, tags=["Group"], prefix="/group")
app.include_router(pc, tags=["PC"], prefix="/pc")
app.include_router(application, tags=["Application"], prefix="/pc/{pc_id}/application")
app.include_router(data, tags=["Data"], prefix="/data")

app.add_exception_handler(NotFoundException, custom_not_found_exception_handler)
app.add_exception_handler(DataBaseException, custom_database_exception_handler)
app.add_exception_handler(DataBaseInsertException, custom_database_insert_exception_handler)
app.add_exception_handler(WrongLoginException, custom_wrong_login_exception_handler)
app.add_exception_handler(InvalidParametersException, custom_invalid_parameter_exception_handler)
app.add_exception_handler(WrongConfigurationException, custom_wrong_configuration_exception_handler)



if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="debug")

@app.get("/")
def root():
    """
    Root Endpoint

    Returns:
        dict: A dictionary with the message "LogSense"
    """
    return {"message": "LogSense"}
