from __future__ import annotations

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.core.config import get_settings
from app.core.exceptions import (
    ApplicationError,
    EmailAlreadyExistsError,
    ProjectNotFoundError,
    UserNotFoundError,
)
from app.routers.projects import router as projects_router
from app.routers.users import router as users_router


def create_app() -> FastAPI:
    settings = get_settings()
    app = FastAPI(
        title=settings.app_name,
        version=settings.app_version,
        description="users, projects, ownership",
    )

    register_exception_handlers(app)
    app.include_router(users_router)
    app.include_router(projects_router)

    @app.get("/health", tags=["health"])
    async def healthcheck() -> dict[str, str]:
        return {"status": "ok"}

    return app


def register_exception_handlers(app: FastAPI) -> None:
    def error_response(status_code: int, detail: str) -> JSONResponse:
        return JSONResponse(status_code=status_code, content={"detail": detail})

    @app.exception_handler(EmailAlreadyExistsError)
    async def handle_duplicate_email(_: Request, exc: EmailAlreadyExistsError) -> JSONResponse:
        return error_response(409, str(exc))

    @app.exception_handler(UserNotFoundError)
    async def handle_user_not_found(_: Request, exc: UserNotFoundError) -> JSONResponse:
        return error_response(404, str(exc))

    @app.exception_handler(ProjectNotFoundError)
    async def handle_project_not_found(_: Request, exc: ProjectNotFoundError) -> JSONResponse:
        return error_response(404, str(exc))

    @app.exception_handler(ApplicationError)
    async def handle_application_error(_: Request, exc: ApplicationError) -> JSONResponse:
        return error_response(400, str(exc))


app = create_app()
