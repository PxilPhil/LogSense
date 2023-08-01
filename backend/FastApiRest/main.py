from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.data import data
from api.group import group
from api.pc import pc
from api.user import user
from api.application import application

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
app.include_router(group, tags=["Group"], prefix="/group")
app.include_router(pc, tags=["PC"], prefix="/pc")
app.include_router(application, tags=["Application"], prefix="/pc/{pc_id}/application")
app.include_router(data, tags=["Data"], prefix="/data")

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
