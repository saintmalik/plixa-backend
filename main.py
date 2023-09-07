from fastapi import FastAPI
from fastapi.responses import RedirectResponse

from routes import auth_router, organization_router

app = FastAPI(
    title="Plixa API",
    description=(
        "The official REST API for Plixa (eliminating payment hurdles and receipt outage)."
        " Note that if you're using this OpenAPI documentation to hit protected routes"
        " the email address of the user should be provided in the username field"
    ),
)
app.include_router(auth_router, prefix="/api/v1")
app.include_router(organization_router, prefix="/api/v1")


@app.get("/")
def redirect_to_documentation():
    return RedirectResponse("/docs")
