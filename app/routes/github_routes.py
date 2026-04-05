from fastapi import APIRouter, Query
from app.services.github_client import fetch_repos, fetch_issues, create_issue, create_pull_request
from app.models.schemas import (
    CreateIssueRequest,
    CreatePRRequest,
    RepoItem,
    IssueItem,
    CreatedIssueResponse,
    CreatedPRResponse,
)
router = APIRouter(prefix="/api", tags=["GitHub Connector"])
@router.get(
    "/repos",
    response_model=list[RepoItem],
    summary="Fetch repositories for a user or organisation",
)
async def get_repos(
    username: str = Query(
        ...,
        description="GitHub username or organisation",
        examples=["torvalds"]
    )
):
    raw_repos = await fetch_repos(username)
    return [
        RepoItem(
            name=repo["name"],
            full_name=repo["full_name"],
            description=repo.get("description"),
            private=repo["private"],
            url=repo["html_url"],
            stars=repo["stargazers_count"],
            language=repo.get("language"),
        )
        for repo in raw_repos
    ]
@router.get(
    "/list-issues",
    response_model=list[IssueItem],
    summary="List open issues in a repository",
)
async def list_issues(
    owner: str = Query(
        ...,
        description="Repository owner — username or organisation",
        examples=["microsoft"]
    ),
    repo: str = Query(
        ...,
        description="Repository name",
        examples=["vscode"]
    ),
):
    raw_issues = await fetch_issues(owner, repo)

    return [
        IssueItem(
            number=issue["number"],
            title=issue["title"],
            state=issue["state"],
            created_at=issue["created_at"],
            url=issue["html_url"],
            author=issue["user"]["login"],
        )
        for issue in raw_issues
        if "pull_request" not in issue
    ]
@router.post(
    "/create-issue",
    response_model=CreatedIssueResponse,
    status_code=201,
    summary="Create a new issue in a repository",
)
async def post_create_issue(payload: CreateIssueRequest):
    created = await create_issue(
        owner=payload.owner,
        repo=payload.repo,
        title=payload.title,
        body=payload.body or "",
    )
    return CreatedIssueResponse(
        message="Issue created successfully",
        issue_number=created["number"],
        title=created["title"],
        url=created["html_url"],
    ) 
@router.post(
    "/create-pr",
    response_model=CreatedPRResponse,
    status_code=201,
    summary="Create a new pull request",
)
async def post_create_pr(payload: CreatePRRequest):
    created = await create_pull_request(
        owner=payload.owner,
        repo=payload.repo,
        title=payload.title,
        head=payload.head,
        base=payload.base,
        body=payload.body or "",
    )
    return CreatedPRResponse(
        message="Pull request created successfully",
        pr_number=created["number"],
        title=created["title"],
        url=created["html_url"],
        state=created["state"],
    )