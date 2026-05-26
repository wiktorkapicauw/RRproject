"""Rolling-window one-step-ahead variance forecasting."""

import pandas as pd
from arch import arch_model

MODEL_SPECS = {
    "GARCH": {"vol": "GARCH", "p": 1, "o": 0, "q": 1},
    "GJR-GARCH": {"vol": "GARCH", "p": 1, "o": 1, "q": 1},
    "EGARCH": {"vol": "EGARCH", "p": 1, "o": 1, "q": 1},
}


class RollingForecaster:
    """Rolling-window one-step-ahead variance forecaster.

    :param returns: Scaled log-return series.
    :param model_type: 'GARCH', 'GJR-GARCH' or 'EGARCH'.
    :param window: Estimation window length.
    """

    def __init__(self, returns, model_type="GARCH", window=500):
        self.returns = returns.reset_index(drop=True)
        self.model_type = model_type
        self.window = window

    def run(self, step=10):
        """Execute rolling forecast, re-estimating every *step* observations."""
        spec = MODEL_SPECS[self.model_type]
        rows = []
        n = len(self.returns)

        for t in range(self.window, n - 1, step):
            train = self.returns.iloc[t - self.window : t]
            try:
                res = arch_model(train, **spec).fit(disp="off")
            except Exception:
                continue
            fc = res.forecast(horizon=1)
            rows.append(
                {
                    "t": t,
                    "variance_forecast": fc.variance.values[-1, 0],
                    "realized_variance": float(self.returns.iloc[t] ** 2),
                }
            )

        df = pd.DataFrame(rows)
        df["volatility_forecast"] = df["variance_forecast"] ** 0.5
        return df

    @staticmethod
    def mse(fc):
        """Mean squared error of variance forecasts."""
        return ((fc["variance_forecast"] - fc["realized_variance"]) ** 2).mean()

    @staticmethod
    def mae(fc):
        """Mean absolute error of volatility forecasts."""
        return (fc["volatility_forecast"] - fc["realized_variance"] ** 0.5).abs().mean()
