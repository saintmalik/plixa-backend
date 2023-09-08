from typing import Final

from fastapi import FastAPI
from fastapi.responses import RedirectResponse

from routers import auth_router, organization_router
from routers.user import user_router

app = FastAPI(
    title="Plixa API",
    description=(
        "The official REST API for Plixa (eliminating payment hurdles and receipt outage)."
        " Note that if you're using this OpenAPI documentation to hit protected routers"
        " the email address of the user should be provided in the username field"
    ),
)
version_prefix: Final[str] = "/api/v1"
app.include_router(auth_router, prefix=version_prefix)
app.include_router(organization_router, prefix=version_prefix)
app.include_router(user_router, prefix=version_prefix)


@app.get("/")
def redirect_to_documentation():
    return RedirectResponse("/docs")
