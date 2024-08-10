"""Primary module for the FastAPI app."""

from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from jinja2.exceptions import UndefinedError

from app.resources.home import JinjaTemplateError
from app.resources.routes import api_router

app = FastAPI()

app.mount("/static", StaticFiles(directory="app/static"), name="static")

app.include_router(api_router)


@app.exception_handler(JinjaTemplateError)
async def jinja_template_exception_handler(
    request: Request, exc: JinjaTemplateError
):
    error_templates = Jinja2Templates(directory="app/static/templates")

    error_type = (
        "Undefined Variable"
        if isinstance(exc.original_exception, UndefinedError)
        else "Template Rendering"
    )
    error_message = str(exc.original_exception)

    return error_templates.TemplateResponse(
        "error.html",
        {
            "request": request,
            "error_type": error_type,
            "error_message": error_message,
        },
        status_code=500,
    )
