import streamlit as st

def home():
    st.title("Wealth Management Portfolio Dashboard")
    st.markdown("---")

    st.subheader("Overview")
    st.write("""
    Welcome to your integrated wealth management assistant. This dashboard is designed to help 
    investors and analysts track, evaluate, and improve portfolio performance with live data, 
    automated insights, and professional visualizations.
    """)

    st.subheader("Key Features")
    st.markdown("""
    - **Portfolio Input Manager** – Add or update holdings including symbol, shares, buy price, and type.
    - **Live Market Data** – Fetch real-time prices and financial metrics via Financial Modeling Prep API.
    - **EDA & Data Transformation** – Perform sectoral breakdowns, tax estimates, and return analysis.
    - **Risk Profiling & Alerts** – View metrics like beta, standard deviation, diversification index, and allocation ratios.
    - **Interactive Visualizations** – Explore charts including return breakdowns, tax impact, CAPM estimates, and sector exposure.
    - **Power BI Dashboard** – Embedded report for real-time business-level portfolio view.
    - **AI Chat Assistant** – Personalized chatbot powered by Groq’s LLaMA 3 to answer portfolio questions.
    - **PDF Report Generator** – Create downloadable summaries with portfolio data, visualizations, and chatbot responses.
    """)

    st.subheader("Objective")
    st.write("""
    This tool is intended to simulate a real-world investment dashboard for educational or professional use, 
    combining manual inputs, real-time market feeds, financial modeling, and AI-driven insights into one unified platform.
    """)

    st.markdown("---")
    st.caption("Built using Streamlit · Financial Modeling Prep API · Groq LLaMA 3 · Power BI Embedded")
