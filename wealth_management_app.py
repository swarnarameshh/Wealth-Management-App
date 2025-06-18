import streamlit as st
from streamlit_option_menu import option_menu

# Import all app modules
from home_app import home
from portfolio_manager_app import portfolio_input
from api_data_app import api_data_fetch
from eda_transform_app import eda_transform
from data_visualization_app import data_visualization
from power_bi_app import power_bi_dashboard
from streamlit_dashboard_app import streamlit_dashboard
from portfolio_chatbot_app import portfolio_chatbot
from report_generator_app import generate_full_pdf_report

# Sidebar navigation menu
with st.sidebar:
    selected = option_menu(
        menu_title="Portfolio Management App",
        options=[
            "Home",
            "Portfolio Manager Data",
            "API Data",
            "Data Transformation",
            "Data Visualization",
            "Streamlit Dashboard",
            "Power BI Dashboard",
            "Portfolio Chatbot",
            "Download Report"
        ],
        icons=[
            "house",               # Home
            "person-lines-fill",   # Portfolio Manager Data
            "cloud-download",      # API Data
            "arrow-repeat",        # Data Transformation
            "graph-up-arrow",      # Data Visualization
            "bar-chart-line",      # Streamlit Dashboard
            "pie-chart",           # Power BI Dashboard
            "robot",               # Chatbot
            "file-earmark-arrow-down"  # Download Report (PDF)
        ],
        menu_icon="graph-up",      # Sidebar menu icon
        default_index=0
    )

# Route to the selected module
if selected == "Home":
    home()

elif selected == "Portfolio Manager Data":
    portfolio_input()

elif selected == "API Data":
    api_data_fetch()

elif selected == "Data Transformation":
    eda_transform()

elif selected == "Data Visualization":
    data_visualization()

elif selected == "Streamlit Dashboard":
    streamlit_dashboard()

elif selected == "Power BI Dashboard":
    power_bi_dashboard()

elif selected == "Portfolio Chatbot":
    portfolio_chatbot()

elif selected == "Download Report":
    st.markdown("---")
    st.success("Ready to generate a comprehensive PDF report of your portfolio insights.")
    if st.button("📄 Download Portfolio Report (PDF)"):
        generate_full_pdf_report()
