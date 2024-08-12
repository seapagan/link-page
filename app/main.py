"""Primary module for the FastAPI app."""

import logging
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
from starlette.middleware.base import BaseHTTPMiddleware

from app.resources.home import JinjaTemplateError
from app.resources.routes import api_router

CallNext = Callable[[Request], Awaitable[Response]]

logger = logging.getLogger(__name__)

app = FastAPI()

app.mount("/static", StaticFiles(directory="app/static"), name="static")

app.include_router(api_router)


class MinifyStaticFilesMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: CallNext) -> Response:
        logger.info(
            f"Minify middleware: Processing {request.url.path} (scheme: {request.url.scheme})"
        )

        if request.url.path.startswith("/static") and (
            request.url.path.endswith(".css")
            or request.url.path.endswith(".js")
        ):
            file_path = Path("app/static") / request.url.path.removeprefix(
                "/static/"
            )
            if file_path.exists():
                content = file_path.read_text(encoding="utf-8")
                if file_path.suffix == ".css":
                    minified_content = csscompressor.compress(content)
                elif file_path.suffix == ".js":
                    minified_content = jsmin.jsmin(content)
                media_type = (
                    "text/css"
                    if file_path.suffix == ".css"
                    else "application/javascript"
                )
                logger.info(f"Minified {file_path}")
                return Response(content=minified_content, media_type=media_type)
            else:
                logger.warning(f"File not found: {file_path}")

        return await call_next(request)


class HTTPSMiddleware(BaseHTTPMiddleware):
    """Middleware to set the scheme based on the X-Forwarded-Proto header."""

    async def dispatch(self, request: Request, call_next: CallNext) -> Response:
        """Set the scheme based on the X-Forwarded-Proto header.

        This allows 'url_for' to generate URLs with the correct scheme - HTTP
        or HTTPS. Otherwise, when proxied behind a load balancer or reverse
        proxy, the URLs would always be generated with 'http' and be blocked
        by the browser as mixed content.

        It requires the 'X-Forwarded-Proto' header to be set by the load
        balancer or reverse proxy. If the header is not present, the scheme
        is unchanged from whatever is set in the request URL.
        """
        if "X-Forwarded-Proto" in request.headers:
            request.scope["scheme"] = request.headers["X-Forwarded-Proto"]
        return await call_next(request)


app.add_middleware(MinifyStaticFilesMiddleware)
app.add_middleware(HTTPSMiddleware)


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


# @app.middleware("http")
# async def minify_static_files(
#     request: Request, call_next: CallNext
# ) -> Response:
#     """Minify JS and CSS static files."""
#     # Only minify .css and .js files
#     if request.url.path.startswith("/static") and (
#         request.url.path.endswith(".css") or request.url.path.endswith(".js")
#     ):
#         file_path = Path("app/static") / request.url.path[len("/static/") :]
#
#         if file_path.exists():
#             content = file_path.read_text(encoding="utf-8")
#
#             # Minify based on file type
#             if file_path.suffix == ".css":
#                 minified_content = csscompressor.compress(content)
#             elif file_path.suffix == ".js":
#                 minified_content = jsmin.jsmin(content)
#
#             media_type = (
#                 "text/css"
#                 if file_path.suffix == ".css"
#                 else "application/javascript"
#             )
#             return Response(content=minified_content, media_type=media_type)
#
#     # For other requests, proceed as normal
#     return await call_next(request)
