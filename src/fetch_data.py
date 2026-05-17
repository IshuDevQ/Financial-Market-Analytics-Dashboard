import yfinance as yf
import pandas as pd
from pathlib import Path


TICKERS = [
    "AAPL",
    "MSFT",
    "GOOGL",
    "AMZN",
    "NVDA",
    "TSLA",
    "JPM",
    "INFY.NS",
    "TCS.NS",
    "RELIANCE.NS",
]


def fetch_stock_data(
    tickers=None,
    start_date="2020-01-01",
    end_date=None,
    output_path="data/raw/stock_prices_raw.csv"
):
    """
    Downloads historical stock data for given tickers and saves it as a CSV file.
    """

    if tickers is None:
        tickers = TICKERS

    all_data = []

    print(f"Total tickers requested: {len(tickers)}")

    for ticker in tickers:
        print(f"Downloading data for {ticker}...")

        data = yf.download(
            ticker,
            start=start_date,
            end=end_date,
            progress=False,
            auto_adjust=False,
            group_by="column"
        )

        if data.empty:
            print(f"No data found for {ticker}")
            continue

        # If yfinance returns multi-level columns, flatten them safely.
        if isinstance(data.columns, pd.MultiIndex):
            data.columns = data.columns.get_level_values(0)

        data = data.reset_index()

        # Keep only the standard columns needed for this project.
        required_columns = ["Date", "Open", "High", "Low", "Close", "Adj Close", "Volume"]
        available_columns = [col for col in required_columns if col in data.columns]
        data = data[available_columns]

        data["Ticker"] = ticker

        all_data.append(data)
        print(f"Rows downloaded for {ticker}: {len(data)}")

    if not all_data:
        raise ValueError("No stock data was downloaded.")

    final_data = pd.concat(all_data, ignore_index=True)

    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    final_data.to_csv(output_path, index=False)

    print(f"Raw stock data saved to {output_path}")
    print("Tickers saved in raw file:", sorted(final_data["Ticker"].unique()))
    print("Total tickers saved:", final_data["Ticker"].nunique())

    return final_data


if __name__ == "__main__":
    fetch_stock_data()