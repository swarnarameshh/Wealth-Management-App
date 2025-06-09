import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

def streamlit_dashboard():
    st.title("📈 Interactive Portfolio Dashboard")

    # Check if transformed data is ready
    if "eda_df" not in st.session_state:
        st.warning("⚠️ Please run Data Transformation first to generate portfolio insights.")
        return

    eda_df = st.session_state.eda_df.copy()

    # Basic filter - select stocks from portfolio
    symbols = eda_df["Symbol"].unique().tolist()
    selected_symbols = st.multiselect("Select Stocks to Display", options=symbols, default=symbols)

    filtered_df = eda_df[eda_df["Symbol"].isin(selected_symbols)]

    # 1. Total Holding Value by Stock
    st.subheader("💼 Total Holdings Value by Stock")

    fig = px.bar(
    filtered_df, 
    x="Symbol", 
    y="Total Holding Value", 
    color="Sector",          # This creates the stacking by category
    title="Total Holding Value by Stock Symbol and Sector",
    labels={"Total Holding Value": "Total Holding Value ($)"},
    text=filtered_df["Total Holding Value"].apply(lambda x: f"${x:,.0f}"),  # Optional: show values on bars
    )

    fig.update_layout(barmode='stack', xaxis={'categoryorder':'total descending'})

    st.plotly_chart(fig, use_container_width=True)

    #2. Breakdown of Investment, Gains and Estimated Tax
    PRIMARY_COLOR = 'royalblue'
    SUCCESS_COLOR = 'seagreen'
    ACCENT_COLOR = 'orange'
    NEUTRAL_COLOR = 'gray'
    st.subheader("📊 Breakdown of Investment, Gains and Estimated Tax")
    # Use existing columns from filtered_df
    symbols = filtered_df["Symbol"]
    investment = filtered_df["Total Holding Value"]  # Assuming this is the invested amount
    gain = filtered_df["Capital Gain"]
    tax = filtered_df["Estimated Tax"]
    fig = go.Figure()
    # Investment bar
    fig.add_trace(go.Bar(
    y=symbols,
    x=investment,
    name='Investment',
    orientation='h',
    marker_color=PRIMARY_COLOR,
    hovertemplate='Investment: $%{x:,.2f}<extra></extra>'
    ))
    # Gains positive and negative split
    positive_gain = gain.clip(lower=0)
    negative_gain = gain.clip(upper=0)
    fig.add_trace(go.Bar(
    y=symbols,
    x=positive_gain,
    name='Gain (Positive)',
    orientation='h',
    marker_color=SUCCESS_COLOR,
    hovertemplate='Gain: $%{x:,.2f}<extra></extra>'
    ))
    fig.add_trace(go.Bar(
    y=symbols,
    x=negative_gain,
    name='Gain (Negative)',
    orientation='h',
    marker_color='indianred',
    hovertemplate='Gain: $%{x:,.2f}<extra></extra>'
    ))
    # Tax (only positive)
    tax_positive = tax.clip(lower=0)
    fig.add_trace(go.Bar(
    y=symbols,
    x=tax_positive,
    name='Estimated Tax',
    orientation='h',
    marker_color=ACCENT_COLOR,
    hovertemplate='Tax: $%{x:,.2f}<extra></extra>'
    ))
    fig.update_layout(
    barmode='stack',
    title="Investment, Gain & Estimated Tax per Stock",
    xaxis_title="Amount ($)",
    yaxis_title="Stock Symbol",
    yaxis=dict(autorange="reversed"),  # Reverse y axis to match horizontal bar order
    legend=dict(title="Legend"),
    height=500,
    margin=dict(l=100, r=50, t=70, b=50)
    )
    st.plotly_chart(fig, use_container_width=True)

    #3. Categorized Holding by sector
    st.subheader("🏢 Holdings Distribution by Sector")
    # Group by Sector using filtered_df (from eda_df)
    sector_df = filtered_df.groupby("Sector")["Total Holding Value"].sum().reset_index()
    # Create interactive pie chart
    fig = px.pie(
    sector_df,
    values="Total Holding Value",
    names="Sector",
    title="Portfolio Distribution by Sector",
    hole=0.4,  # Donut chart
    color_discrete_sequence=px.colors.qualitative.Pastel,
    )
    fig.update_traces(textinfo='percent+label', pull=[0.03]*len(sector_df))
    st.plotly_chart(fig, use_container_width=True)

    # 4. Returns by Investment Type (%)
    st.subheader("📈 Returns by Investment Type (%)")
    # Grouping return % by Symbol (or use as-is if already unique per symbol)
    returns_df = filtered_df[["Symbol", "Return (%)"]].copy()
    # Optional: take absolute returns to represent share in pie (remove if you want signed values)
    returns_df["Return Abs (%)"] = returns_df["Return (%)"].abs()
    # Create interactive donut chart
    fig = px.pie(
    returns_df,
    values="Return Abs (%)",
    names="Symbol",
    title="Returns by Investment Type",
    hole=0.4,
    color_discrete_sequence=px.colors.sequential.RdBu,
    )
    fig.update_traces(textinfo="percent+label", hovertemplate="Symbol: %{label}<br>Return: %{value:.2f}%")
    st.plotly_chart(fig, use_container_width=True)

    # 5. Expected Returns by CAPM
    st.subheader("🔮 Expected Returns (CAPM)")
    if "Expected Return (%)" in filtered_df.columns:
        capm_df = filtered_df[["Symbol", "Expected Return (%)"]].copy()
    # Interactive clustered column chart
    fig = px.bar(
        capm_df,
        x="Symbol",
        y="Expected Return (%)",
        color="Symbol",  # Colors grouped by symbol (each bar colored differently)
        title="Expected Returns (CAPM Model)",
        labels={"Expected Return (%)": "Expected Return (%)"},
        text=capm_df["Expected Return (%)"].apply(lambda x: f"{x:.2f}%"),
    )
    fig.update_layout(
        xaxis_title="Stock Symbol",
        yaxis_title="Expected Return (%)",
        showlegend=False,
        bargap=0.3,
    )
    st.plotly_chart(fig, use_container_width=True)
    st.markdown("Expected return values estimated using the **Capital Asset Pricing Model (CAPM)**.")


    # 6. Cumulative Return vs S&P 500 Benchmark
    st.subheader("📊 Cumulative Return Comparison vs S&P 500")
    if "merged_all" in st.session_state:
        merged_all = st.session_state.merged_all
        st.line_chart(merged_all.set_index('date'))
    else:
        st.info("Run Data Transformation to fetch and compute cumulative returns.")

    # 7. Top Gainers and Losers
    if "top_5_gainers" in st.session_state and "top_5_losers" in st.session_state:
        st.subheader("🚀 Top Gainers and 📉 Top Losers")
        gainers = st.session_state.top_5_gainers.copy()
        losers = st.session_state.top_5_losers.copy()
        # Ensure numeric and clean
        gainers["changesPercentage"] = pd.to_numeric(gainers["changesPercentage"], errors='coerce')
        losers["changesPercentage"] = pd.to_numeric(losers["changesPercentage"], errors='coerce')
        gainers.dropna(subset=["changesPercentage"], inplace=True)
        losers.dropna(subset=["changesPercentage"], inplace=True)
        # Add category label
        gainers["Category"] = "Gainer"
        losers["Category"] = "Loser"
        # Combine into one DataFrame
        combined_df = pd.concat([gainers, losers], ignore_index=True)
        combined_df["changesPercentage"] = combined_df["changesPercentage"].round(2)

        # Create interactive clustered bar chart
        fig = px.bar(
            combined_df,
            x="ticker",
            y="changesPercentage",
            color="Category",
            barmode="group",
            title="Top Gainers and Losers (%)",
            labels={"ticker": "Stock Ticker", "changesPercentage": "Change (%)"},
            text="changesPercentage",
            color_discrete_map={"Gainer": "#28a745", "Loser": "#dc3545"}  # Green for gainers, red for losers
        )

        fig.update_layout(
            xaxis_title="Ticker",
            yaxis_title="Percentage Change (%)",
            legend_title="Type",
            bargap=0.3
        )

        st.plotly_chart(fig, use_container_width=True)


    # 8. Suggested Top Funds
    if "top_funds" in st.session_state:
        st.subheader("💰 Suggested Top Funds")
        funds = st.session_state.top_funds.copy()
        if "symbol" in funds.columns and "price" in funds.columns:
            # Optional stacking category: create one if not present
            if "category" not in funds.columns:
                funds["category"] = "ETF"

            funds = funds.sort_values(by="price", ascending=True)

            fig = px.bar(
                funds,
                x="symbol",
                y="price",
                color="category",  # This will enable stacking
                title="Suggested Top Funds by Price",
                labels={"symbol": "Fund Symbol", "price": "Price ($)", "category": "Fund Type"},
                text="price",
                color_discrete_sequence=px.colors.qualitative.Set2
            )

            fig.update_layout(
                barmode="stack",
                xaxis_title="Fund Symbol",
                yaxis_title="Price ($)",
                legend_title="Fund Category",
                bargap=0.3
            )

            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("⚠️ 'symbol' or 'price' columns missing in top funds data.")


