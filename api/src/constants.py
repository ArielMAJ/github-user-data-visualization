from src.config import get_settings

GITHUB_API_HEADERS = {
    "Accept": "application/vnd.github+json",
    "X-GitHub-Api-Version": "2022-11-28",
}

if get_settings().GITHUB_TOKEN:
    GITHUB_API_HEADERS["Authorization"] = f"Bearer {get_settings().GITHUB_TOKEN}"
