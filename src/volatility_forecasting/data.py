import numpy as np
import pandas as pd
import yfinance as yf


class DataLoader:
    """Class for loading and preprocessing financial market data.

    This class provides methods to download historical stock prices from Yahoo Finance
    and calculate log returns for volatility forecasting models.

    :param ticker: The stock ticker symbol (e.g., 'NFLX').
    :type ticker: str
    :param start_date: The start date for fetching data in 'YYYY-MM-DD' format.
    :type start_date: str
    :param end_date: The end date for fetching data in 'YYYY-MM-DD' format.
    :type end_date: str
    """

    def __init__(
        self, ticker: str = "NFLX", start_date: str = "2002-05-23", end_date: str = None
    ):
        """Initialize the DataLoader with ticker and date range."""
        self.ticker = ticker
        self.start_date = start_date
        self.end_date = end_date

    def download_data(self) -> pd.DataFrame:
        """Download historical market data using yfinance.

        Downloads historical daily price data for the specified ticker and date range.
        If `end_date` is not provided, downloads data up to the current date.

        :return: A DataFrame containing historical market data with dates as index.
        :rtype: pandas.DataFrame
        :raises ValueError: If downloading data fails or returns empty dataset.
        """
        try:
            # Download data using yfinance
            df = yf.download(
                tickers=self.ticker,
                start=self.start_date,
                end=self.end_date,
                progress=False,
            )
            if df.empty:
                raise ValueError(
                    f"No data for '{self.ticker}'. Check ticker & date range."
                )
            return df
        except Exception as e:
            raise ValueError(f"Failed to download data for {self.ticker}: {str(e)}")

    def calculate_log_returns(
        self, df: pd.DataFrame, price_column: str = "Close"
    ) -> pd.DataFrame:
        """Calculate log returns based on a price column.

        Computes log returns as the first difference of the log prices:
        log_return_t = ln(Price_t) - ln(Price_{t-1}).

        The resulting DataFrame contains a new column 'Log_Return' and the first row
        containing NaN is removed.

        :param df: The input DataFrame containing historical prices.
        :type df: pandas.DataFrame
        :param price_column: Price column name, defaults to 'Close'.
        :type price_column: str
        :return: DataFrame with 'Log_Return' column and NaN values removed.
        :rtype: pandas.DataFrame
        :raises KeyError: If the price_column is missing from the DataFrame.
        """
        df_copy = df.copy()

        # Handle yfinance MultiIndex column headers if present
        if isinstance(df_copy.columns, pd.MultiIndex):
            df_copy.columns = df_copy.columns.get_level_values(0)

        if price_column not in df_copy.columns:
            raise KeyError(
                f"Column '{price_column}' not found in the DataFrame. "
                f"Available columns: {list(df_copy.columns)}"
            )

        # Calculate log returns: ln(P_t / P_{t-1})
        df_copy["Log_Return"] = np.log(
            df_copy[price_column] / df_copy[price_column].shift(1)
        )

        # Ensure index has a name 'Date' so it becomes a 'date' column after resetting
        df_copy.index.name = "Date"

        # Reset index to make Date a regular column
        df_copy = df_copy.reset_index()

        # Format column names to lowercase and replace spaces with underscores
        df_copy.columns = [col.lower().replace(" ", "_") for col in df_copy.columns]

        # Drop the first row which will have NaN log return
        df_copy = df_copy.dropna(subset=["log_return"])

        return df_copy

    def get_processed_data(self) -> pd.DataFrame:
        """Retrieve and process historical data in a single pipeline.

        Downloads the data and calculates log returns, formatting the final DataFrame
        so it is ready for volatility modeling.

        :return: Preprocessed DataFrame containing prices and 'Log_Return' columns.
        :rtype: pandas.DataFrame
        """
        raw_data = self.download_data()
        processed_data = self.calculate_log_returns(raw_data)
        return processed_data
