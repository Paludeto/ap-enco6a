from .strategies import PredictionStrategy, SLOTS, TOTAL_SLOTS


class TurnipPredictor:
    """
    Context in the Strategy pattern.
    Delegates prediction to whichever PredictionStrategy is currently set.
    """

    def __init__(self, strategy: PredictionStrategy) -> None:
        self._strategy = strategy

    def set_strategy(self, strategy: PredictionStrategy) -> None:
        self._strategy = strategy

    def predict(self, observed: list[int]) -> list[tuple[int, int]]:
        if len(observed) > TOTAL_SLOTS:
            raise ValueError(f"Maximum {TOTAL_SLOTS} price slots per week.")
        return self._strategy.predict(observed)

    def display_prediction(self, observed: list[int], buy_price: int = 0) -> None:
        if buy_price:
            print(f"  Preço de compra (domingo): {buy_price} bells")
        print()
        print(f"  {'Slot':<10} {'Observado':>12}   {'Projeção (min–max)':>20}")
        print(f"  {'-'*46}")

        predictions = self.predict(observed)
        pred_iter = iter(predictions)

        for i, slot in enumerate(SLOTS):
            if i < len(observed):
                print(f"  {slot:<10} {observed[i]:>12}   {'—':>20}")
            else:
                lo, hi = next(pred_iter)
                print(f"  {slot:<10} {'—':>12}   {f'{lo}–{hi} bells':>20}")
