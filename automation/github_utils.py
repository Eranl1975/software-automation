"""GitHub API helpers for automation pipelines."""
import os
import httpx

GITHUB_API = "https://api.github.com"


def get_headers(token: str | None = None) -> dict:
    t = token or os.getenv("GITHUB_TOKEN", "")
    return {
        "Authorization": f"Bearer {t}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
    }


async def get_repo_info(owner: str, repo: str) -> dict:
    async with httpx.AsyncClient() as client:
        r = await client.get(f"{GITHUB_API}/repos/{owner}/{repo}", headers=get_headers())
        r.raise_for_status()
        return r.json()


async def list_branches(owner: str, repo: str) -> list[dict]:
    async with httpx.AsyncClient() as client:
        r = await client.get(
            f"{GITHUB_API}/repos/{owner}/{repo}/branches", headers=get_headers()
        )
        r.raise_for_status()
        return r.json()


async def get_latest_commit(owner: str, repo: str, branch: str = "main") -> dict:
    async with httpx.AsyncClient() as client:
        r = await client.get(
            f"{GITHUB_API}/repos/{owner}/{repo}/commits/{branch}",
            headers=get_headers(),
        )
        r.raise_for_status()
        return r.json()
