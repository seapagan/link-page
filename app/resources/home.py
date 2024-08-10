"""Define the routes for the home page of the app.

For this app, the home page will be the only page, so this module will only
define one route. No saying what the future holds, though!
"""

from fastapi import APIRouter

router = APIRouter()


@router.get("/")
async def root() -> dict[str, str]:
    """Root route, which will be the only route for this app right now."""
    return {"message": "App is working!"}
