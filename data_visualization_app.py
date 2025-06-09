import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd

def data_visualization():
    st.title("📊 Portfolio Data Visualizations")
    sns.set(style="whitegrid")
    
    # Define consistent pastel color palette
    PRIMARY_COLOR = '#A8D8EA'      # Pastel Blue
    SECONDARY_COLOR = '#D4A5D4'    # Pastel Purple
    ACCENT_COLOR = '#FFD3A5'       # Pastel Orange
    SUCCESS_COLOR = '#FDB7C1'      # Pastel Pink/Red
    NEUTRAL_COLOR = '#C8C8C8'      # Light Gray
    
    # Pastel color palette for multiple items
    PALETTE = ['#A8D8EA', '#D4A5D4', '#FFD3A5', '#FDB7C1', '#B8E6B8', '#F7D794', '#E6C3F7', '#98D8C8', '#F7CAC9', '#C7CEEA']

    if "eda_df" not in st.session_state:
        st.warning("⚠️ Please run the Portfolio EDA first to generate required data.")
        return

    df = st.session_state.eda_df

    # (i) Total Holdings Value by Stock
    st.subheader("💼 Total Holdings Value by Stock")
    fig, ax = plt.subplots(figsize=(6, 4))
    sns.barplot(x="Symbol", y="Total Holding Value", data=df, ax=ax, palette=PALETTE, dodge=False, legend=False)
    ax.axhline(0, color=NEUTRAL_COLOR, linewidth=0.8)  # zero baseline for negative values
    ax.set_title("Total Holdings Value by Stock", fontsize=14)
    ax.set_xlabel("Stock Symbol")
    ax.set_ylabel("Total Value ($)")
    st.pyplot(fig)
    st.markdown("This chart shows the total monetary value you hold in each stock. A higher bar indicates a larger investment. This helps identify overconcentration or diversification.")

    # (ii) Estimated Tax on Gains - handle negative gains correctly
    st.subheader("🧾 Estimated Tax on Gains")
    fig, ax = plt.subplots(figsize=(6, 4))
    y = np.arange(len(df['Symbol']))
    height = 0.5

    investment = df['Buy Price'] * df['Shares']
    gain = df['Capital Gain']
    tax = df['Estimated Tax']

    ax.barh(y, investment, height=height, label='Investment', color=PRIMARY_COLOR)

    # Plot gains with proper left positions to handle negatives
    for i, (inv, g) in enumerate(zip(investment, gain)):
        if g >= 0:
            ax.barh(i, g, height=height, left=inv, color=SUCCESS_COLOR, label='Gain' if i == 0 else "")
        else:
            ax.barh(i, g, height=height, left=inv+g, color=SUCCESS_COLOR, label='Gain' if i == 0 else "")

    # Plot tax only if positive, positioned correctly
    for i, (inv, g, t) in enumerate(zip(investment, gain, tax)):
        if t > 0:
            left_pos = inv + max(g, 0)
            ax.barh(i, t, height=height, left=left_pos, color=ACCENT_COLOR, label='Tax' if i == 0 else "")

    ax.set_yticks(y)
    ax.set_yticklabels(df['Symbol'])
    ax.set_title("Investment, Gain & Estimated Tax per Stock")
    ax.set_xlabel("Amount ($)")
    ax.legend()
    ax.axvline(0, color=NEUTRAL_COLOR, linewidth=0.8)  # zero baseline
    st.pyplot(fig)
    st.markdown("This chart illustrates your original investment, the profit (gain), and the estimated tax. It helps assess tax exposure on your capital gains.")

    # (iii) Categorized Holdings by Sector
    st.subheader("🏢 Holdings by Sector")
    sector_df = df.groupby(["Sector", "Symbol"])["Total Holding Value"].sum().reset_index()
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.barplot(x="Sector", y="Total Holding Value", hue="Symbol", data=sector_df, ax=ax, palette=PALETTE)
    ax.axhline(0, color=NEUTRAL_COLOR, linewidth=0.8)  # zero baseline
    ax.set_title("Holdings by Sector and Ticker")
    ax.set_xlabel("Sector")
    ax.set_ylabel("Total Value (₹)")
    plt.xticks(rotation=45)
    st.pyplot(fig)
    st.markdown("This chart breaks down your portfolio by sector and symbol. It gives you a view of sector diversification.")

    # (iv) Returns by Investment Type - replaced pie chart with barplot due to negatives
    st.subheader("📈 Returns by Investment Type")
    fig, ax = plt.subplots(figsize=(7, 4))
    sns.barplot(x="Symbol", y="Return (%)", data=df, palette=PALETTE, ax=ax)
    ax.axhline(0, color=NEUTRAL_COLOR, linewidth=0.8)  # zero baseline
    ax.set_title("Returns by Investment Type")
    ax.set_ylabel("Return (%)")
    st.pyplot(fig)
    st.markdown("This bar chart shows how each stock contributes to your overall return, including losses if any.")

    # (v) Cumulative Return vs Benchmark
    if "merged_all" in st.session_state:
        st.subheader("📊 Cumulative Returns vs Benchmark")
        merged = st.session_state.merged_all.copy()

        if 'date' in merged.columns:
            merged['date'] = pd.to_datetime(merged['date'])

            fig, ax = plt.subplots(figsize=(10, 4))
            colors = PALETTE[:len(merged.columns[1:])]
            for i, col in enumerate(merged.columns[1:]):
                sns.lineplot(data=merged, x="date", y=col, ax=ax, label=col.replace('_cum_return_pct', '').upper(), color=colors[i])
            ax.axhline(0, linestyle="--", color=NEUTRAL_COLOR)  # zero baseline
            ax.set_title("Cumulative Returns vs S&P 500")
            ax.set_ylabel("Cumulative Return (%)")
            ax.set_xlabel("Date")
            ax.legend(title="Ticker")
            plt.xticks(rotation=45)
            st.pyplot(fig)
            st.markdown("This line chart compares your portfolio's performance against the S&P 500.")
        else:
            st.warning("⚠️ 'date' column missing in merged benchmark data.")
    # (vi) Top gainers and losers
    if "top_5_gainers" in st.session_state and "top_5_losers" in st.session_state:
        st.subheader("🚀 Top Gainers and 📉 Top Losers")

        gainers = st.session_state.top_5_gainers.copy()
        losers = st.session_state.top_5_losers.copy()

        gainers["changesPercentage"] = pd.to_numeric(gainers["changesPercentage"], errors='coerce')
        losers["changesPercentage"] = pd.to_numeric(losers["changesPercentage"], errors='coerce')

        gainers.dropna(subset=["changesPercentage"], inplace=True)
        losers.dropna(subset=["changesPercentage"], inplace=True)

        gainers.sort_values("changesPercentage", ascending=True, inplace=True)
        losers.sort_values("changesPercentage", ascending=True, inplace=True)

        # Gainers Dumbbell Chart
        fig, ax = plt.subplots(figsize=(6, 4))
        ax.axvline(0, color=NEUTRAL_COLOR, linewidth=0.8)
        xmin = min(gainers["changesPercentage"].min(), 0) * 1.1
        xmax = gainers["changesPercentage"].max() * 1.1
        ax.set_xlim(xmin, xmax)
        for _, row in gainers.iterrows():
            ax.plot([0, row["changesPercentage"]], [row["ticker"], row["ticker"]], marker="o", color=PRIMARY_COLOR)
        ax.set_title("Top Gainers (%) - Dumbbell Chart")
        ax.set_xlabel("Change (%)")
        st.pyplot(fig)

        # Losers Dumbbell Chart
        fig, ax = plt.subplots(figsize=(6, 4))
        ax.axvline(0, color=NEUTRAL_COLOR, linewidth=0.8)
        xmin = losers["changesPercentage"].min() * 1.1
        xmax = max(losers["changesPercentage"].max(), 0) * 1.1
        ax.set_xlim(xmin, xmax)
        for _, row in losers.iterrows():
            ax.plot([0, row["changesPercentage"]], [row["ticker"], row["ticker"]], marker="o", color=SECONDARY_COLOR)
        ax.set_title("Top Losers (%) - Dumbbell Chart")
        ax.set_xlabel("Change (%)")
        st.pyplot(fig)

        st.markdown("These dumbbell charts show the biggest movers. Longer bars reflect larger percentage changes.")


    # (vii) Estimated Expected Returns (CAPM)
    st.subheader("🔮 Expected Returns (CAPM)")
    if "Expected Return (%)" in df.columns:
        capm_df = df[["Symbol", "Expected Return (%)"]].copy()
        fig, ax = plt.subplots(figsize=(6, 3))
        sns.barplot(data=capm_df, y="Symbol", x="Expected Return (%)", palette=PALETTE, ax=ax)
        ax.axvline(0, color=NEUTRAL_COLOR, linewidth=0.8)  # zero baseline
        ax.set_title("CAPM Expected Return")
        st.pyplot(fig)
        st.markdown("Expected return values estimated using the Capital Asset Pricing Model.")

    # (viii) Suggested Top Funds
    if "top_funds" in st.session_state:
        st.subheader("💰 Suggested Top Funds")
        funds = st.session_state.top_funds.copy()

        if "symbol" in funds.columns and "price" in funds.columns:
            funds = funds.sort_values(by="price", ascending=True)

            fig, ax = plt.subplots(figsize=(10, 5))
            bars = sns.barplot(data=funds, x="symbol", y="price", palette=PALETTE, ax=ax)

            ax.set_title("Suggested Top Funds by Price")
            ax.set_xlabel("Fund Symbol")
            ax.set_ylabel("Price ($)")

            # Display values on top of bars
            for bar in bars.patches:
                height = bar.get_height()
                ax.annotate(f"${height:,.0f}", xy=(bar.get_x() + bar.get_width() / 2, height),
                            xytext=(0, 3), textcoords="offset points",
                            ha='center', va='bottom', fontsize=9, color='black')

            st.pyplot(fig)
            st.markdown("This chart highlights top ETF funds by price.")
        else:
            st.warning("⚠️ 'symbol' or 'price' columns missing in top funds data.")
