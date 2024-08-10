"""Define the routes for the home page of the app.

For this app, the home page will be the only page, so this module will only
define one route. No saying what the future holds, though!
"""

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from app.config import settings

router = APIRouter()


@router.get("/")
async def root(request: Request) -> HTMLResponse:
    """Root route, which will be the only route for this app right now."""
    templates = Jinja2Templates(directory="app/static/templates")

    return templates.TemplateResponse(
        request=request, name="index.html", context={"settings": settings}
    )
