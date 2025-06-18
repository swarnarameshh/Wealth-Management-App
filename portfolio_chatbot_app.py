import streamlit as st
from groq import Groq
import os
import pandas as pd

def portfolio_chatbot():
    st.subheader("💬 Portfolio Chatbot (Groq LLaMA 3 - Personalized)")

    groq_api_key = st.secrets.get("groq_api_key") or os.getenv("GROQ_API_KEY")
    if not groq_api_key:
        st.error("Groq API key not found. Please set it in .streamlit/secrets.toml or as env variable.")
        return

    client = Groq(api_key=groq_api_key)

    # Fallback summary if no portfolio loaded
    portfolio_summary = "No portfolio data loaded."
    if "eda_df" in st.session_state:
        df = st.session_state.eda_df.copy()
        top_holdings = df.groupby("Sector")["Total Holding Value"].sum().sort_values(ascending=False).head(3)
        diversification = df["Sector"].nunique()
        risky_assets = df[df["Beta"] > 1.2]["Symbol"].tolist()
        top_return = df.loc[df["Return (%)"].idxmax(), ["Symbol", "Return (%)"]]

        portfolio_summary = f"""
        - Top sectors by holding: {', '.join(top_holdings.index.tolist())}
        - Number of unique sectors: {diversification}
        - High beta stocks (>1.2): {', '.join(risky_assets) if risky_assets else 'None'}
        - Highest returning stock: {top_return['Symbol']} ({top_return['Return (%)']:.2f}%)
        """

    # Initialize session state for chat
    if "conversation" not in st.session_state:
        st.session_state.conversation = [
            {
                "role": "system",
                "content": f"""You are a smart portfolio assistant that helps users understand their investments. You are given access to a summary of the user's portfolio:

{portfolio_summary}

Based on this, give actionable insights, risk warnings, diversification advice, and tax tips. When a user asks questions, personalize your answers using the portfolio context above."""
            }
        ]

    # Show history
    for i, msg in enumerate(st.session_state.conversation[1:]):
        if msg["role"] == "user":
            st.markdown(f"🧑‍💼 **You asked:**\n> {msg['content']}")
        else:
            st.markdown(f"🤖 **Assistant replied:**\n{msg['content']}")
            if i < len(st.session_state.conversation) - 2:
                st.markdown("---")

    # Chat input
    user_input = st.chat_input("Ask a portfolio-specific question...")

    if user_input:
        st.session_state.conversation.append({"role": "user", "content": user_input})

        try:
            with st.spinner("Analyzing your portfolio..."):
                response = client.chat.completions.create(
                    model="llama3-70b-8192",
                    messages=st.session_state.conversation
                )
                reply = response.choices[0].message.content
                st.session_state.conversation.append({"role": "assistant", "content": reply})
                st.rerun()
        except Exception as e:
            st.error(f"Error: {str(e)}")

    # Reset
    with st.expander("🧹 Reset Conversation"):
        if st.button("Clear Chat"):
            del st.session_state.conversation
            st.experimental_rerun()
