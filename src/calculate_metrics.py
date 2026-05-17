import pandas as pd
import numpy as np
from pathlib import Path


def calculate_stock_metrics(
    input_path="data/processed/stock_prices_clean.csv",
    output_path="data/processed/stock_metrics.csv"
):
    """
    Calculates financial metrics:
    - daily returns
    - cumulative returns
    - moving averages
    - volatility
    - trend signal
    """

    df = pd.read_csv(input_path)
    df["date"] = pd.to_datetime(df["date"])
    df["close"] = pd.to_numeric(df["close"], errors="coerce")

    df.sort_values(by=["ticker", "date"], inplace=True)

    metric_frames = []

    for ticker, group in df.groupby("ticker"):
        group = group.copy()

        # Daily return
        group["daily_return"] = group["close"].pct_change()

        # Cumulative return
        group["cumulative_return"] = (1 + group["daily_return"]).cumprod() - 1

        # Moving averages
        group["ma_20"] = group["close"].rolling(window=20).mean()
        group["ma_50"] = group["close"].rolling(window=50).mean()

        # Rolling volatility: 20-day volatility
        group["volatility_20d"] = group["daily_return"].rolling(window=20).std()

        # Annualized volatility
        group["annualized_volatility"] = group["volatility_20d"] * np.sqrt(252)

        # Trend signal
        group["trend_signal"] = np.where(
            group["ma_20"] > group["ma_50"],
            "Bullish",
            "Bearish"
        )

        metric_frames.append(group)

    final_df = pd.concat(metric_frames, ignore_index=True)

    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    final_df.to_csv(output_path, index=False)

    print(f"Stock metrics saved to {output_path}")

    return final_df


if __name__ == "__main__":
    calculate_stock_metrics()