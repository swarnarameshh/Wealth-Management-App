import streamlit as st
from streamlit_option_menu import option_menu
from home_app import home
from portfolio_manager_app import portfolio_input
from api_data_app import api_data_fetch
from eda_transform_app import eda_transform
from data_visualization_app import data_visualization
from power_bi_app import power_bi_dashboard
from streamlit_dashboard_app import streamlit_dashboard
with st.sidebar:
    selected = option_menu(
        "Portfolio Management App", 
        ["Home", 
         "Portfolio Manager Data", 
         "API Data",
         "Data Transformation" ,
         "Data Visualization",
         "Streamlit Dashboard",
         "Power BI Dashboard"],
        icons=[
            'house',            # Home
            'person-lines-fill',# Portfolio Manager Data
            'cloud-download',   # API Data
            'arrow-repeat' ,    #data transformation
            'graph-up-arrow',   # Data Visualization
            'bar-chart-line',   #Streamlit dashboard
            'pie-chart'         # Power BI Dashboard
        ], 
        menu_icon="graph-up", 
        default_index=0
    )

# Menu Navigation Logic
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