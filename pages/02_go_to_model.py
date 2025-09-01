# pages/_02_go_to_model.py
import streamlit as st

def app(MODULES, run_page, default_page):
    st.title("Go to a Model")
    mod_names = list(MODULES.keys())
    default_mod = next((m for m, pages in MODULES.items() if default_page in pages), mod_names[0])

    col1, col2 = st.columns([1,1])
    with col1:
        module = st.selectbox("Module", mod_names, index=mod_names.index(default_mod))
    with col2:
        page = st.selectbox("Page", MODULES[module],
                            index=MODULES[module].index(default_page)
                                  if default_page in MODULES[module] else 0)

    if st.button("Open model"):
        st.session_state["nav_default_page"] = page
        st.experimental_rerun()