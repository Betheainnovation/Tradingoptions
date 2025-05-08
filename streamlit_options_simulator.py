import streamlit as st
import pandas as pd
import openai
import datetime

# === App Branding ===
st.set_page_config(page_title="Quant Fox", layout="wide")

st.markdown("""
    <style>
    body {
        background-color: #0F1117;
    }
    .main {
        color: white;
    }
    h1, h2, h3 {
        color: #00FF85;
    }
    .stButton>button {
        background-color: #1E90FF;
        color: white;
        border-radius: 8px;
        padding: 0.5em 1em;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

# === Logo + Title ===
st.image("https://via.placeholder.com/300x100.png?text=Quant+Fox+Logo", width=300)
st.title("🦊 Quant Fox — Trade Smarter with Style")
st.subheader("Real-time trading sim + AAVE-style financial advice from a GPT-powered fox.")

# === Session State Init ===
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "saved_advice" not in st.session_state:
    st.session_state.saved_advice = []

if "saved_trades" not in st.session_state:
    st.session_state.saved_trades = []

# === Sidebar Inputs ===
st.sidebar.header("📊 Simulate a Trade")
symbol = st.sidebar.text_input("Stock Symbol", value="AAPL")
option_type = st.sidebar.selectbox("Option Type", ["Call", "Put"])
strike_price = st.sidebar.number_input("Strike Price", min_value=1.0, value=150.0)
premium = st.sidebar.number_input("Option Premium ($)", min_value=0.1, value=5.0)
contracts = st.sidebar.number_input("Contracts", min_value=1, value=1)
exit_price = st.sidebar.number_input("Target Option Exit Price ($)", value=8.0)

# === Simulated Trade Summary ===
total_cost = premium * contracts * 100
total_payout = exit_price * contracts * 100
profit = total_payout - total_cost

st.markdown(f"### 💼 Simulated Trade Summary for {symbol.upper()} {option_type}")
st.write(f"**Entry Cost:** `${total_cost:,.2f}`")
st.write(f"**Exit Value:** `${total_payout:,.2f}`")
st.write(f"**Estimated Profit:** `${profit:,.2f}`")

if st.button("💾 Save This Trade"):
    trade_data = {
        "Time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
        "Symbol": symbol.upper(),
        "Type": option_type,
        "Strike": strike_price,
        "Premium": premium,
        "Contracts": contracts,
        "Exit Price": exit_price,
        "Profit": profit
    }
    st.session_state.saved_trades.append(trade_data)
    st.success("Trade saved.")

# === TradingView Embed ===
st.subheader(f"📈 {symbol.upper()} Market Chart (TradingView)")
embed_url = f"https://s.tradingview.com/widgetembed/?symbol=NASDAQ%3A{symbol.upper()}&interval=D&theme=dark&style=1&locale=en"
iframe_code = f'<iframe src="{embed_url}" width="100%" height="400" frameborder="0" allowfullscreen></iframe>'
st.markdown(iframe_code, unsafe_allow_html=True)

# === AAVE-Style Advice Box ===
st.subheader("🧠 Quant Fox Bot Says:")
default_advice = f"Aye fam, dat {symbol.upper()} {option_type.lower()} wit a {strike_price} strike? If da volume holdin’ and da trend strong, you might just walk off wit a lil’ bag. Don’t get caught slippin’. Lock in them profits."
st.markdown(f"**_“{default_advice}”_**")

# === AAVE-Style Chatbot ===
st.subheader("🗣️ Ask Quant Fox for Money Tips")

openai_api_key = st.secrets["OPENAI_API_KEY"] if "OPENAI_API_KEY" in st.secrets else st.text_input("Enter your OpenAI API key")
user_input = st.text_input("What’s on yo mind?", placeholder="e.g. What should I do if the dollar crashin’?")

if st.button("👂 Let Fox Talk"):
    if not openai_api_key:
        st.warning("Enter your OpenAI API key.")
    elif user_input.strip() == "":
        st.warning("Say somethin’, fam.")
    else:
        try:
            openai.api_key = openai_api_key
            prompt = f"You are Quant Fox — a smart, street-savvy financial assistant that speaks in African American Vernacular English (AAVE). Offer smart, current advice based on market conditions, global news, or finance. Speak how Black folks talk naturally. Question: {user_input}"
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.85
            )
            reply = response.choices[0].message.content.strip()
            st.session_state.chat_history.append({"question": user_input, "answer": reply})
            st.markdown(f"**Quant Fox:** _\"{reply}\"_")

            if st.button("💾 Save This Advice"):
                st.session_state.saved_advice.append({
                    "Time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
                    "Question": user_input,
                    "Advice": reply
                })
                st.success("Advice saved.")
        except Exception as e:
            st.error(f"Error: {e}")

# === Display Chat History ===
if st.session_state.chat_history:
    st.markdown("### 💬 Chat History")
    for entry in reversed(st.session_state.chat_history[-5:]):
        st.markdown(f"**You:** {entry['question']}")
        st.markdown(f"**Fox:** _{entry['answer']}_")

# === Display Saved Data ===
if st.session_state.saved_advice:
    st.markdown("### 🧾 Saved Advice")
    df_advice = pd.DataFrame(st.session_state.saved_advice)
    st.dataframe(df_advice)

if st.session_state.saved_trades:
    st.markdown("### 💼 Saved Trades")
    df_trades = pd.DataFrame(st.session_state.saved_trades)
    st.dataframe(df_trades)

# === Footer ===
st.markdown("---")
st.markdown("Made with 💚 by **Betheainnovation** · Powered by Streamlit · Quant Fox™")
