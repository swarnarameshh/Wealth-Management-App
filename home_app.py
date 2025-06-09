#home
import streamlit as st

def home():
    st.title("💰 Wealth Management Portfolio Dashboard")
    st.markdown("---")

    st.subheader("📊 Overview")
    st.write("""
    Welcome to your all-in-one wealth management assistant! This interactive dashboard helps 
    portfolio managers and individual investors effectively track, analyze, and visualize 
    their investments with real-time data and rich analytics.
    """)

    st.subheader("✨ Key Features")
    st.markdown("""
    - 📝 **Portfolio Manager Data Input**: Enter investment details such as symbol, shares, buy price, etc.
    - 🔄 **Live API Data Fetching**: Get real-time market data using Financial Modeling Prep API.
    - 🧮 **Data Transformation & EDA**: Analyze performance, calculate returns & taxes, and segment by sector/type.
    - 📈 **Interactive Visualizations**: Gain insights via dynamic charts (matplotlib/seaborn).
    - 🖥️ **Dashboard Integration**: Use Streamlit and view live-updating dashboards.
    """)

    st.subheader("🎯 Objective")
    st.write("""
    The aim of this dashboard is to simulate real-world portfolio management by 
    combining live financial data with user inputs to generate actionable insights.
    """)


    st.markdown("---")
    st.caption("Built using Streamlit · Powered by Financial Modeling Prep · Integrated with Power BI")