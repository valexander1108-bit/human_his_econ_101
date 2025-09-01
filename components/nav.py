# components/nav.py
import streamlit as st

def go_to(page_name: str):
    """Switch to Module Navigator and open the requested page."""
    st.session_state["nav_default_page"] = page_name
    st.session_state["mode_radio"] = "Module Navigator"
    st.experimental_rerun()