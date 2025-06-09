import streamlit as st
import requests
import pandas as pd
import yfinance as yf

API_KEY = "ntuZmT0fG22CEhrJEekgNQ6NGsQkvqlE"


# ---------------------- API Functions ----------------------

def fetch_quote(symbol):
    url = f"https://financialmodelingprep.com/api/v3/profile/{symbol}?apikey={API_KEY}"
    response = requests.get(url)
    if response.status_code == 200 and response.json():
        return response.json()[0]
    return None

def fetch_profile(symbol):
    url = f"https://financialmodelingprep.com/api/v3/profile/{symbol}?apikey={API_KEY}"
    response = requests.get(url)
    if response.status_code == 200 and response.json():
        return response.json()[0]
    return None

def fetch_historical_data(symbol):
    url = f"https://financialmodelingprep.com/api/v3/historical-price-full/{symbol}?apikey={API_KEY}"
    response = requests.get(url)
    if response.status_code == 200 and "historical" in response.json():
        return response.json()["historical"]
    return []

def fetch_top_gainers():
    url = f"https://financialmodelingprep.com/api/v3/gainers?apikey={API_KEY}"
    return requests.get(url).json()

def fetch_top_losers():
    url = f"https://financialmodelingprep.com/api/v3/losers?apikey={API_KEY}"
    return requests.get(url).json()

def fetch_top_funds():
    url = f"https://financialmodelingprep.com/api/v3/etf/list?apikey={API_KEY}"
    return requests.get(url).json()[:10]  # Top 10 suggested ETFs

def fetch_benchmark_data(ticker="^GSPC"):
    data = yf.download(ticker, period="1mo")
    return data.reset_index()

def prepare_display(df):
    df = df.copy().reset_index(drop=True)
    df.index += 1
    df.index.name = "S.No."
    return df

# ---------------------- Streamlit App ----------------------
def api_data_fetch():
    st.title("📡 Live Stock Data Fetched from API")
    st.markdown("This section automatically fetches data for all symbols in your portfolio.")

    if "symbol_list" not in st.session_state or not st.session_state.symbol_list:
        st.warning("⚠️ No symbols found from Portfolio Manager Data. Please input investments first.")
        return

    symbols = st.session_state.symbol_list
    st.info(f"📦 Fetching data for: {', '.join(symbols)}")

    quote_data = []
    profile_data = []

    for symbol in symbols:
        quote = fetch_quote(symbol)
        profile = fetch_profile(symbol)
        history = fetch_historical_data(symbol)

        if quote and profile:
            quote_data.append({
                "Symbol": profile.get("symbol"),
                "Price": profile.get("price"),
                "Beta": profile.get("beta"),
                "Volume Avg": profile.get("volAvg"),
                "Market Cap": profile.get("mktCap"),
                "Last Dividend": profile.get("lastDiv"),
                "Range": profile.get("range"),
                "Change": profile.get("changes"),
                "Company Name": profile.get("companyName"),
                "Exchange": profile.get("exchange"),
                "Exchange Short Name": profile.get("exchangeShortName")
            })

        if profile:
            profile_data.append({
                "Symbol": profile["symbol"],
                "Company Name": profile["companyName"],
                "Industry": profile["industry"],
                "Sector": profile["sector"],
                "Website": profile["website"]
            })

        if history:
            df_history = pd.DataFrame(history)
            st.subheader(f"📉 Historical Data for {symbol}")
            st.dataframe(prepare_display(df_history.head(10)))

    if quote_data:
        st.subheader("📈 Quote Data")
        st.dataframe(prepare_display(pd.DataFrame(quote_data)))

    if profile_data:
        st.subheader("🏢 Profile Data")
        st.dataframe(prepare_display(pd.DataFrame(profile_data)))
        
    st.session_state.quote_data = quote_data

    # Top Gainers
    st.subheader("🚀 Top Gainers")
    gainers = fetch_top_gainers()
    st.dataframe(prepare_display(pd.DataFrame(gainers)))

    # Top Losers
    st.subheader("📉 Top Losers")
    losers = fetch_top_losers()
    st.dataframe(prepare_display(pd.DataFrame(losers)))

    # Suggested Top Funds
    st.subheader("💰 Suggested Top ETFs")
    funds = fetch_top_funds()
    st.dataframe(prepare_display(pd.DataFrame(funds)))

    # Benchmark Index (e.g., S&P 500)
    st.subheader("📊 Benchmark Data (S&P 500)")
    benchmark = fetch_benchmark_data()
    st.dataframe(prepare_display(benchmark.head(10)))

    # Store current prices in session_state for EDA use
    if quote_data:
        current_prices = {
            entry["Symbol"]: entry["Price"]
            for entry in quote_data
            if entry.get("Symbol") and entry.get("Price") is not None
        }
        st.session_state.api_prices = current_prices
        st.success("✅ Live stock prices stored for EDA module.")

        # Extract and display live prices separately
        st.subheader("💹 Live Stock Prices")
        live_prices = {
            entry["Symbol"]: entry["Price"]
            for entry in quote_data
            if entry.get("Symbol") and entry.get("Price") is not None
        }
        live_prices_df = pd.DataFrame.from_dict(live_prices, orient="index", columns=["Current Price (₹)"])
        st.dataframe(prepare_display(live_prices_df))