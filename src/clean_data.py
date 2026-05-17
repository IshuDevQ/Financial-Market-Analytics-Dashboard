import pandas as pd
from pathlib import Path


def clean_stock_data(
    input_path="data/raw/stock_prices_raw.csv",
    output_path="data/processed/stock_prices_clean.csv"
):
    """
    Cleans raw stock price data and saves the cleaned file.
    """

    df = pd.read_csv(input_path)

    # Standardize column names
    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace(" ", "_")
    )

    # Rename adjusted close column
    if "adj_close" in df.columns:
        df.rename(columns={"adj_close": "adjusted_close"}, inplace=True)

    # Convert date column
    df["date"] = pd.to_datetime(df["date"])

    # Remove duplicate rows
    df.drop_duplicates(subset=["date", "ticker"], inplace=True)

    # Sort data
    df.sort_values(by=["ticker", "date"], inplace=True)

    # Remove rows with missing close price
    df.dropna(subset=["close"], inplace=True)

    # Save cleaned data
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_path, index=False)

    print(f"Cleaned stock data saved to {output_path}")

    return df


if __name__ == "__main__":
    clean_stock_data()