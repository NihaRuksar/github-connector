from fastapi import FastAPI
from app.routes.github_routes import router
from app.services.github_client import get_authenticated_user
app = FastAPI(
    title="GitHub Cloud Connector",
    description=(
        "A lightweight cloud connector that authenticates with GitHub "
        "and exposes clean REST endpoints for common repository actions."
    ),
    version="1.0.0",
    contact={
        "name": "Niha Ruksar",
        "url": "https://github.com/NihaRuksar",
    },
)
app.include_router(router)
@app.get("/", tags=["Health"], summary="Health check")
async def root():
    """Confirms the server is running."""
    return {"status": "ok", "message": "GitHub Cloud Connector is running."}
@app.get("/auth/verify", tags=["Auth"], summary="Verify GitHub token")
async def verify_auth():
    """
    Verifies the GitHub Personal Access Token is valid
    by fetching the authenticated user's profile.
    """
    user = await get_authenticated_user()
    return {
        "status": "authenticated",
        "github_user": user.get("login"),
        "name": user.get("name"),
        "public_repos": user.get("public_repos"),
    }