import pandas as pd
from sqlalchemy import create_engine
from pathlib import Path


def load_data_to_sql(
    prices_path="data/processed/stock_prices_clean.csv",
    metrics_path="data/processed/stock_metrics.csv",
    database_path="database/market_analytics.db"
):
    """
    Loads cleaned stock prices and calculated metrics into SQLite database.
    """

    Path(database_path).parent.mkdir(parents=True, exist_ok=True)

    engine = create_engine(f"sqlite:///{database_path}")

    prices_df = pd.read_csv(prices_path)
    metrics_df = pd.read_csv(metrics_path)

    prices_df.to_sql(
        "stock_prices",
        engine,
        if_exists="replace",
        index=False
    )

    metrics_df.to_sql(
        "stock_metrics",
        engine,
        if_exists="replace",
        index=False
    )

    print(f"Data loaded successfully into {database_path}")
    print("Tables created: stock_prices, stock_metrics")


if __name__ == "__main__":
    load_data_to_sql()