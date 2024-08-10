"""Primary module for the FastAPI app."""

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.resources.routes import api_router

app = FastAPI()

app.mount("/static", StaticFiles(directory="app/static"), name="static")

app.include_router(api_router)
