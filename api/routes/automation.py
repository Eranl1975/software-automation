from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from automation.workflows import WorkflowEngine
from automation.scheduler import TaskScheduler

router = APIRouter()
engine = WorkflowEngine()
scheduler = TaskScheduler()


class WorkflowRequest(BaseModel):
    name: str
    steps: list[dict]
    trigger: str = "manual"


class TaskRequest(BaseModel):
    name: str
    command: str
    schedule: str | None = None  # cron expression


@router.get("/workflows")
async def list_workflows():
    return {"workflows": engine.list_workflows()}


@router.post("/workflows")
async def create_workflow(req: WorkflowRequest):
    workflow_id = engine.create(req.name, req.steps, req.trigger)
    return {"id": workflow_id, "status": "created"}


@router.post("/workflows/{workflow_id}/run")
async def run_workflow(workflow_id: str):
    result = engine.run(workflow_id)
    if result is None:
        raise HTTPException(status_code=404, detail="Workflow not found")
    return result


@router.get("/tasks")
async def list_tasks():
    return {"tasks": scheduler.list_tasks()}


@router.post("/tasks")
async def schedule_task(req: TaskRequest):
    task_id = scheduler.add(req.name, req.command, req.schedule)
    return {"id": task_id, "status": "scheduled"}
