"""MLflow prediction interface for the supplied, already-fitted mapper."""

import joblib
import pandas as pd


FEATURES = ["ctag", "label", "stmt"]
RANKS = [f"rank_{i}" for i in range(1, 6)]


class RegisteredMapper:
    def __init__(self, mapper):
        self.mapper = mapper

    def predict(self, model_input):
        if model_input.empty:
            return pd.DataFrame(columns=RANKS)
        suggestions, _ = self.mapper.suggest(model_input[FEATURES])
        return pd.DataFrame(suggestions, columns=RANKS, index=model_input.index)


def _load_pyfunc(path):
    """MLflow loads this trusted registry artifact without opening the warehouse."""
    return RegisteredMapper(joblib.load(path))
