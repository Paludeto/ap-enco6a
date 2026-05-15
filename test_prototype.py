import sys
import os
import unittest
from datetime import date, timedelta
from unittest.mock import MagicMock

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from tasks.task import Task, TaskType
from tasks.task_manager import TaskManager
from tasks.observer import Observer
from turnip.predictor import TurnipPredictor
from turnip.strategies import (
    DecreasingPatternStrategy,
    LargeSpikeStrategy,
    TOTAL_SLOTS,
)


# ──────────────────────────────────────────────────────────────
# Helper
# ──────────────────────────────────────────────────────────────

def make_daily_task(name: str = "Coletar conchas") -> Task:
    return Task(name, TaskType.DAILY, "Desc", available_date=date.today())

def make_seasonal_task(name: str = "Festival", days_offset: int = 0) -> Task:
    return Task(
        name, TaskType.SEASONAL, "Desc",
        available_date=date.today() + timedelta(days=days_offset),
    )


# ──────────────────────────────────────────────────────────────
# Tests for TaskManager.complete_task
# ──────────────────────────────────────────────────────────────

class TestCompleteTask(unittest.TestCase):

    def setUp(self) -> None:
        self.manager = TaskManager()

    # ── success ──────────────────────────────────────────────

    def test_completes_existing_task(self) -> None:
        """Completing a present, pending task sets completed=True."""
        task = make_daily_task("Regar flores")
        self.manager.add_task(task)

        self.manager.complete_task("Regar flores")

        self.assertTrue(task.completed)

    def test_completed_task_leaves_others_untouched(self) -> None:
        """Only the named task is marked; siblings remain pending."""
        t1 = make_daily_task("Tarefa A")
        t2 = make_daily_task("Tarefa B")
        self.manager.add_task(t1)
        self.manager.add_task(t2)

        self.manager.complete_task("Tarefa A")

        self.assertTrue(t1.completed)
        self.assertFalse(t2.completed)

    def test_notifies_observer_on_completion(self) -> None:
        """Observer.update is called exactly once with the correct event."""
        observer = MagicMock(spec=Observer)
        self.manager.attach(observer)
        task = make_daily_task("Checar loja")
        self.manager.add_task(task)

        self.manager.complete_task("Checar loja")

        observer.update.assert_called_once()
        event, data = observer.update.call_args[0]
        self.assertEqual(event, "task_completed")
        self.assertIs(data["task"], task)

    # ── failure / exception ───────────────────────────────────

    def test_raises_for_nonexistent_task(self) -> None:
        """Completing a name that was never added raises ValueError."""
        with self.assertRaises(ValueError):
            self.manager.complete_task("Tarefa Inexistente")

    def test_raises_for_already_completed_task(self) -> None:
        """Completing the same task twice raises ValueError on the second call."""
        task = make_daily_task("Coletar conchas")
        self.manager.add_task(task)
        self.manager.complete_task("Coletar conchas")

        with self.assertRaises(ValueError):
            self.manager.complete_task("Coletar conchas")

    # ── edge ─────────────────────────────────────────────────

    def test_does_not_complete_future_seasonal_task_by_name_clash(self) -> None:
        """
        A seasonal task dated in the future is still completable by name
        (complete_task does not filter by date — that is get_today_tasks's job).
        This documents the intentional boundary between the two methods.
        """
        future_task = make_seasonal_task("Festival Futuro", days_offset=5)
        self.manager.add_task(future_task)

        # complete_task does NOT enforce date; only get_today_tasks does.
        self.manager.complete_task("Festival Futuro")
        self.assertTrue(future_task.completed)

    def test_empty_manager_raises(self) -> None:
        """Calling complete_task on a manager with no tasks raises ValueError."""
        with self.assertRaises(ValueError):
            self.manager.complete_task("Qualquer Coisa")

    def test_two_tasks_same_name_completes_first_only(self) -> None:
        """
        If two tasks share the same name, only the first pending one is
        completed per call — a known limitation of the current implementation.
        """
        t1 = make_daily_task("Duplicada")
        t2 = make_daily_task("Duplicada")
        self.manager.add_task(t1)
        self.manager.add_task(t2)

        self.manager.complete_task("Duplicada")

        self.assertTrue(t1.completed)
        self.assertFalse(t2.completed)


# ──────────────────────────────────────────────────────────────
# Tests for TurnipPredictor.predict
# ──────────────────────────────────────────────────────────────

class TestTurnipPredictorPredict(unittest.TestCase):

    def setUp(self) -> None:
        self.predictor = TurnipPredictor(DecreasingPatternStrategy())

    # ── success ──────────────────────────────────────────────

    def test_returns_correct_number_of_remaining_slots(self) -> None:
        """With k prices observed, exactly (TOTAL_SLOTS - k) intervals are returned."""
        observed = [110, 98, 92]
        result = self.predictor.predict(observed)

        self.assertEqual(len(result), TOTAL_SLOTS - len(observed))

    def test_each_result_is_valid_interval(self) -> None:
        """Every returned interval has min <= max and both values are positive."""
        observed = [110, 98]
        result = self.predictor.predict(observed)

        for lo, hi in result:
            self.assertGreater(lo, 0)
            self.assertLessEqual(lo, hi)

    def test_strategy_swap_changes_output(self) -> None:
        """set_strategy replaces the delegate; outputs differ between strategies."""
        observed = [110, 98, 92]

        self.predictor.set_strategy(DecreasingPatternStrategy())
        result_dec = self.predictor.predict(observed)

        self.predictor.set_strategy(LargeSpikeStrategy())
        result_spike = self.predictor.predict(observed)

        self.assertNotEqual(result_dec, result_spike)

    # ── failure / exception ───────────────────────────────────

    def test_raises_for_too_many_prices(self) -> None:
        """More than TOTAL_SLOTS observed prices raises ValueError."""
        oversized = [100] * (TOTAL_SLOTS + 1)

        with self.assertRaises(ValueError):
            self.predictor.predict(oversized)

    # ── edge ─────────────────────────────────────────────────

    def test_empty_observed_returns_all_slots(self) -> None:
        """With no observations, all TOTAL_SLOTS intervals are projected."""
        result = self.predictor.predict([])

        self.assertEqual(len(result), TOTAL_SLOTS)

    def test_fully_observed_week_returns_empty(self) -> None:
        """With all slots observed, there is nothing left to predict."""
        full_week = [100] * TOTAL_SLOTS
        result = self.predictor.predict(full_week)

        self.assertEqual(result, [])

    def test_single_price_observation(self) -> None:
        """A single observed price produces TOTAL_SLOTS - 1 projections."""
        result = self.predictor.predict([120])

        self.assertEqual(len(result), TOTAL_SLOTS - 1)


if __name__ == "__main__":
    unittest.main(verbosity=2)
