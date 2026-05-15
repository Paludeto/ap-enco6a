from .observer import Observer


class ConsoleNotifier(Observer):
    """Prints task events to stdout — simulates a push notification."""

    def update(self, event: str, data: dict) -> None:
        if event == "task_completed":
            task = data["task"]
            print(f"  [✓] Concluída: {task.name} ({task.task_type.value})")
        elif event == "daily_reset":
            print(f"  [↺] Reset diário: {data['count']} tarefa(s) disponíveis novamente.")


class TaskLogger(Observer):
    """Accumulates a history of completed tasks for the session."""

    def __init__(self) -> None:
        self._log: list[str] = []

    def update(self, event: str, data: dict) -> None:
        if event == "task_completed":
            task = data["task"]
            self._log.append(f"{task.name} [{task.task_type.value}]")

    def get_log(self) -> list[str]:
        return list(self._log)
