"""Primary module for the FastAPI app."""

from fastapi import FastAPI

from app.resources.routes import api_router

app = FastAPI()

app.include_router(api_router)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)  # noqa: S104
