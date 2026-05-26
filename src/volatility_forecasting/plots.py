"""Visualisation functions for the volatility forecasting pipeline."""

import matplotlib.pyplot as plt
import numpy as np
from scipy import stats


def plot_returns(dates, returns):
    """Time-series plot of log returns."""
    fig, ax = plt.subplots(figsize=(12, 4))
    ax.plot(dates, returns, linewidth=0.4, color="steelblue")
    ax.axhline(0, color="black", linewidth=0.5, linestyle="--")
    ax.set_title("NFLX Daily Log Returns")
    ax.set_ylabel("Log return")
    fig.tight_layout()
    return fig


def plot_conditional_volatility(dates, volatility, model_name="GARCH"):
    """Plot conditional volatility from a fitted model."""
    fig, ax = plt.subplots(figsize=(12, 4))
    ax.plot(dates, volatility, linewidth=0.6, color="darkorange")
    ax.set_title(f"Conditional Volatility — {model_name}")
    ax.set_ylabel("σ (%)")
    fig.tight_layout()
    return fig


def plot_forecast_vs_realized(fc_df, dates=None, model_name="GARCH"):
    """Overlay forecasted and realised variance."""
    fig, ax = plt.subplots(figsize=(12, 5))
    x = dates if dates is not None else fc_df["t"]
    ax.plot(
        x,
        fc_df["variance_forecast"],
        label="Forecast σ²",
        linewidth=0.8,
        color="crimson",
    )
    ax.plot(
        x,
        fc_df["realized_variance"],
        label="Realized r²",
        linewidth=0.4,
        alpha=0.5,
        color="steelblue",
    )
    ax.set_title(f"Rolling Variance Forecast vs Realised — {model_name}")
    ax.set_ylabel("Variance")
    ax.legend()
    fig.tight_layout()
    return fig


def plot_residuals_diagnostics(residuals, model_name="GARCH"):
    """Histogram and Q-Q plot of standardised residuals."""
    fig, axes = plt.subplots(1, 2, figsize=(12, 4))
    clean = residuals.dropna()

    axes[0].hist(clean, bins=50, density=True, alpha=0.7, color="steelblue")
    x = np.linspace(clean.min(), clean.max(), 200)
    axes[0].plot(x, stats.norm.pdf(x), "r-", linewidth=1.5, label="N(0,1)")
    axes[0].set_title(f"Standardised Residuals — {model_name}")
    axes[0].legend()

    stats.probplot(clean, dist="norm", plot=axes[1])
    axes[1].set_title("Q-Q Plot")
    fig.tight_layout()
    return fig


def plot_model_comparison(comparison_df):
    """Bar chart comparing AIC and BIC across models."""
    fig, axes = plt.subplots(1, 2, figsize=(10, 4))

    comparison_df["AIC"].plot(kind="bar", ax=axes[0], color="steelblue")
    axes[0].set_title("AIC (lower = better)")
    axes[0].set_ylabel("AIC")

    comparison_df["BIC"].plot(kind="bar", ax=axes[1], color="darkorange")
    axes[1].set_title("BIC (lower = better)")
    axes[1].set_ylabel("BIC")

    for ax in axes:
        ax.tick_params(axis="x", rotation=0)
    fig.tight_layout()
    return fig
