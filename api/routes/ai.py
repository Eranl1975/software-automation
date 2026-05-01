import os
import anthropic
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter()


class AutomateRequest(BaseModel):
    task: str
    context: str = ""
    language: str = "python"


class ReviewRequest(BaseModel):
    code: str
    language: str = "python"
    focus: str = "general"  # general | security | performance | style


@router.post("/automate")
async def ai_automate(req: AutomateRequest):
    """Generate automation script for a given task using Claude."""
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        raise HTTPException(status_code=503, detail="ANTHROPIC_API_KEY not configured")

    client = anthropic.Anthropic(api_key=api_key)
    prompt = (
        f"You are a DevOps automation expert. Write a {req.language} script to: {req.task}\n"
        f"Context: {req.context}\n"
        "Return only the code with inline comments. No explanations outside the code."
    )

    message = client.messages.create(
        model="claude-opus-4-6",
        max_tokens=2048,
        messages=[{"role": "user", "content": prompt}],
    )
    return {"script": message.content[0].text, "language": req.language}


@router.post("/review")
async def ai_review(req: ReviewRequest):
    """AI-powered code review focused on automation quality."""
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        raise HTTPException(status_code=503, detail="ANTHROPIC_API_KEY not configured")

    client = anthropic.Anthropic(api_key=api_key)
    prompt = (
        f"Review this {req.language} code for {req.focus} issues.\n"
        "Respond as JSON with keys: score (0-10), issues (list), suggestions (list).\n\n"
        f"```{req.language}\n{req.code}\n```"
    )

    message = client.messages.create(
        model="claude-opus-4-6",
        max_tokens=1024,
        messages=[{"role": "user", "content": prompt}],
    )
    return {"review": message.content[0].text}


@router.post("/explain")
async def ai_explain(req: ReviewRequest):
    """Explain what an automation script does."""
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        raise HTTPException(status_code=503, detail="ANTHROPIC_API_KEY not configured")

    client = anthropic.Anthropic(api_key=api_key)
    prompt = (
        f"Explain what this {req.language} automation script does in plain English.\n"
        "Be concise: 3-5 sentences max.\n\n"
        f"```{req.language}\n{req.code}\n```"
    )

    message = client.messages.create(
        model="claude-opus-4-6",
        max_tokens=512,
        messages=[{"role": "user", "content": prompt}],
    )
    return {"explanation": message.content[0].text}
