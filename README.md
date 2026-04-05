# GitHub Cloud Connector

A lightweight REST API connector that authenticates with GitHub and exposes clean endpoints for common repository actions.

Built with **Python** and **FastAPI** as part of the Aventisia Junior Developer assignment.

---

## Features

- Authenticate with GitHub using a Personal Access Token (PAT)
- Fetch public repositories for any GitHub user or organisation
- List open issues from any repository
- Create new issues in a repository
- Clean error handling for all GitHub API failures
- Auto-generated interactive API docs at `/docs`

---

## Tech Stack

| Layer | Technology |
|---|---|
| Language | Python 3.10+ |
| Framework | FastAPI |
| HTTP Client | httpx (async) |
| Validation | Pydantic v2 |
| Server | Uvicorn |
| Auth | GitHub Personal Access Token |

---

## Project Structure

```
github_connector/
│
├── main.py                        # FastAPI app entry point
├── requirements.txt               # All dependencies
├── .env                           # Your secret token (never committed)
├── .env.example                   # Safe template to show required variables
├── .gitignore                     # Excludes .env and cache files
│
└── app/
    ├── config.py                  # Loads and validates environment variables
    ├── models/
    │   └── schemas.py             # Pydantic request and response models
    ├── routes/
    │   └── github_routes.py       # All API endpoint definitions
    └── services/
        └── github_client.py       # All GitHub API calls live here
```

---

## Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/NihaRuksar/github-connector.git
cd github-connector
```

### 2. Create a virtual environment

```bash
python -m venv venv

# Activate it
venv\Scripts\activate        # Windows
source venv/bin/activate     # Mac / Linux
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Create your `.env` file

```bash
cp .env.example .env
```

Open `.env` and add your GitHub Personal Access Token:

```
GITHUB_TOKEN=your_personal_access_token_here
GITHUB_API_URL=https://api.github.com
```

**How to get a GitHub PAT:**
1. Go to GitHub → Settings → Developer Settings
2. Personal Access Tokens → Tokens (classic)
3. Click **Generate new token (classic)**
4. Select scopes: `repo` and `read:user`
5. Copy the token and paste it in `.env`

### 5. Run the server

```bash
uvicorn main:app --reload
```

The server starts at: `http://127.0.0.1:8000`

---

## API Endpoints

### Interactive Docs

Visit `http://127.0.0.1:8000/docs` for the full interactive API documentation where you can test all endpoints directly in the browser.

---

### `GET /`
Health check — confirms the server is running.

**Response:**
```json
{
  "status": "ok",
  "message": "GitHub Cloud Connector is running."
}
```

---

### `GET /auth/verify`
Verifies your GitHub token is valid by fetching your GitHub profile.

**Response:**
```json
{
  "status": "authenticated",
  "github_user": "NihaRuksar",
  "name": "Niha Ruksar",
  "public_repos": 5
}
```

---

### `GET /api/repos?username={username}`
Fetches up to 30 most recently updated public repositories for a GitHub user or organisation.

**Query Parameters:**

| Parameter | Type | Required | Description |
|---|---|---|---|
| `username` | string | Yes | GitHub username or organisation name |

**Example Request:**
```
GET http://127.0.0.1:8000/api/repos?username=torvalds
```

**Example Response:**
```json
[
  {
    "name": "linux",
    "full_name": "torvalds/linux",
    "description": "Linux kernel source tree",
    "private": false,
    "url": "https://github.com/torvalds/linux",
    "stars": 180000,
    "language": "C"
  }
]
```

---

### `GET /api/list-issues?owner={owner}&repo={repo}`
Lists up to 30 open issues in a given repository. Pull requests are automatically excluded.

**Query Parameters:**

| Parameter | Type | Required | Description |
|---|---|---|---|
| `owner` | string | Yes | Repository owner (username or org) |
| `repo` | string | Yes | Repository name |

**Example Request:**
```
GET http://127.0.0.1:8000/api/list-issues?owner=microsoft&repo=vscode
```

**Example Response:**
```json
[
  {
    "number": 214963,
    "title": "Bug: terminal not rendering correctly",
    "state": "open",
    "created_at": "2026-03-28T10:22:00Z",
    "url": "https://github.com/microsoft/vscode/issues/214963",
    "author": "someuser"
  }
]
```

---

### `POST /api/create-issue`
Creates a new issue in a specified repository. Your token must have write access to the target repo.

**Request Body:**

| Field | Type | Required | Description |
|---|---|---|---|
| `owner` | string | Yes | Repository owner |
| `repo` | string | Yes | Repository name |
| `title` | string | Yes | Issue title |
| `body` | string | No | Issue description (markdown supported) |

**Example Request:**
```bash
curl -X POST http://127.0.0.1:8000/api/create-issue \
  -H "Content-Type: application/json" \
  -d '{
    "owner": "NihaRuksar",
    "repo": "Niha-Ruksar",
    "title": "Bug: something is broken",
    "body": "Steps to reproduce..."
  }'
```

**Example Response (201 Created):**
```json
{
  "message": "Issue created successfully",
  "issue_number": 2,
  "title": "Bug: something is broken",
  "url": "https://github.com/NihaRuksar/Niha-Ruksar/issues/2"
}
```

---

## Error Handling

The connector returns clean, descriptive errors for all GitHub API failures:

| Status Code | Meaning |
|---|---|
| `401` | Invalid or expired GitHub token |
| `403` | Rate limit exceeded or insufficient permissions |
| `404` | Repository or resource not found |
| `422` | Invalid input data |

**Example error response:**
```json
{
  "detail": "Resource not found. Check the owner and repository name."
}
```

---

## Author

**Niha Ruksar**
GitHub: [NihaRuksar](https://github.com/NihaRuksar)
