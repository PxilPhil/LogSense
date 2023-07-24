from fastapi import FastAPI

from api.data import data
from api.pc import pc
from api.user import user

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
    }
]

app.include_router(data, tags=["Data"], prefix="/data")
app.include_router(pc, tags=["PC"], prefix="/pc")
app.include_router(user, tags=["User"], prefix="/user")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)