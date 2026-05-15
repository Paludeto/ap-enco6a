from abc import ABC, abstractmethod


# In Animal Crossing, turnip prices change twice daily (AM/PM) Mon–Sat = 12 slots.
SLOTS = [
    "Seg AM", "Seg PM", "Ter AM", "Ter PM",
    "Qua AM", "Qua PM", "Qui AM", "Qui PM",
    "Sex AM", "Sex PM", "Sáb AM", "Sáb PM",
]
TOTAL_SLOTS = len(SLOTS)


class PredictionStrategy(ABC):
    @abstractmethod
    def predict(self, observed: list[int]) -> list[tuple[int, int]]:
        """
        Given observed prices, return (min, max) intervals
        for each of the remaining slots.
        """
        pass


class DecreasingPatternStrategy(PredictionStrategy):
    """
    Prices decay monotonically throughout the week.
    Each slot is roughly 85–96% of the previous one.
    """

    def predict(self, observed: list[int]) -> list[tuple[int, int]]:
        remaining = TOTAL_SLOTS - len(observed)
        if not observed:
            base_min, base_max = 60, 80
        else:
            base_min = int(observed[-1] * 0.85)
            base_max = int(observed[-1] * 0.96)

        result = []
        lo, hi = base_min, base_max
        for _ in range(remaining):
            result.append((lo, hi))
            lo = int(lo * 0.85)
            hi = int(hi * 0.96)
        return result


class LargeSpikeStrategy(PredictionStrategy):
    """
    Prices spike dramatically (200–600 bells) in a window of 3 consecutive
    slots somewhere mid-week, preceded and followed by low values.
    """

    SPIKE_WINDOWS = [{2, 3, 4}, {4, 5, 6}, {6, 7, 8}]

    def predict(self, observed: list[int]) -> list[tuple[int, int]]:
        remaining = TOTAL_SLOTS - len(observed)
        # Use the most common spike window if not yet observed
        spike_slots = self.SPIKE_WINDOWS[1]

        result = []
        for i in range(remaining):
            slot_index = len(observed) + i
            if slot_index in spike_slots:
                result.append((200, 600))
            else:
                result.append((85, 90))
        return result


class SmallSpikeStrategy(PredictionStrategy):
    """
    Prices spike moderately (140–200 bells) toward the end of the week.
    """

    def predict(self, observed: list[int]) -> list[tuple[int, int]]:
        remaining = TOTAL_SLOTS - len(observed)
        spike_slots = {6, 7, 8}

        result = []
        for i in range(remaining):
            slot_index = len(observed) + i
            if slot_index in spike_slots:
                result.append((140, 200))
            else:
                result.append((85, 110))
        return result
