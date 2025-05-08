import streamlit as st
from streamlit_option_menu import option_menu

st.set_page_config(page_title="Quant Fox", layout="wide")

selected = option_menu(
    menu_title=None,
    options=["Home", "App", "Contact"],
    icons=["house", "cpu", "envelope"],
    menu_icon="cast",
    default_index=0,
    orientation="horizontal",
    styles={
        "container": {"padding": "0!important", "background-color": "#0F1117"},
        "icon": {"color": "white", "font-size": "18px"},
        "nav-link": {"color": "white", "font-size": "16px", "text-align": "center", "margin":"0 1rem"},
        "nav-link-selected": {"background-color": "#1E90FF"},
    }
)

if selected == "Home":
    st.markdown("<iframe src='homepage.html' width='100%' height='1000'></iframe>", unsafe_allow_html=True)

elif selected == "App":
    exec(open("quant_fox_platform.py").read())

elif selected == "Contact":
    st.header("Contact Us")
    with st.form("contact_form"):
        name = st.text_input("Your Name")
        email = st.text_input("Your Email")
        subject = st.text_input("Subject")
        message = st.text_area("Message")
        submitted = st.form_submit_button("Send")
        if submitted:
            st.success("Thanks for reaching out. We'll respond shortly.")
