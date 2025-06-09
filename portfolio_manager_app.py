#portfolio_manager_app.py
import streamlit as st
from datetime import date

def portfolio_input():
    st.title("💼 Portfolio Manager Data Input")
    st.markdown("Use the form below to input details about your investments. You can add multiple stocks using the **➕ Add Another Investment** button.")
    st.markdown("---")

    # Initialize portfolio_data if it doesn't exist
    if "portfolio_data" not in st.session_state:
        st.session_state.portfolio_data = []

    # If the portfolio is empty when the app loads, add one default empty investment
    if not st.session_state.portfolio_data:
        st.session_state.portfolio_data.append({
            "Symbol": None,
            "Company": None,
            "Type": None,
            "Sector": None,
            "Shares": 0,
            "Buy Price": None,
            "Buy Date": None
        })

    # Include None as the first option for select boxes to represent "null"
    symbol_options = [None, 'AAPL', 'GOOGL', 'TSLA', 'MSFT']
    company_options = {
        'AAPL': 'Apple Inc.',
        'GOOGL': 'Alphabet Inc.',
        'TSLA': 'Tesla Inc.',
        'MSFT': 'Microsoft Corp.'
    }
    company_options[None] = "Select Company"

    type_options = [None, 'Stock', 'ETF', 'Mutual Fund']
    sector_options = [None, 'Technology', 'Finance', 'Healthcare', 'Energy', 'IT', 'Consumer Goods']

    deleted_item_flag = False 

    for i, data in enumerate(st.session_state.portfolio_data):
        with st.expander(f"📁 Investment {i+1}", expanded=True):
            current_symbol_index = symbol_options.index(data["Symbol"]) if data["Symbol"] in symbol_options else 0
            symbol = st.selectbox(f"Symbol (Investment {i+1})", symbol_options, index=current_symbol_index, key=f"symbol_{i}")

            company = company_options.get(symbol, "") if symbol else ""

            current_type_index = type_options.index(data["Type"]) if data["Type"] in type_options else 0
            investment_type = st.selectbox(f"Investment Type (Investment {i+1})", type_options, index=current_type_index, key=f"type_{i}")

            current_sector_index = sector_options.index(data["Sector"]) if data["Sector"] in sector_options else 0
            sector = st.selectbox(f"Sector (Investment {i+1})", sector_options, index=current_sector_index, key=f"sector_{i}")

            shares = st.number_input(f"Number of Shares (Investment {i+1})", min_value=0, value=data.get("Shares") or 0, step=1, key=f"shares_{i}")
            buy_price = st.number_input(f"Buy Price (₹) (Investment {i+1})", min_value=0.0, value=data.get("Buy Price") or 0.0, step=0.1, key=f"price_{i}")
            buy_date = st.date_input(f"Buy Date (Investment {i+1})", value=data.get("Buy Date") or date.today(), key=f"date_{i}")

            if st.button(f"🖑️ Delete Investment {i+1}", key=f"delete_{i}"):
                del st.session_state.portfolio_data[i]
                deleted_item_flag = True
                st.rerun()

            if not deleted_item_flag: 
                st.session_state.portfolio_data[i] = {
                    "Symbol": symbol,
                    "Company": company,
                    "Type": investment_type,
                    "Sector": sector,
                    "Shares": shares,
                    "Buy Price": buy_price,
                    "Buy Date": buy_date
                }

    # Extract and store unique symbols for API data fetch usage
    valid_symbols = [entry["Symbol"] for entry in st.session_state.portfolio_data if entry["Symbol"]]
    st.session_state.symbol_list = list(set(valid_symbols))

    if st.button("➕ Add Another Investment"):
        st.session_state.portfolio_data.append({
            "Symbol": None,
            "Company": None,
            "Type": None,
            "Sector": None,
            "Shares": 0,
            "Buy Price": None,
            "Buy Date": None
        })
        st.rerun()

    st.markdown("---")
    if st.session_state.portfolio_data:
        st.subheader("📊 Your Portfolio Summary")
        st.dataframe(st.session_state.portfolio_data)
    else:
        st.info("No investments added yet. Click '➕ Add Another Investment' to begin!")