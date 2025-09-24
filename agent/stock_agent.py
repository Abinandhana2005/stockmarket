from langgraph.graph import StateGraph, END
from typing import TypedDict, Dict
import yfinance as yf
import requests

# --- Define Agent State ---
class AgentState(TypedDict):
    query: str
    response: str

# --- Tool: Get Stock Info (using yfinance) ---
def get_stock_info(symbol: str) -> str:
    try:
        stock = yf.Ticker(symbol)
        hist = stock.history(period="5d")  # last 5 days
        latest_price = hist["Close"].iloc[-1]
        prev_price = hist["Close"].iloc[-2]

        trend = "UP" if latest_price > prev_price else "DOWN"
        return f"Stock {symbol}: Price={latest_price:.2f}, Trend={trend}"
    except Exception as e:
        return f"Error fetching stock info for {symbol}: {e}"

# --- Tool: Send Signal (dummy API call) ---
def send_signal(action: str, symbol: str) -> str:
    try:
        url = "https://httpbin.org/post"  # demo endpoint
        payload = {"symbol": symbol, "action": action}
        response = requests.post(url, json=payload)

        if response.status_code == 200:
            return f"Signal sent: {action.upper()} {symbol}"
        else:
            return f"Failed to send signal ({response.status_code})"
    except Exception as e:
        return f"Error sending signal: {e}"

# --- Agent Node Function ---
def stock_agent_node(state: AgentState) -> Dict:
    query = state["query"].strip().upper()

    stock_info = get_stock_info(query)

    if "UP" in stock_info:
        signal = send_signal("buy", query)
    elif "DOWN" in stock_info:
        signal = send_signal("sell", query)
    else:
        signal = "No clear signal."

    return {"response": f"{stock_info}\n{signal}"}

# --- Build LangGraph Agent ---
def build_agent():
    graph = StateGraph(AgentState)
    graph.add_node("stock", stock_agent_node)
    graph.set_entry_point("stock")
    graph.add_edge("stock", END)
    return graph.compile()
