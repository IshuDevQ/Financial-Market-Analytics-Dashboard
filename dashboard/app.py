import sqlite3
from pathlib import Path

import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st
from sklearn.linear_model import LinearRegression


DATABASE_PATH = Path("database/market_analytics.db")
CSV_PATH = Path("data/processed/stock_metrics.csv")


st.set_page_config(
    page_title="ML-Powered Financial Market Analytics Dashboard",
    layout="wide"
)


@st.cache_data
def load_data():
    """
    Loads stock metrics data from SQLite database.
    Falls back to CSV if database is not found.
    """

    if DATABASE_PATH.exists():
        connection = sqlite3.connect(DATABASE_PATH)
        df = pd.read_sql_query("SELECT * FROM stock_metrics", connection)
        connection.close()
    else:
        df = pd.read_csv(CSV_PATH)

    df["date"] = pd.to_datetime(df["date"])

    return df


def generate_forecast(data, ticker, forecast_days):
    """
    Generates a simple short-term closing price forecast using Linear Regression.
    This is for educational and exploratory analysis only.
    """

    ticker_df = data[data["ticker"] == ticker].copy()
    ticker_df = ticker_df.dropna(subset=["close"])
    ticker_df = ticker_df.sort_values("date")

    if len(ticker_df) < 30:
        return None

    ticker_df["day_number"] = np.arange(len(ticker_df))

    X = ticker_df[["day_number"]]
    y = ticker_df["close"]

    model = LinearRegression()
    model.fit(X, y)

    future_days = np.arange(
        len(ticker_df),
        len(ticker_df) + forecast_days
    ).reshape(-1, 1)

    forecast_values = model.predict(future_days)

    last_date = ticker_df["date"].max()

    future_dates = pd.date_range(
        start=last_date + pd.Timedelta(days=1),
        periods=forecast_days,
        freq="D"
    )

    forecast_df = pd.DataFrame({
        "date": future_dates,
        "ticker": ticker,
        "forecasted_close": forecast_values
    })

    return forecast_df


def generate_automated_insights(summary_table, anomaly_summary):
    """
    Generates rule-based financial insights using returns, volatility,
    trend behavior, and anomaly count.
    """

    insights = []

    if summary_table.empty:
        return ["No data available to generate insights."]

    best_return_row = summary_table.sort_values(
        "max_cumulative_return",
        ascending=False
    ).iloc[0]

    highest_vol_row = summary_table.sort_values(
        "average_annualized_volatility",
        ascending=False
    ).iloc[0]

    lowest_vol_row = summary_table.sort_values(
        "average_annualized_volatility",
        ascending=True
    ).iloc[0]

    insights.append(
        f"{best_return_row['ticker']} shows the highest cumulative return "
        f"within the selected period, indicating stronger historical performance."
    )

    insights.append(
        f"{highest_vol_row['ticker']} has the highest annualized volatility, "
        f"suggesting a higher-risk price movement profile."
    )

    insights.append(
        f"{lowest_vol_row['ticker']} has the lowest annualized volatility, "
        f"indicating relatively more stable movement compared to the selected stocks."
    )

    if not anomaly_summary.empty:
        most_anomalies = anomaly_summary.sort_values(
            "anomaly_count",
            ascending=False
        ).iloc[0]

        if most_anomalies["anomaly_count"] > 0:
            insights.append(
                f"{most_anomalies['ticker']} has the highest number of detected anomaly days, "
                f"which may indicate unusual return movements during the selected period."
            )

    bullish_count = summary_table["latest_trend_signal"].eq("Bullish").sum()
    bearish_count = summary_table["latest_trend_signal"].eq("Bearish").sum()

    insights.append(
        f"Among the selected stocks, {bullish_count} are currently classified as Bullish "
        f"and {bearish_count} are classified as Bearish based on the 20-day and 50-day moving average signal."
    )

    return insights


df = load_data()

st.title("ML-Powered Financial Market Analytics Dashboard")

st.markdown(
    """
    This dashboard analyzes historical stock performance using financial metrics,
    machine learning-based forecasting, statistical anomaly detection, and automated financial insights.
    """
)

st.info(
    "Disclaimer: Forecasting and anomaly detection are for educational and exploratory analysis only. "
    "This dashboard does not provide investment advice."
)


# Sidebar filters
st.sidebar.header("Filters")

tickers = sorted(df["ticker"].unique())
st.sidebar.caption(f"Available stocks: {len(tickers)}")

selected_tickers = st.sidebar.multiselect(
    "Select stocks",
    options=tickers,
    default=tickers
)

