import streamlit as st
import pandas as pd
from datetime import datetime
import yfinance as yf
from api_data_app import fetch_top_gainers, fetch_top_losers, fetch_top_funds, fetch_quote
import os

def eda_transform():
    st.title("🔍 Portfolio Analysis & EDA")
    st.markdown("This section calculates key financial insights from your portfolio. Each result is backed by the formula used to compute it.")

    # Pre-check
    if "portfolio_data" not in st.session_state or "api_prices" not in st.session_state or "quote_data" not in st.session_state:
        st.warning("⚠️ Please enter portfolio data, fetch live stock prices, and load quote data before running EDA.")
        return

    portfolio = st.session_state.portfolio_data
    prices = st.session_state.api_prices
    quote_data = st.session_state.quote_data  # Fetch quote data from session state

    df = pd.DataFrame(portfolio)
    df = df[df["Symbol"].notnull()]

    quote_data_df = pd.DataFrame(quote_data)
    df = pd.merge(df, quote_data_df[['Symbol', 'Beta']], on='Symbol', how='left')

    # 1. Total Holding Value
    st.subheader("💼 Total Portfolio Value")
    st.markdown("**Formula:** Total Holding Value = Quantity × Current Price")
    df["Current Price"] = df["Symbol"].map(prices)
    df["Total Holding Value"] = df["Shares"] * df["Current Price"]
    st.write(f"**Total Holding Value:** ₹ {df['Total Holding Value'].sum():,.2f}")
    display_df = df[["Symbol", "Company", "Shares", "Current Price", "Total Holding Value"]].copy()
    display_df.index += 1
    st.dataframe(display_df)

    # 2. Estimated Tax Calculation
    st.subheader("🧾 Estimated Capital Gains Tax")
    st.markdown("**Formula:** Capital Gain = (Current Price - Purchase Price) × Quantity")
    st.markdown("**Estimated Tax Formula:** Estimated Tax = Capital Gain × Tax Rate")
    TAX_RATE = 0.15
    df["Capital Gain"] = (df["Current Price"] - df["Buy Price"]) * df["Shares"]
    df["Estimated Tax"] = df["Capital Gain"] * TAX_RATE
    st.write(f"**Total Estimated Tax:** ₹ {df['Estimated Tax'].sum():,.2f}")
    display_df = df[["Symbol", "Capital Gain", "Estimated Tax"]].copy()
    display_df.index += 1
    st.dataframe(display_df)

    # 3. Categorized Holdings (by Sector and Company)
    st.subheader("🏢 Categorized Holdings Overview")
    categorized = df[["Symbol", "Company", "Sector", "Shares", "Total Holding Value"]].copy()
    categorized.index += 1
    st.dataframe(categorized)

    st.subheader("🏙️ Holdings by Company")
    company_group = df.groupby("Company")["Total Holding Value"].sum().reset_index()
    company_group.index += 1
    st.dataframe(company_group)

    # 4. Returns by Investment Type
    st.subheader("📊 Return Percentage Calculation")
    st.markdown("**Formula:** Return (%) = ((Current Price - Buy Price) / Buy Price) × 100")
    df["Return (%)"] = ((df["Current Price"] - df["Buy Price"]) / df["Buy Price"]) * 100
    returns_df = df[["Symbol", "Company", "Current Price", "Buy Price", "Return (%)"]].copy()
    returns_df.index += 1
    st.dataframe(returns_df)

    # 5. Expected Return Estimation
    risk_free_rate = 0.04  
    expected_market_return = 0.10  
    df["Expected Return (CAPM)"] = risk_free_rate + df["Beta"] * (expected_market_return - risk_free_rate)
    df["Expected Return (%)"] = (df["Capital Gain"] / (df["Buy Price"] * df["Shares"])) * 100
    expected_df = df[["Symbol", "Buy Price", "Current Price", "Capital Gain", "Expected Return (%)", "Expected Return (CAPM)"]].copy()
    expected_df.index += 1
    st.subheader("📈 Expected Returns")
    st.markdown("**Formula:** Expected Return (CAPM) = Risk-Free Rate + Beta × (Market Return - Risk-Free Rate)")
    st.markdown("**Formula:** Expected Return (%) = (Capital Gain / (Buy Price × Shares)) × 100")
    st.dataframe(expected_df)

    # 6. Cumulative Return vs Benchmark (S&P 500)
    symbols = st.session_state.get("symbol_list", [])
    if not symbols:
        st.warning("No stock symbols provided from Portfolio Manager.")
        st.stop()

    benchmark_symbol = "^GSPC"
    benchmark_data = yf.download(benchmark_symbol, start="2023-11-23", end="2025-06-01")
    benchmark_data.reset_index(inplace=True)
    benchmark_data = benchmark_data[['Date', 'Close']]
    benchmark_data.columns = ['date', 'sp500_close']
    benchmark_data['date'] = pd.to_datetime(benchmark_data['date'])
    benchmark_data['sp500_cum_return_pct'] = (
        (benchmark_data['sp500_close'] - benchmark_data['sp500_close'].iloc[0]) / 
        benchmark_data['sp500_close'].iloc[0]
    ).mul(100).round(2)

    merged_all = benchmark_data[['date', 'sp500_cum_return_pct']].copy()

    for symbol in symbols:
        stock_data = yf.download(symbol, start="2023-11-23", end="2025-06-01")
        stock_data.reset_index(inplace=True)
        stock_data = stock_data[['Date', 'Close']]
        stock_data.columns = ['date', f'{symbol.lower()}_close']
        stock_data['date'] = pd.to_datetime(stock_data['date'])
        stock_data[f'{symbol.lower()}_cum_return_pct'] = (
            (stock_data[f'{symbol.lower()}_close'] - stock_data[f'{symbol.lower()}_close'].iloc[0]) /
            stock_data[f'{symbol.lower()}_close'].iloc[0]
        ).mul(100).round(2)
        return_data = stock_data[['date', f'{symbol.lower()}_cum_return_pct']]
        merged_all = pd.merge(merged_all, return_data, on='date', how='inner')

    st.subheader("📊 Cumulative Return Comparison")
    st.markdown("**Formula:** Cumulative Return (%) = ((Current Price - Starting Price) / Starting Price) × 100")
    cum_df = merged_all.tail().copy()
    cum_df.index += 1
    st.dataframe(cum_df)

    # Store merged_all in session_state
    st.session_state.merged_all = merged_all

    # 7. Top Gainers and Losers (Fetched from API)
    st.subheader("🚀 Top Gainers and 📉 Top Losers")
    gainers_raw = fetch_top_gainers()
    losers_raw = fetch_top_losers()

    top_5_gainers = pd.DataFrame(gainers_raw)[["ticker", "changesPercentage"]].head(5).copy()
    top_5_gainers.index += 1
    st.write("**Top Gainers**")
    st.dataframe(top_5_gainers)

    top_5_losers = pd.DataFrame(losers_raw)[["ticker", "changesPercentage"]].head(5).copy()
    top_5_losers.index += 1
    st.write("**Top Losers**")
    st.dataframe(top_5_losers)

    st.session_state.top_5_gainers = top_5_gainers
    st.session_state.top_5_losers = top_5_losers

    # 8. Suggested Top Funds (ETFs from API)
    st.subheader("💰 Suggested Top Funds")
    funds = fetch_top_funds()
    top_funds = pd.DataFrame(funds).copy()
    top_funds.index += 1
    st.dataframe(top_funds)

    st.session_state.top_funds = top_funds

    # Final clean DataFrame
    st.session_state.eda_df = df

