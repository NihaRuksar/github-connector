from pydantic import BaseModel, Field
from typing import Optional
class CreateIssueRequest(BaseModel):
    owner: str = Field(..., min_length=1, description="GitHub username or organisation name", examples=["torvalds"])
    repo: str = Field(..., min_length=1, description="Repository name", examples=["linux"])
    title: str = Field(..., min_length=1, description="Issue title", examples=["Bug: login fails on mobile"])
    body: Optional[str] = Field(None, description="Issue description — markdown supported", examples=["Steps to reproduce:\n1. Open app\n2. Tap login"])
class CreatePRRequest(BaseModel):
    owner: str = Field(..., min_length=1, description="Repository owner", examples=["NihaRuksar"])
    repo: str = Field(..., min_length=1, description="Repository name", examples=["github-connector"])
    title: str = Field(..., min_length=1, description="Pull request title", examples=["feat: add new feature"])
    body: Optional[str] = Field(None, description="Pull request description", examples=["This PR adds a new feature"])
    head: str = Field(..., description="Branch with your changes (must exist on GitHub)", examples=["feature/test-pr"])
    base: str = Field(..., description="Branch to merge into", examples=["master"])
class RepoItem(BaseModel):
    name: str
    full_name: str
    description: Optional[str]
    private: bool
    url: str
    stars: int
    language: Optional[str]
class IssueItem(BaseModel):
    number: int
    title: str
    state: str
    created_at: str
    url: str
    author: str
class CreatedIssueResponse(BaseModel):
    message: str
    issue_number: int
    title: str
    url: str
class CreatedPRResponse(BaseModel):
    message: str
    pr_number: int
    title: str
    url: str
    state: str