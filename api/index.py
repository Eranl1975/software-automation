from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routes.automation import router as automation_router
from api.routes.ai import router as ai_router
from api.routes.cicd import router as cicd_router

app = FastAPI(
    title="Software Automation API",
    description="AI-powered software automation platform with CI/CD tooling",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(automation_router, prefix="/api/automation", tags=["Automation"])
app.include_router(ai_router, prefix="/api/ai", tags=["AI"])
app.include_router(cicd_router, prefix="/api/cicd", tags=["CI/CD"])


@app.get("/")
async def root():
    return {
        "service": "Software Automation",
        "status": "running",
        "version": "1.0.0",
        "docs": "/docs",
    }


@app.get("/health")
async def health():
    return {"status": "ok"}
