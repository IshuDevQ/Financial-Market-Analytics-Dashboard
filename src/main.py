from fetch_data import fetch_stock_data
from clean_data import clean_stock_data
from calculate_metrics import calculate_stock_metrics
from load_to_sql import load_data_to_sql


def run_pipeline():
    print("Starting Financial Market Analytics Pipeline...")

    fetch_stock_data()
    clean_stock_data()
    calculate_stock_metrics()
    load_data_to_sql()

    print("Pipeline completed successfully.")


if __name__ == "__main__":
    run_pipeline()