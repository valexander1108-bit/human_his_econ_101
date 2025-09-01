# pages/_coming_soon.py
import streamlit as st

def app(page_title="Coming Soon"):
    st.title(page_title)
    st.markdown("---")

    st.markdown("""
    ## 🚧 Coming Soon 🚧  
    This interactive model is not available yet.  

    Please check back later as we continue to build out this section.  
    """)

    st.info("Tip: Use the sidebar to explore completed models.")
