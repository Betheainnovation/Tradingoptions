import streamlit as st
import pandas as pd
import datetime
import uuid
import sqlite3
import hashlib

# Initialize SQLite database
conn = sqlite3.connect("quant_fox.db", check_same_thread=False)
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS users (
    email TEXT PRIMARY KEY,
    hashed_password TEXT,
    balance REAL DEFAULT 1000000
)''')
c.execute('''CREATE TABLE IF NOT EXISTS trades (
    id TEXT PRIMARY KEY,
    email TEXT,
    symbol TEXT,
    type TEXT,
    strike REAL,
    premium REAL,
    contracts INTEGER,
    exit REAL,
    profit REAL,
    time TEXT
)''')
conn.commit()

# Helper functions
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def login_user(email, password):
    hashed = hash_password(password)
    c.execute("SELECT email, balance FROM users WHERE email=? AND hashed_password=?", (email, hashed))
    return c.fetchone()

def create_user(email, password):
    hashed = hash_password(password)
    try:
        c.execute("INSERT INTO users (email, hashed_password) VALUES (?, ?)", (email, hashed))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False

def get_user_trades(email):
    c.execute("SELECT * FROM trades WHERE email=? ORDER BY time DESC", (email,))
    return c.fetchall()

# Auth flow
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

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.email = ""
    st.session_state.balance = 0.0

if not st.session_state.logged_in:
    st.title("Quant Fox Login")
    option = st.radio("Select Option", ["Login", "Sign Up"])
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    if st.button(option):
        if option == "Login":
            user = login_user(email, password)
            if user:
                st.session_state.logged_in = True
                st.session_state.email = user[0]
                st.session_state.balance = user[1]
                st.success("Logged in successfully!")
                st.rerun()
            else:
                st.error("Invalid credentials")
        else:
            if create_user(email, password):
                st.success("Account created. Please log in.")
            else:
                st.error("Account already exists.")
    st.stop()

# Dashboard
st.sidebar.title("Quant Fox")
st.sidebar.write(f"User: {st.session_state.email}")
st.sidebar.write(f"💰 Balance: ${st.session_state.balance:,.2f}")
if st.sidebar.button("Logout"):
    st.session_state.logged_in = False
    st.session_state.email = ""
    st.session_state.balance = 0.0
    st.rerun()

st.title("📊 Simulate a Trade")
symbol = st.selectbox("Select Stock", ["AAPL", "TSLA", "GOOGL", "MSFT", "NVDA"])
option_type = st.radio("Option Type", ["Call", "Put"])
strike_price = st.number_input("Strike Price", min_value=1.0, value=150.0)
premium = st.number_input("Premium ($)", min_value=0.1, value=5.0)
contracts = st.number_input("Contracts", min_value=1, value=1)
exit_price = st.number_input("Target Exit Price ($)", value=8.0)

if st.button("Place Simulated Trade"):
    cost = premium * contracts * 100
    payout = exit_price * contracts * 100
    profit = payout - cost
    if cost <= st.session_state.balance:
        st.session_state.balance -= cost
        c.execute("UPDATE users SET balance=? WHERE email=?", (st.session_state.balance, st.session_state.email))
        trade = (
            str(uuid.uuid4()), st.session_state.email, symbol, option_type,
            strike_price, premium, contracts, exit_price, profit,
            datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        )
        c.execute("INSERT INTO trades VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", trade)
        conn.commit()
        st.success(f"Trade placed. Est. profit: ${profit:,.2f}")
    else:
        st.error("Insufficient balance")

# Show trades
st.subheader("Your Trades")
rows = get_user_trades(st.session_state.email)
if rows:
    df = pd.DataFrame(rows, columns=["ID", "Email", "Symbol", "Type", "Strike", "Premium", "Contracts", "Exit", "Profit", "Time"])
    st.dataframe(df.drop(columns=["ID", "Email"]))
else:
    st.info("No trades found.")

