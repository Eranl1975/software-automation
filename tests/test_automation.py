import pytest
from automation.workflows import WorkflowEngine
from automation.scheduler import TaskScheduler


def test_create_and_run_workflow():
    engine = WorkflowEngine()
    wf_id = engine.create("deploy", [{"step": "build"}, {"step": "test"}])
    assert wf_id

    workflows = engine.list_workflows()
    assert len(workflows) == 1
    assert workflows[0]["name"] == "deploy"

    result = engine.run(wf_id)
    assert result["status"] == "completed"
    assert result["steps_executed"] == 2


def test_workflow_not_found():
    engine = WorkflowEngine()
    assert engine.run("nonexistent") is None


def test_schedule_task():
    scheduler = TaskScheduler()
    task_id = scheduler.add("cleanup", "rm -rf /tmp/cache", "0 3 * * *")
    assert task_id

    tasks = scheduler.list_tasks()
    assert len(tasks) == 1
    assert tasks[0]["status"] == "scheduled"


def test_task_without_schedule():
    scheduler = TaskScheduler()
    task_id = scheduler.add("run-tests", "pytest tests/")
    tasks = scheduler.list_tasks()
    assert tasks[0]["status"] == "ready"
