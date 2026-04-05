import httpx
from fastapi import HTTPException
from app.config import GITHUB_TOKEN, GITHUB_API_URL
REQUEST_TIMEOUT = 10.0
def get_headers() -> dict[str, str]:
    return {
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
    }
def handle_github_error(response: httpx.Response) -> None:
    if response.status_code == 401:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired GitHub token. Check your .env file."
        )
    if response.status_code == 403:
        raise HTTPException(
            status_code=403,
            detail="GitHub API rate limit exceeded or insufficient token permissions."
        )
    if response.status_code == 404:
        raise HTTPException(
            status_code=404,
            detail="Resource not found. Check the owner and repository name."
        )
    if response.status_code == 422:
        raise HTTPException(
            status_code=422,
            detail="Invalid data sent to GitHub API. Check your request fields."
        )
    if response.status_code >= 400:
        raise HTTPException(
            status_code=response.status_code,
            detail=f"GitHub API returned an error: {response.text}"
        )
async def get_authenticated_user() -> dict:
    async with httpx.AsyncClient(timeout=REQUEST_TIMEOUT) as client:
        response = await client.get(
            f"{GITHUB_API_URL}/user",
            headers=get_headers()
        )
        handle_github_error(response)
        return response.json()
async def fetch_repos(username: str) -> list:
    async with httpx.AsyncClient(timeout=REQUEST_TIMEOUT) as client:
        response = await client.get(
            f"{GITHUB_API_URL}/users/{username}/repos",
            headers=get_headers(),
            params={"per_page": 30, "sort": "updated"}
        )
        handle_github_error(response)
        return response.json()
async def fetch_issues(owner: str, repo: str) -> list:
    async with httpx.AsyncClient(timeout=REQUEST_TIMEOUT) as client:
        response = await client.get(
            f"{GITHUB_API_URL}/repos/{owner}/{repo}/issues",
            headers=get_headers(),
            params={"state": "open", "per_page": 30}
        )
        handle_github_error(response)
        return response.json()
async def create_issue(owner: str, repo: str, title: str, body: str = "") -> dict:
    async with httpx.AsyncClient(timeout=REQUEST_TIMEOUT) as client:
        response = await client.post(
            f"{GITHUB_API_URL}/repos/{owner}/{repo}/issues",
            headers=get_headers(),
            json={"title": title, "body": body}
        )
        handle_github_error(response)
        return response.json()
async def create_pull_request(
    owner: str,
    repo: str,
    title: str,
    head: str,
    base: str,
    body: str = ""
) -> dict:
    async with httpx.AsyncClient(timeout=REQUEST_TIMEOUT) as client:
        response = await client.post(
            f"{GITHUB_API_URL}/repos/{owner}/{repo}/pulls",
            headers=get_headers(),
            json={
                "title": title,
                "body": body,
                "head": head,
                "base": base,
            }
        )
        handle_github_error(response)
        return response.json()