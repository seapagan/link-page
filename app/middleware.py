"""Define some middleware needed for this project."""

from collections.abc import Awaitable
from pathlib import Path
from typing import Callable

import csscompressor  # type: ignore
import jsmin  # type: ignore
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

from app.logger import logger

CallNext = Callable[[Request], Awaitable[Response]]


class MinifyStaticFilesMiddleware(BaseHTTPMiddleware):
    """Middleware to minify static CSS and JS files."""

    async def dispatch(self, request: Request, call_next: CallNext) -> Response:
        """Minify static CSS and JS files."""
        logger.info(
            "Minify middleware - Processing %s (scheme: %s)",
            request.url.path,
            request.url.scheme,
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
                return Response(content=minified_content, media_type=media_type)

            logger.warning("File not found: %s", file_path)

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
