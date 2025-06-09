import streamlit as st
import streamlit.components.v1 as components

def power_bi_dashboard():
    st.title("📊 Power BI Dashboard Embedded")

    powerbi_iframe = """
    <iframe
        title="portfolio_management_dashboard_main"
        width="700"
        height="600"
        src="https://app.powerbi.com/reportEmbed?reportId=e3dd255a-6b7d-4f3d-92fc-caa1af2a4595&autoAuth=true&ctid=e0793d39-0939-496d-b129-198edd916feb"
        frameborder="0"
        allowFullScreen="true">
    </iframe>
    """

    components.html(powerbi_iframe, height=620)