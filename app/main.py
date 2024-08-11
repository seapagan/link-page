"""Primary module for the FastAPI app."""

from collections.abc import Awaitable
from pathlib import Path
from typing import Callable

import csscompressor  # type: ignore
import jsmin  # type: ignore
from fastapi import FastAPI, Request, Response
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from jinja2.exceptions import UndefinedError

from app.resources.home import JinjaTemplateError
from app.resources.routes import api_router

CallNext = Callable[[Request], Awaitable[Response]]

app = FastAPI()

app.mount("/static", StaticFiles(directory="app/static"), name="static")

app.include_router(api_router)


@app.exception_handler(JinjaTemplateError)
async def jinja_template_exception_handler(
    request: Request, exc: JinjaTemplateError
) -> HTMLResponse:
    """Deal with template exceptions."""
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


@app.middleware("http")
async def minify_static_files(
    request: Request, call_next: CallNext
) -> Response:
    """Minify JS and CSS static files."""
    # Only minify .css and .js files
    if request.url.path.startswith("/static") and (
        request.url.path.endswith(".css") or request.url.path.endswith(".js")
    ):
        file_path = Path("app/static") / request.url.path[len("/static/") :]

        if file_path.exists():
            content = file_path.read_text(encoding="utf-8")

            # Minify based on file type
            if file_path.suffix == ".css":
                minified_content = csscompressor.compress(content)
            elif file_path.suffix == ".js":
                minified_content = jsmin.jsmin(content)

            media_type = (
                "text/css"
                if file_path.suffix == ".css"
                else "application/javascript"
            )
            return Response(content=minified_content, media_type=media_type)

    # For other requests, proceed as normal
    return await call_next(request)
