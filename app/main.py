from fastapi import FastAPI
from . import models
from .database import engine
from . import markers
from fastapi.staticfiles import StaticFiles

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(markers.router)

app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")
