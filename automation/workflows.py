import uuid
from datetime import datetime


class WorkflowEngine:
    """In-memory workflow engine. Swap storage backend for production."""

    def __init__(self):
        self._workflows: dict[str, dict] = {}

    def create(self, name: str, steps: list[dict], trigger: str = "manual") -> str:
        wf_id = str(uuid.uuid4())[:8]
        self._workflows[wf_id] = {
            "id": wf_id,
            "name": name,
            "steps": steps,
            "trigger": trigger,
            "created_at": datetime.utcnow().isoformat(),
            "runs": [],
        }
        return wf_id

    def list_workflows(self) -> list[dict]:
        return list(self._workflows.values())

    def run(self, workflow_id: str) -> dict | None:
        wf = self._workflows.get(workflow_id)
        if not wf:
            return None

        run = {
            "run_id": str(uuid.uuid4())[:8],
            "workflow_id": workflow_id,
            "started_at": datetime.utcnow().isoformat(),
            "status": "completed",
            "steps_executed": len(wf["steps"]),
        }
        wf["runs"].append(run)
        return run
