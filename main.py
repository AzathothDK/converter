from fastapi import FastAPI

from database import engine
from models import Base
from api import router

app = FastAPI()

app.include_router(router)

Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="debug")

