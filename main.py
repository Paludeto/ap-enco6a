from datetime import date

from tasks.task import Task, TaskType
from tasks.task_manager import TaskManager
from tasks.notifiers import ConsoleNotifier, TaskLogger
from turnip.predictor import TurnipPredictor
from turnip.strategies import (
    DecreasingPatternStrategy,
    LargeSpikeStrategy,
    SmallSpikeStrategy,
)


# ──────────────────────────────────────────────
# H3 — Daily task manager (Observer pattern)
# ──────────────────────────────────────────────
def demo_task_manager() -> None:
    print("=" * 52)
    print("  H3 — GERENCIADOR DE TAREFAS DIÁRIAS")
    print("=" * 52)

    manager = TaskManager()
    manager.attach(ConsoleNotifier())

    logger = TaskLogger()
    manager.attach(logger)

    tasks = [
        Task("Coletar conchas",      TaskType.DAILY,    "Varrer a praia diariamente"),
        Task("Falar com vizinhos",   TaskType.DAILY,    "Interagir com todos os villagers"),
        Task("Checar loja Nook",     TaskType.DAILY,    "Ver itens e pagar dívida"),
        Task("Regar flores",         TaskType.DAILY,    "Manter jardim saudável"),
        Task("Festival da Lua",      TaskType.SEASONAL, "Evento especial de outono",
             available_date=date.today()),
    ]
    for t in tasks:
        manager.add_task(t)

    print("\nTarefas disponíveis hoje:")
    for t in manager.get_today_tasks():
        print(f"  [ ] {t.name} — {t.description}")

    print("\nMarcando tarefas como concluídas:")
    manager.complete_task("Coletar conchas")
    manager.complete_task("Checar loja Nook")
    manager.complete_task("Festival da Lua")

    print("\nTarefas restantes:")
    remaining = manager.get_today_tasks()
    if remaining:
        for t in remaining:
            print(f"  [ ] {t.name}")
    else:
        print("  Nenhuma — todas concluídas!")

    print("\nSimulando reset das 5 AM...")
    manager.reset_daily_tasks()

    print("\nLog da sessão:")
    for entry in logger.get_log():
        print(f"  • {entry}")


# ──────────────────────────────────────────────
# H2 — Turnip price predictor (Strategy pattern)
# ──────────────────────────────────────────────
def demo_turnip_predictor() -> None:
    print("\n" + "=" * 52)
    print("  H2 — PREDITOR DE PREÇOS DE TURNIP")
    print("=" * 52)

    # Prices the player observed so far this week (Mon AM through Wed AM)
    observed = [110, 98, 92, 87, 81]
    buy_price = 95

    strategies = [
        ("Padrão Decrescente",  DecreasingPatternStrategy()),
        ("Spike Grande",        LargeSpikeStrategy()),
        ("Spike Pequeno",       SmallSpikeStrategy()),
    ]

    predictor = TurnipPredictor(DecreasingPatternStrategy())

    for name, strategy in strategies:
        print(f"\n--- Estratégia: {name} ---")
        predictor.set_strategy(strategy)
        predictor.display_prediction(observed, buy_price)


if __name__ == "__main__":
    demo_task_manager()
    demo_turnip_predictor()