if not selected_tickers:
    st.sidebar.warning("Please select at least one stock.")
    st.stop()

min_date = df["date"].min()
max_date = df["date"].max()

selected_date_range = st.sidebar.date_input(
    "Select date range",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)

if len(selected_date_range) == 2:
    start_date, end_date = selected_date_range
    filtered_df = df[
        (df["ticker"].isin(selected_tickers)) &
        (df["date"] >= pd.to_datetime(start_date)) &
        (df["date"] <= pd.to_datetime(end_date))
    ]
else:
    filtered_df = df[df["ticker"].isin(selected_tickers)]


if filtered_df.empty:
    st.warning("No data available for the selected filters.")
    st.write("Available tickers in data:", tickers)
    st.write("Selected tickers:", selected_tickers)
    st.write("Data date range:", df["date"].min(), "to", df["date"].max())
    st.stop()


# KPI calculations
average_daily_return = filtered_df["daily_return"].mean()
average_volatility = filtered_df["annualized_volatility"].mean()
average_volume = filtered_df["volume"].mean()

best_stock = (
    filtered_df.groupby("ticker")["cumulative_return"]
    .max()
    .sort_values(ascending=False)
    .index[0]
)

total_anomalies = filtered_df[filtered_df["is_anomaly"] == "Anomaly"].shape[0]

col1, col2, col3, col4, col5 = st.columns(5)

col1.metric("Average Daily Return", f"{average_daily_return:.2%}")
col2.metric("Average Annualized Volatility", f"{average_volatility:.2%}")
col3.metric("Average Volume", f"{average_volume:,.0f}")
col4.metric("Best Performing Stock", best_stock)
col5.metric("Detected Anomaly Days", total_anomalies)


st.divider()


# Section 1: Market Overview
st.header("1. Market Overview")

fig_close = px.line(
    filtered_df,
    x="date",
    y="close",
    color="ticker",
    title="Closing Price Over Time"
)

st.plotly_chart(fig_close, use_container_width=True)

returns_by_ticker = (
    filtered_df.groupby("ticker", as_index=False)["cumulative_return"]
    .max()
    .sort_values("cumulative_return", ascending=False)
)

fig_returns = px.bar(
    returns_by_ticker,
    x="ticker",
    y="cumulative_return",
    title="Maximum Cumulative Return by Stock",
    text_auto=".2%"
)

st.plotly_chart(fig_returns, use_container_width=True)


st.divider()


# Section 2: Trend Analysis
st.header("2. Trend Analysis")

single_ticker = st.selectbox(
    "Select one stock for moving average analysis",
    options=tickers
)

trend_df = filtered_df[filtered_df["ticker"] == single_ticker]

fig_ma = px.line(
    trend_df,
    x="date",
    y=["close", "ma_20", "ma_50"],
    title=f"Price and Moving Averages: {single_ticker}"
)

st.plotly_chart(fig_ma, use_container_width=True)

trend_count = (
    filtered_df["trend_signal"]
    .value_counts()
    .reset_index()
)

trend_count.columns = ["trend_signal", "count"]

fig_signal = px.pie(
    trend_count,
    names="trend_signal",
    values="count",
    title="Bullish vs Bearish Signal Distribution",
    hole=0.4
)

st.plotly_chart(fig_signal, use_container_width=True)


st.divider()


# Section 3: Risk and Return Analysis
st.header("3. Risk and Return Analysis")

risk_return = (
    filtered_df.groupby("ticker", as_index=False)
    .agg(
        average_daily_return=("daily_return", "mean"),
        average_annualized_volatility=("annualized_volatility", "mean"),
        maximum_cumulative_return=("cumulative_return", "max")
    )
)

fig_risk_return = px.scatter(
    risk_return,
    x="average_annualized_volatility",
    y="average_daily_return",
    size="maximum_cumulative_return",
    color="ticker",
    hover_name="ticker",
    title="Risk-Return Comparison"
)

st.plotly_chart(fig_risk_return, use_container_width=True)

fig_volatility = px.bar(
    risk_return.sort_values("average_annualized_volatility", ascending=False),
    x="ticker",
    y="average_annualized_volatility",
    title="Average Annualized Volatility by Stock",
    text_auto=".2%"
)

st.plotly_chart(fig_volatility, use_container_width=True)


st.divider()


# Section 4: Stock Comparison
st.header("4. Stock Comparison Table")

summary_table = (
    filtered_df.sort_values("date")
    .groupby("ticker", as_index=False)
    .agg(
        latest_close=("close", "last"),
        average_daily_return=("daily_return", "mean"),
        max_cumulative_return=("cumulative_return", "max"),
        average_annualized_volatility=("annualized_volatility", "mean"),
        average_volume=("volume", "mean"),
        latest_trend_signal=("trend_signal", "last")
    )
)

