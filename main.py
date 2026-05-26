import os
import sys

# Ensure src/ is in the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), "src"))

from volatility_forecasting.data import DataLoader  # noqa: E402


def main():
    print("Starting Volatility Forecasting Data Pipeline...")

    # Initialize DataLoader for Netflix (NFLX) from 2002 to present (May 2026)
    loader = DataLoader(ticker="NFLX")

    try:
        # Download and process data
        df = loader.get_processed_data()

        print("\n[SUCCESS] Data successfully downloaded and preprocessed!")
        print(f"Ticker: {loader.ticker}")
        print(f"DataFrame Shape: {df.shape}")
        print(
            f"Date Range: from {df['date'].min().date()} to {df['date'].max().date()}"
        )

        print("\nFirst 5 rows:")
        print(df[["date", "close", "log_return"]].head())

        print("\nLast 5 rows:")
        print(df[["date", "close", "log_return"]].tail())

        # Simple verification checks
        assert "log_return" in df.columns, "log_return column missing!"
        assert not df["log_return"].isnull().any(), "NaN values found in log_return!"
        print("\n[VERIFICATION] All assertions passed successfully.")

    except Exception as e:
        print(f"\n[ERROR] Failed to run the pipeline: {e}")


if __name__ == "__main__":
    main()
