import streamlit as st
st.set_page_config(page_title="Quant Fox", layout="wide")  # ✅ Must be here first

from streamlit_option_menu import option_menu

selected = option_menu(
    menu_title=None,
    options=["Home", "App", "Contact"],
    icons=["house", "cpu", "mail"],
    default_index=0,
    orientation="horizontal",
)

if selected == "Home":
    with open("homepage.html", "r") as f:
        st.components.v1.html(f.read(), height=1300)

elif selected == "App":
    import quant_fox_platform_module  # ✅ now safe to import

elif selected == "Contact":
    st.title("Contact Us")
    st.write("Email: support@quantfox.ai")

import streamlit as st
from streamlit_option_menu import option_menu

# ✅ Set page config FIRST — before anything else
st.set_page_config(page_title="Quant Fox", layout="wide")

# Navigation bar
selected = option_menu(
    menu_title=None,
    options=["Home", "App", "Contact"],
    icons=["house", "cpu", "mail"],
    default_index=0,
    orientation="horizontal",
    styles={
        "container": {"padding": "0!important", "background-color": "#0F1117"},
        "nav-link": {"color": "#fff", "font-size": "16px", "text-align": "center"},
        "nav-link-selected": {"background-color": "#1E90FF"},
    }
)

# Routes
if selected == "Home":
    with open("homepage.html", "r") as f:
        st.components.v1.html(f.read(), height=1300, scrolling=True)

elif selected == "App":
    import quant_fox_platform_module  # ✅ This now loads correctly

elif selected == "Contact":
    st.title("Contact Us")
    st.markdown("📧 Email: support@quantfox.ai")
