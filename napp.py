import requests
import streamlit as st

st.set_page_config(
    page_title="inMart - Barcode Scanner",
    layout="wide"
)
is_mobile = st.session_state.get("is_mobile", False)

st.markdown(
    """
    <h1 style="text-align:center;">🛒 inMart - Barcode Scanner</h1>
    <p style="text-align:center; color:gray;">
        Scan products to add them to your cart
    </p>
    """,
    unsafe_allow_html=True
)

