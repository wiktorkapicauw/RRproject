"""
Volatility models module.

Contains the VolatilityModel class for fitting GARCH-family models
and running basic diagnostics.
"""

import pandas as pd
from arch import arch_model
from statsmodels.stats.diagnostic import acorr_ljungbox


class VolatilityModel:
    """Fits a GARCH-type model and provides diagnostic methods.

    Supported model types: 'GARCH', 'GJR-GARCH', 'EGARCH'.

    Example usage:
        model = VolatilityModel(returns, model_type='GARCH')
        model.fit()
        print(model.get_aic_bic())
    """

    def __init__(self, returns: pd.Series, model_type: str = "GARCH"):
        """Set up the model with return data and model type."""
        self.returns = returns
        self.model_type = model_type
        self.result = None  # will be filled after calling fit()

    def fit(self):
        """Fit the model to the return data."""
        if self.model_type == "GARCH":
            model = arch_model(self.returns, vol="GARCH", p=1, o=0, q=1)

        elif self.model_type == "GJR-GARCH":
            # o=1 adds the leverage (asymmetry) term
            model = arch_model(self.returns, vol="GARCH", p=1, o=1, q=1)

        elif self.model_type == "EGARCH":
            model = arch_model(self.returns, vol="EGARCH", p=1, o=1, q=1)

        else:
            raise ValueError(f"Unknown model type: {self.model_type}")

        self.result = model.fit(disp="off")

    def get_aic_bic(self) -> dict:
        """Return AIC, BIC and log-likelihood of the fitted model."""
        if self.result is None:
            raise RuntimeError("You need to call fit() first.")

        return {
            "model": self.model_type,
            "AIC": round(self.result.aic, 2),
            "BIC": round(self.result.bic, 2),
            "LogLikelihood": round(self.result.loglikelihood, 2),
        }

    def get_standardized_residuals(self) -> pd.Series:
        """Return standardized residuals (residuals divided by conditional volatility)."""
        if self.result is None:
            raise RuntimeError("You need to call fit() first.")

        return self.result.resid / self.result.conditional_volatility

    def ljung_box_test(self, lags: list = None) -> pd.DataFrame:
        """Run Ljung-Box test to check if residuals still have autocorrelation.

        A p-value below 0.05 means the model did not capture all patterns.
        """
        if lags is None:
            lags = [5, 10, 15]

        residuals = self.get_standardized_residuals().dropna()
        return acorr_ljungbox(residuals, lags=lags, return_df=True)


def compare_models(returns: pd.Series) -> pd.DataFrame:
    """Fit GARCH, GJR-GARCH and EGARCH on the same data and compare them.

    Returns a table sorted by AIC (lower is better).
    """
    results = []

    for model_type in ["GARCH", "GJR-GARCH", "EGARCH"]:
        model = VolatilityModel(returns, model_type=model_type)
        model.fit()
        results.append(model.get_aic_bic())

    df = pd.DataFrame(results).set_index("model")
    return df.sort_values("AIC")
