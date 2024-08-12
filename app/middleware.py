"""Define some middleware needed for this project."""

from collections.abc import Awaitable
from typing import Callable

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

CallNext = Callable[[Request], Awaitable[Response]]


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
