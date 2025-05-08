import streamlit as st
from streamlit_option_menu import option_menu

st.set_page_config(page_title="Quant Fox", layout="wide")

selected = option_menu(
    menu_title=None,
    options=["Home", "App", "Contact"],
    icons=["house", "cpu", "mail"],
    default_index=0,
    orientation="horizontal",
    styles={
        "container": {"padding": "0", "background-color": "#0F1117"},
        "nav-link": {"color": "#fff", "font-size": "16px", "text-align": "center"},
        "nav-link-selected": {"background-color": "#1E90FF"},
    }
)

if selected == "Home":
    with open("homepage.html", "r") as f:
        html = f.read()
    st.components.v1.html(html, height=1200, scrolling=True)

elif selected == "App":
    exec(open("quant_fox_platform.py").read())

elif selected == "Contact":
    st.title("Contact Us")
    st.markdown("Email: hello@quantfox.ai")
