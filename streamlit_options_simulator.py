import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf
import datetime
import plotly.graph_objs as go
import requests

# === Branding & Styling ===
st.set_page_config(page_title="Options AI Simulator", layout="wide")

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

# === App Title ===
st.title("💹 Options AI Simulator with Voice")
st.subheader("Powered by AAVE-style AI insight, real-time trading data, and ElevenLabs TTS")

# === Sidebar Inputs ===
st.sidebar.header("📊 Simulate a Trade")
symbol = st.sidebar.text_input("Stock Symbol", value="AAPL")
option_type = st.sidebar.selectbox("Option Type", ["Call", "Put"])
strike_price = st.sidebar.number_input("Strike Price", min_value=1.0, value=150.0)
premium = st.sidebar.number_input("Option Premium ($)", min_value=0.1, value=5.0)
contracts = st.sidebar.number_input("Contracts", min_value=1, value=1)
exit_price = st.sidebar.number_input("Target Option Exit Price ($)", value=8.0)

# === Trade Simulation ===
total_cost = premium * contracts * 100
total_payout = exit_price * contracts * 100
profit = total_payout - total_cost

st.markdown(f"### 💼 Simulated Trade Summary for {symbol.upper()} {option_type}")
st.write(f"**Entry Cost:** `${total_cost:,.2f}`")
st.write(f"**Potential Exit Value:** `${total_payout:,.2f}`")
st.write(f"**Estimated Profit:** `${profit:,.2f}`")

# === Real-Time Chart ===
st.subheader(f"📈 {symbol.upper()} Market Chart (3 Months)")

try:
    stock_data = yf.download(symbol, period="3mo", interval="1d")
    fig = go.Figure()
    fig.add_trace(go.Candlestick(
        x=stock_data.index,
        open=stock_data['Open'],
        high=stock_data['High'],
        low=stock_data['Low'],
        close=stock_data['Close'],
        name="Candlestick"
    ))
    fig.update_layout(
        xaxis_rangeslider_visible=False,
        height=400,
        margin=dict(t=10, b=10),
        plot_bgcolor="#0F1117",
        paper_bgcolor="#0F1117",
        font=dict(color="#FFFFFF")
    )
    st.plotly_chart(fig, use_container_width=True)
except:
    st.error("⚠️ Could not retrieve stock data. Check the symbol.")

# === AI Advice in AAVE ===
st.subheader("🧠 AI Advice (AAVE Style) + 🎙️ Voice Playback")

mock_advice = "Aight, listen here — AAPL on a mission. That 150 call lookin' tasty if that breakout holdin’. Secure that entry, ride the momentum, and don’t play yaself."

st.markdown(f"**_“{mock_advice}”_**")

# === ElevenLabs TTS ===
api_key = st.secrets["ELEVEN_API_KEY"] if "ELEVEN_API_KEY" in st.secrets else st.text_input("Enter your ElevenLabs API Key")
voice_id = "EXAVITQu4vr4xnSDxMaL"  # Rachel (default voice)

def generate_tts(text, voice_id, api_key):
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
    headers = {
        "xi-api-key": api_key,
        "Content-Type": "application/json"
    }
    payload = {
        "text": text,
        "voice_settings": {
            "stability": 0.4,
            "similarity_boost": 0.75
        }
    }
    response = requests.post(url, headers=headers, json=payload)
    return response.content if response.status_code == 200 else None

if st.button("🔊 Generate Voice"):
    if not api_key:
        st.warning("Please enter your ElevenLabs API key.")
    else:
        audio = generate_tts(mock_advice, voice_id, api_key)
        if audio:
            st.audio(audio, format="audio/mp3")
        else:
            st.error("Could not generate voice. Please check your API key.")

# === Footer ===
st.markdown("---")
st.markdown("Built by **Betheainnovation** | Powered by Streamlit, Plotly, Yahoo Finance, and ElevenLabs")

