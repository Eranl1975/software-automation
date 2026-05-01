import os
import httpx
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter()

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
GITHUB_API = "https://api.github.com"


def _gh_headers():
    if not GITHUB_TOKEN:
        raise HTTPException(status_code=503, detail="GITHUB_TOKEN not configured")
    return {
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
    }


class WorkflowDispatch(BaseModel):
    owner: str
    repo: str
    workflow_id: str
    ref: str = "main"
    inputs: dict = {}


class PRRequest(BaseModel):
    owner: str
    repo: str
    title: str
    body: str
    head: str
    base: str = "main"


@router.get("/repos/{owner}/{repo}/workflows")
async def list_workflows(owner: str, repo: str):
    async with httpx.AsyncClient() as client:
        r = await client.get(
            f"{GITHUB_API}/repos/{owner}/{repo}/actions/workflows",
            headers=_gh_headers(),
        )
        r.raise_for_status()
        return r.json()


@router.post("/dispatch")
async def trigger_workflow(req: WorkflowDispatch):
    async with httpx.AsyncClient() as client:
        r = await client.post(
            f"{GITHUB_API}/repos/{req.owner}/{req.repo}/actions/workflows/{req.workflow_id}/dispatches",
            headers=_gh_headers(),
            json={"ref": req.ref, "inputs": req.inputs},
        )
        if r.status_code == 204:
            return {"status": "triggered"}
        r.raise_for_status()


@router.get("/repos/{owner}/{repo}/runs")
async def get_runs(owner: str, repo: str, status: str = ""):
    params = {"status": status} if status else {}
    async with httpx.AsyncClient() as client:
        r = await client.get(
            f"{GITHUB_API}/repos/{owner}/{repo}/actions/runs",
            headers=_gh_headers(),
            params=params,
        )
        r.raise_for_status()
        return r.json()


@router.post("/pull-request")
async def create_pr(req: PRRequest):
    async with httpx.AsyncClient() as client:
        r = await client.post(
            f"{GITHUB_API}/repos/{req.owner}/{req.repo}/pulls",
            headers=_gh_headers(),
            json={
                "title": req.title,
                "body": req.body,
                "head": req.head,
                "base": req.base,
            },
        )
        r.raise_for_status()
        return r.json()
