

# ML-Powered Financial Market Analytics Dashboard

An end-to-end ML-powered financial analytics project that extracts historical stock market data, processes it using Python, stores structured data in SQLite, and presents interactive insights through a Streamlit dashboard.

The dashboard includes financial metric analysis, statistical anomaly detection, machine learning-based short-term forecasting, and automated financial insights.

## Live App

The deployed Streamlit dashboard is available here:

```text
https://financial-market-analytics-dashboard-xvibf3zdfcuacc3aetryf2.streamlit.app/
```

## Project Objective

The objective of this project is to analyze stock market performance using business-friendly financial metrics such as returns, volatility, moving averages, cumulative growth, trend signals, anomaly detection, and short-term forecasting.

This project demonstrates practical skills in:

- Financial data analytics
- Python-based ETL pipeline development
- Data cleaning and transformation
- SQL database storage
- Machine learning-based forecasting
- Statistical anomaly detection
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
- scikit-learn

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
Anomaly detection
   ↓
SQLite database storage
   ↓
ML-based forecasting and automated insights
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

### 4. Statistical Anomaly Detection

The dashboard detects unusual stock return movements using z-score based anomaly detection.

A daily return is marked as an anomaly when:

```text
|z-score| > 2.5
```

This helps identify unusual market movements for selected stocks.

### 5. ML-Based KPI Forecasting

The dashboard uses a Linear Regression model to forecast short-term closing prices.

The model uses time as the independent variable and closing price as the target variable.

Forecasting is available for selected stocks over short horizons such as:

- 7 days
- 14 days
- 21 days
- 30 days

### 6. SQL Storage

The cleaned and processed datasets are loaded into a SQLite database with tables such as:

- `stock_prices`
- `stock_metrics`

### 7. Streamlit Dashboard

The dashboard provides interactive filters and visualizations for:

- Stock price movement
- Cumulative return comparison
- Moving average trend analysis
- Bullish/Bearish signal distribution
- Risk-return comparison
- Volatility comparison
- Statistical anomaly detection
- ML-based closing price forecasting
- Automated financial insights
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

### Statistical Anomaly Detection

Detects unusual return movements using z-score based anomaly detection and displays anomaly counts, anomaly charts, and anomaly tables.

### ML-Based KPI Forecasting

Uses Linear Regression to forecast short-term closing price trends for selected stocks.

### Automated Financial Insights

Generates rule-based business insights using financial metrics such as cumulative return, volatility, anomaly count, and moving-average trend signals.

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

This app is deployed using Streamlit Community Cloud.

Deployment settings:

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
- Anomaly frequency
- Short-term forecasted closing price movement

## Machine Learning and Analytics Methods Used

### Linear Regression Forecasting

A Linear Regression model is used to forecast short-term closing prices based on historical price trends.

### Z-Score Anomaly Detection

Daily returns are standardized using z-scores. Large deviations from normal return behavior are flagged as anomalies.

### Rule-Based Automated Insights

Automated insights are generated using calculated financial indicators such as:

- Cumulative return
- Annualized volatility
- Trend signal
- Anomaly count

## Disclaimer

This dashboard is built for educational and exploratory financial analytics purposes only. It does not provide investment advice or trading recommendations.

## Future Improvements

- Add portfolio weight allocation
- Add Sharpe ratio and Value at Risk
- Add sector-wise stock comparison
- Add advanced forecasting models
- Add model performance evaluation metrics
- Add downloadable Excel reports
- Add automated daily data refresh

## Author

Ishu Dev