st.dataframe(
    summary_table,
    use_container_width=True
)


st.divider()


# Section 5: Statistical Anomaly Detection
st.header("5. Statistical Anomaly Detection")

st.markdown(
    """
    Anomalies are detected using z-scores on daily returns.  
    A day is marked as an anomaly when the absolute z-score is greater than 2.5.
    """
)

anomaly_df = filtered_df[filtered_df["is_anomaly"] == "Anomaly"].copy()

anomaly_summary = (
    anomaly_df.groupby("ticker", as_index=False)
    .size()
    .rename(columns={"size": "anomaly_count"})
)

all_ticker_summary = pd.DataFrame({"ticker": selected_tickers})
anomaly_summary = all_ticker_summary.merge(
    anomaly_summary,
    on="ticker",
    how="left"
).fillna({"anomaly_count": 0})

fig_anomaly_count = px.bar(
    anomaly_summary.sort_values("anomaly_count", ascending=False),
    x="ticker",
    y="anomaly_count",
    title="Detected Anomaly Days by Stock",
    text_auto=True
)

st.plotly_chart(fig_anomaly_count, use_container_width=True)

anomaly_ticker = st.selectbox(
    "Select stock for anomaly visualization",
    options=selected_tickers
)

anomaly_chart_df = filtered_df[filtered_df["ticker"] == anomaly_ticker].copy()
anomaly_points = anomaly_chart_df[anomaly_chart_df["is_anomaly"] == "Anomaly"]

fig_anomaly = px.line(
    anomaly_chart_df,
    x="date",
    y="daily_return",
    title=f"Daily Returns and Anomaly Points: {anomaly_ticker}"
)

if not anomaly_points.empty:
    fig_anomaly.add_scatter(
        x=anomaly_points["date"],
        y=anomaly_points["daily_return"],
        mode="markers",
        name="Anomaly"
    )

st.plotly_chart(fig_anomaly, use_container_width=True)

if anomaly_df.empty:
    st.success("No anomaly days detected for the selected filters.")
else:
    st.subheader("Anomaly Table")
    st.dataframe(
        anomaly_df[
            [
                "date",
                "ticker",
                "close",
                "daily_return",
                "return_z_score",
                "volume"
            ]
        ].sort_values("return_z_score", ascending=False),
        use_container_width=True
    )


st.divider()


# Section 6: ML-Based KPI Forecasting
st.header("6. ML-Based KPI Forecasting")

st.markdown(
    """
    This section uses a simple Linear Regression model to forecast short-term closing prices.
    The model uses time as the independent variable and closing price as the target variable.
    """
)

forecast_col1, forecast_col2 = st.columns(2)

with forecast_col1:
    forecast_ticker = st.selectbox(
        "Select stock for forecasting",
        options=selected_tickers
    )

with forecast_col2:
    forecast_days = st.slider(
        "Forecast horizon in days",
        min_value=7,
        max_value=30,
        value=14,
        step=7
    )

forecast_df = generate_forecast(filtered_df, forecast_ticker, forecast_days)

if forecast_df is None:
    st.warning("Not enough data available for forecasting.")
else:
    historical_forecast_df = filtered_df[
        filtered_df["ticker"] == forecast_ticker
    ][["date", "close"]].copy()

    historical_forecast_df.rename(columns={"close": "price"}, inplace=True)
    historical_forecast_df["type"] = "Historical"

    future_forecast_df = forecast_df.rename(
        columns={"forecasted_close": "price"}
    )[["date", "price"]]

    future_forecast_df["type"] = "Forecast"

    combined_forecast_df = pd.concat(
        [historical_forecast_df, future_forecast_df],
        ignore_index=True
    )

    fig_forecast = px.line(
        combined_forecast_df,
        x="date",
        y="price",
        color="type",
        title=f"Closing Price Forecast: {forecast_ticker}"
    )

    st.plotly_chart(fig_forecast, use_container_width=True)

    st.subheader("Forecasted Values")
    st.dataframe(forecast_df, use_container_width=True)


st.divider()


# Section 7: Automated Financial Insights
st.header("7. Automated Financial Insights")

insights = generate_automated_insights(summary_table, anomaly_summary)

for insight in insights:
    st.write(f"- {insight}")

st.markdown(
    """
    These insights are generated using rule-based logic from financial metrics such as
    cumulative return, volatility, anomaly count, and moving-average trend signals.
    """
)