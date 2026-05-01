import uuid
from datetime import datetime


class TaskScheduler:
    """Simple task registry. Integrate APScheduler or Celery for production."""

    def __init__(self):
        self._tasks: dict[str, dict] = {}

    def add(self, name: str, command: str, schedule: str | None = None) -> str:
        task_id = str(uuid.uuid4())[:8]
        self._tasks[task_id] = {
            "id": task_id,
            "name": name,
            "command": command,
            "schedule": schedule,
            "created_at": datetime.utcnow().isoformat(),
            "status": "scheduled" if schedule else "ready",
        }
        return task_id

    def list_tasks(self) -> list[dict]:
        return list(self._tasks.values())
