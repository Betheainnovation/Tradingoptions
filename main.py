from streamlit_option_menu import option_menu
import streamlit as st

st.set_page_config(page_title="Quant Fox", layout="wide")

selected = option_menu(
    menu_title=None,
    options=["Home", "App", "Contact"],
    icons=["house", "cpu", "mail"],
    default_index=0,
    orientation="horizontal"
)

if selected == "Home":
    with open("homepage.html", "r") as f:
        st.components.v1.html(f.read(), height=1000)
elif selected == "App":
    import quant_fox_platform_module
elif selected == "Contact":
    st.title("Contact")
    st.write("Email: support@quantfox.ai")
