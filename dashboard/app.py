import sqlite3
from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st


DATABASE_PATH = Path("database/market_analytics.db")


st.set_page_config(
    page_title="Financial Market Analytics Dashboard",
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
        df = pd.read_csv("data/processed/stock_metrics.csv")

    df["date"] = pd.to_datetime(df["date"])

    return df


df = load_data()

st.title("Financial Market Analytics Dashboard")

st.markdown(
    """
    This dashboard analyzes historical stock performance using financial metrics such as
    daily returns, cumulative returns, moving averages, volatility, and trend signals.
    """
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
latest_data = (
    filtered_df.sort_values("date")
    .groupby("ticker")
    .tail(1)
)

average_daily_return = filtered_df["daily_return"].mean()
average_volatility = filtered_df["annualized_volatility"].mean()
average_volume = filtered_df["volume"].mean()
best_stock = (
    filtered_df.groupby("ticker")["cumulative_return"]
    .max()
    .sort_values(ascending=False)
    .index[0]
)

col1, col2, col3, col4 = st.columns(4)

col1.metric("Average Daily Return", f"{average_daily_return:.2%}")
col2.metric("Average Annualized Volatility", f"{average_volatility:.2%}")
col3.metric("Average Volume", f"{average_volume:,.0f}")
col4.metric("Best Performing Stock", best_stock)


st.divider()


# Page section 1: Market Overview
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


# Page section 2: Trend Analysis
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


# Page section 3: Risk and Return Analysis
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


# Page section 4: Stock Comparison
st.header("4. Stock Comparison Table")

summary_table = (
    filtered_df.groupby("ticker", as_index=False)
    .agg(
        latest_close=("close", "last"),
        average_daily_return=("daily_return", "mean"),
        max_cumulative_return=("cumulative_return", "max"),
        average_annualized_volatility=("annualized_volatility", "mean"),
        average_volume=("volume", "mean")
    )
)

st.dataframe(
    summary_table,
    use_container_width=True
)


st.divider()


# Business insights
st.header("Business Insights")

st.markdown(
    f"""
    - The dashboard compares selected stocks using price trends, cumulative returns, and volatility.
    - **{best_stock}** shows the highest cumulative return within the selected period.
    - The risk-return scatter plot helps compare stocks based on average return and annualized volatility.
    - Moving average trends help identify bullish and bearish phases in stock price behavior.
    """
)