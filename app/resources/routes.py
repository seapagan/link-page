"""Module for handling routes in the application."""

from fastapi import APIRouter

from app.resources import home

api_router = APIRouter()

api_router.include_router(home.router)
