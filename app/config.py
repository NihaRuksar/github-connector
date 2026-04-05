import os
from dotenv import load_dotenv
load_dotenv()
GITHUB_TOKEN: str = os.getenv("GITHUB_TOKEN", "")
GITHUB_API_URL: str = os.getenv("GITHUB_API_URL", "https://api.github.com")
if not GITHUB_TOKEN:
    raise ValueError(
        "GITHUB_TOKEN is missing. "
        "Create a .env file and add: GITHUB_TOKEN=your_token_here"
    )