

# Financial Market Analytics Dashboard

An end-to-end financial analytics project that extracts historical stock market data, processes it using Python, stores structured data in SQLite, and presents interactive insights through a Streamlit dashboard.

## Live App

Add your deployed Streamlit app link here after deployment:

```text
https://your-app-name.streamlit.app
```

## Project Objective

The objective of this project is to analyze stock market performance using business-friendly financial metrics such as returns, volatility, moving averages, cumulative growth, and trend signals.

This project demonstrates practical skills in:

- Financial data analytics
- Python-based ETL pipeline development
- Data cleaning and transformation
- SQL database storage
- Interactive dashboard development
- Business insight generation

## Tech Stack

- Python
- Pandas
- NumPy
- yfinance
- SQLite
- SQLAlchemy
- Streamlit
- Plotly
- Matplotlib

## Dataset

Historical stock market data is collected using the `yfinance` Python library.

Selected stock tickers:

- AAPL
- MSFT
- GOOGL
- AMZN
- NVDA
- TSLA
- JPM
- INFY.NS
- TCS.NS
- RELIANCE.NS

The dataset contains historical OHLCV data:

- Open
- High
- Low
- Close
- Adjusted Close
- Volume

## Project Workflow

```text
Stock tickers
   ↓
Data extraction using yfinance
   ↓
Raw CSV storage
   ↓
Data cleaning using Pandas
   ↓
Financial metric calculation
   ↓
SQLite database storage
   ↓
Interactive Streamlit dashboard
```

## Features

### 1. Data Extraction

The project downloads historical stock price data for multiple equities using Python and saves the raw data in CSV format.

### 2. Data Cleaning

The raw data is cleaned and standardized by:

- Formatting column names
- Converting date columns
- Removing duplicate records
- Sorting data by ticker and date
- Handling missing values

### 3. Financial Metrics

The following financial metrics are calculated:

- Daily return
- Cumulative return
- 20-day moving average
- 50-day moving average
- 20-day rolling volatility
- Annualized volatility
- Bullish/Bearish trend signal

### 4. SQL Storage

The cleaned and processed datasets are loaded into a SQLite database with tables such as:

- `stock_prices`
- `stock_metrics`

### 5. Streamlit Dashboard

The dashboard provides interactive filters and visualizations for:

- Stock price movement
- Cumulative return comparison
- Moving average trend analysis
- Bullish/Bearish signal distribution
- Risk-return comparison
- Volatility comparison
- Stock-level summary table

## Dashboard Sections

### Market Overview

Shows stock-wise closing price trends and cumulative return comparison.

### Trend Analysis

Displays closing price, 20-day moving average, and 50-day moving average for selected stocks.

### Risk and Return Analysis

Compares stocks based on average return and annualized volatility.

### Stock Comparison Table

Summarizes latest close price, average daily return, cumulative return, volatility, and average trading volume.

## Folder Structure

```text
Financial-Market-Analytics-Dashboard/
│
├── dashboard/
│   └── app.py
│
├── data/
│   ├── raw/
│   └── processed/
│       └── stock_metrics.csv
│
├── database/
│
├── notebooks/
│
├── src/
│   ├── fetch_data.py
│   ├── clean_data.py
│   ├── calculate_metrics.py
│   ├── load_to_sql.py
│   └── main.py
│
├── README.md
├── requirements.txt
└── .gitignore
```

## How to Run Locally

Clone the repository:

```bash
git clone https://github.com/IshuDevQ/Financial-Market-Analytics-Dashboard.git
cd Financial-Market-Analytics-Dashboard
```

Create and activate a virtual environment:

```bash
python -m venv venv
source venv/bin/activate
```

For Windows:

```bash
venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the ETL pipeline:

```bash
python src/main.py
```

Run the Streamlit dashboard:

```bash
streamlit run dashboard/app.py
```

## Deployment

This app can be deployed using Streamlit Community Cloud.

Use the following deployment settings:

```text
Repository: IshuDevQ/Financial-Market-Analytics-Dashboard
Branch: main
Main file path: dashboard/app.py
```

The processed dataset below should be available in the repository so the deployed app can load data directly:

```text
data/processed/stock_metrics.csv
```

## Business Insights

This project helps users compare selected stocks using:

- Price trend behavior
- Long-term cumulative return
- Short-term and long-term moving averages
- Volatility-based risk analysis
- Risk-return positioning
- Bullish and bearish signal phases

## Resume Description

**Financial Market Analytics Dashboard | Python, SQL, Streamlit, Pandas**

- Built an end-to-end financial analytics pipeline using Python, Pandas, yfinance, and SQL to collect, clean, store, and analyze historical equity market data.
- Developed an interactive Streamlit dashboard to visualize stock price trends, cumulative returns, moving averages, volatility, and trend signals.
- Calculated financial metrics including daily returns, cumulative returns, 20-day and 50-day moving averages, rolling volatility, and annualized volatility.
- Designed risk-return comparison visuals to evaluate selected equities based on average returns and volatility.

## Future Improvements

- Add portfolio weight allocation
- Add Sharpe ratio and Value at Risk
- Add sector-wise stock comparison
- Add automated daily data refresh
- Add downloadable Excel reports
- Add forecasting models for trend analysis

## Author

Ishu Dev