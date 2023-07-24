from fastapi import FastAPI

from api.data import data
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
    }
]

app.include_router(user, tags=["User"], prefix="/user")
app.include_router(pc, tags=["PC"], prefix="/pc")
app.include_router(application, tags=["Application"], prefix="/pc/{pc_id}/application")
app.include_router(data, tags=["Data"], prefix="/data")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)

@app.get("/")
def root():
    """
    Root Endpoint

    Returns:
        dict: A dictionary with the message "LogSense"
    """
    return {"message": "LogSense"}
