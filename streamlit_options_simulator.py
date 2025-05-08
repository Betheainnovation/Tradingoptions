import streamlit as st
import pandas as pd
import numpy as np

st.title("📈 Options Trading Growth Simulator")

# User inputs
starting_capital = st.number_input("Starting Capital ($)", min_value=100, value=5000, step=100)
months = st.slider("Months to Simulate", 1, 60, 24)
monthly_return_avg = st.slider("Average Monthly Return (%)", 1, 100, 30) / 100
monthly_return_stddev = st.slider("Return Variability (%)", 0, 50, 10) / 100
drawdown_limit = st.slider("Drawdown Floor (% of Peak)", 0, 100, 50) / 100

if st.button("Run Simulation"):
    np.random.seed(42)
    capital = starting_capital
    peak_capital = capital
    data = []

    for month in range(1, months + 1):
        monthly_return = np.random.normal(monthly_return_avg, monthly_return_stddev)
        capital *= max(1 + monthly_return, 0)
        peak_capital = max(capital, peak_capital)

        if capital < peak_capital * drawdown_limit:
            capital = peak_capital * drawdown_limit

        data.append({
            "Month": month,
            "Monthly Return (%)": round(monthly_return * 100, 2),
            "Projected Capital ($)": round(capital, 2),
            "Estimated Monthly Profit ($)": round(capital * monthly_return, 2)
        })

    df = pd.DataFrame(data)
    st.dataframe(df)

    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button("📥 Download CSV", data=csv, file_name="simulation_output.csv", mime='text/csv')
