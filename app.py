import streamlit as st
import yfinance as yf
import matplotlib.pyplot as plt
from agent.stock_agent import build_agent

st.set_page_config(page_title="Stock Market Agent", page_icon="📈")

st.title("📈 Stock Market Agent (LangGraph + Streamlit)")

# --- User input ---
user_symbol = st.text_input("Enter a stock symbol (e.g., AAPL, TSLA, RELIANCE):")

if st.button("Run Agent") and user_symbol:
    # Run the agent
    agent = build_agent()
    result = agent.invoke({"query": user_symbol})
    st.success(result["response"])

    # --- Show stock chart ---
    try:
        stock = yf.Ticker(user_symbol)
        hist = stock.history(period="1mo")  # last 1 month
        st.subheader(f"📊 {user_symbol.upper()} Price History (1 month)")

        fig, ax = plt.subplots()
        hist["Close"].plot(ax=ax, title=f"{user_symbol.upper()} Closing Prices")
        ax.set_ylabel("Price (USD)")
        st.pyplot(fig)

    except Exception as e:
        st.error(f"Could not fetch chart: {e}")
