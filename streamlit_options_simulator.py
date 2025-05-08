# Quant Fox Full-Stack MVP (Phase 1)
# This is a scaffolded Python/Streamlit app with login, dashboard, simulated trading, and integrated chatbot

import streamlit as st
import pandas as pd
import datetime
import uuid
from openai import OpenAI

# Store users and session data (normally would be in a DB)
users = {
    "demo@quantfox.ai": {"password": "demo123", "balance": 1_000_000, "role": "Free"},
    # Add admin manually if needed
}
session = {}

st.set_page_config(page_title="Quant Fox", layout="wide")
st.markdown("""
    <style>
        body { background-color: #0F1117; }
        .main { color: white; }
        h1, h2, h3 { color: #00FF85; }
        .stButton>button { background-color: #1E90FF; color: white; border-radius: 8px; padding: 0.5em 1em; font-weight: bold; }
        .chatbox { border: 1px solid #333; border-radius: 10px; padding: 1em; background-color: #15171c; }
    </style>
""", unsafe_allow_html=True)

# Authentication section
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.user = ""

if not st.session_state.logged_in:
    st.title("🦊 Quant Fox")
    st.markdown("Login to your dashboard")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if email in users and users[email]["password"] == password:
            st.session_state.logged_in = True
            st.session_state.user = email
            st.session_state.balance = users[email]["balance"]
            st.success("Logged in successfully!")
            st.experimental_rerun()
        else:
            st.error("Invalid credentials")
    st.stop()

# Dashboard section
st.sidebar.title("Quant Fox")
st.sidebar.write(f"Logged in as: {st.session_state.user}")
st.sidebar.write(f"💰 Balance: ${st.session_state.balance:,.2f}")
if st.sidebar.button("Logout"):
    st.session_state.logged_in = False
    st.session_state.user = ""
    st.experimental_rerun()

st.title("Dashboard")
st.markdown("Welcome to your trading simulator. Choose your stock and simulate an options trade.")

symbol = st.selectbox("Select Stock", ["AAPL", "TSLA", "GOOGL", "MSFT", "NVDA"])
option_type = st.radio("Option Type", ["Call", "Put"])
strike_price = st.number_input("Strike Price", min_value=1.0, value=150.0)
premium = st.number_input("Premium ($)", min_value=0.1, value=5.0)
contracts = st.number_input("Contracts", min_value=1, value=1)
exit_price = st.number_input("Target Exit Price ($)", value=8.0)

if "trades" not in st.session_state:
    st.session_state.trades = []

if st.button("Place Simulated Trade"):
    cost = premium * contracts * 100
    payout = exit_price * contracts * 100
    profit = payout - cost
    if cost <= st.session_state.balance:
        st.session_state.balance -= cost
        trade = {
            "id": str(uuid.uuid4()),
            "symbol": symbol,
            "type": option_type,
            "strike": strike_price,
            "premium": premium,
            "contracts": contracts,
            "exit": exit_price,
            "profit": profit,
            "time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        }
        st.session_state.trades.append(trade)
        st.success(f"Trade placed. Est. profit: ${profit:,.2f}")
    else:
        st.error("Insufficient balance")

# Show trades
st.subheader("Your Trades")
if st.session_state.trades:
    st.dataframe(pd.DataFrame(st.session_state.trades))
else:
    st.info("No trades placed yet.")

# Chatbot toggleable
with st.expander("💬 Quant Fox Chatbot (AI Coach)", expanded=False):
    st.markdown("Ask Quant Fox how to optimize your trades.")
    user_input = st.text_input("You:", key="chat_input")
    if user_input:
        try:
            client = OpenAI(api_key="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")
            response = client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "user", "content": f"Respond in AAVE: {user_input}. Assume this user has ${st.session_state.balance:,.0f} and just placed a {option_type} option on {symbol}."}
                ],
                temperature=0.85
            )
            reply = response.choices[0].message.content.strip()
            st.markdown(f"**Quant Fox:** _\"{reply}\"_")
        except Exception as e:
            st.error(f"Chatbot error: {e}")

# Footer
st.markdown("---")
st.markdown(" **Betheainnovation 2025** · Quant Fox™")
