from datetime import date

from .observer import Subject
from .task import Task, TaskType


class TaskManager(Subject):
    def __init__(self) -> None:
        super().__init__()
        self._tasks: list[Task] = []

    def add_task(self, task: Task) -> None:
        self._tasks.append(task)

    def get_today_tasks(self) -> list[Task]:
        today = date.today()
        return [
            t for t in self._tasks
            if t.available_date <= today and not t.completed
        ]

    def complete_task(self, name: str) -> None:
        for task in self._tasks:
            if task.name == name and not task.completed:
                task.complete()
                self.notify("task_completed", {"task": task})
                return
        raise ValueError(f"Task '{name}' not found or already completed.")

    def reset_daily_tasks(self) -> None:
        for task in self._tasks:
            if task.task_type == TaskType.DAILY:
                task.completed = False
        self.notify("daily_reset", {"count": sum(
            1 for t in self._tasks if t.task_type == TaskType.DAILY
        )})
