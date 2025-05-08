import streamlit as st
import pandas as pd
import datetime
import uuid
from openai import OpenAI

# Load OpenAI key securely
api_key = st.secrets["OPENAI_API_KEY"]
client = OpenAI(api_key=api_key)

# Hardcoded demo user for now
users = {
    "demo@quantfox.ai": {
        "password": "demo123",
        "balance": 1_000_000,
        "role": "Free"
    }
}

# Streamlit config
st.set_page_config(page_title="Quant Fox", layout="wide")
st.markdown("""<style>
    body { background-color: #0F1117; }
    .main { color: white; }
    h1, h2, h3 { color: #00FF85; }
    .stButton>button {
        background-color: #1E90FF;
        color: white;
        border-radius: 8px;
        padding: 0.5em 1em;
        font-weight: bold;
    }
</style>""", unsafe_allow_html=True)

# Auth
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.user = ""

if not st.session_state.logged_in:
    st.title("Login to Quant Fox")
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

# Sidebar and logout
st.sidebar.title("Quant Fox")
st.sidebar.write(f"User: {st.session_state.user}")
st.sidebar.write(f"💰 Balance: ${st.session_state.balance:,.2f}")
if st.sidebar.button("Logout"):
    st.session_state.logged_in = False
    st.session_state.user = ""
    st.experimental_rerun()

# App interface
st.title("📊 Simulate a Trade")
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

# Show past trades
st.subheader("Your Trades")
if st.session_state.trades:
    st.dataframe(pd.DataFrame(st.session_state.trades))
else:
    st.info("No trades yet.")

# Chatbot (docked)
with st.expander("💬 Ask Quant Fox (AAVE Style)", expanded=False):
    user_input = st.text_input("Ask anything about this trade, markets, or your balance:")
    if user_input:
        try:
            response = client.chat.completions.create(
                model="gpt-4",
                messages=[{
                    "role": "user",
                    "content": f"You are Quant Fox, a smart trading AI who speaks in AAVE. Give advice about {option_type} options on {symbol} with strike {strike_price}. User balance is ${st.session_state.balance}."
                }],
                temperature=0.85
            )
            reply = response.choices[0].message.content.strip()
            st.markdown(f"**Quant Fox says:** _\"{reply}\"_")
        except Exception as e:
            st.error(f"Chatbot Error: {e}")
