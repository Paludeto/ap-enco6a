from dataclasses import dataclass, field
from datetime import date
from enum import Enum


class TaskType(Enum):
    DAILY = "daily"
    SEASONAL = "seasonal"


@dataclass
class Task:
    name: str
    task_type: TaskType
    description: str
    available_date: date = field(default_factory=date.today)
    completed: bool = False

    def complete(self) -> None:
        if self.completed:
            raise ValueError(f"Task '{self.name}' is already completed.")
        self.completed = True
