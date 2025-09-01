# pages/_01_explore_map_timeline.py
import json
from pathlib import Path
import pandas as pd
import pydeck as pdk
import streamlit as st
from components.nav import go_to

MODEL_MAP = {
    "1_budget_constraint": "Budget Constraint",
    "2_ppc": "PPC",
    "3_comparative_advantage": "Comparative Advantage",
    # add more as you expand the knowledge base
}

def app(MODULES=None, ALL_PAGES=None):
    st.title("Explore the Timeline Map")

    # Load scenarios
    data_files = [Path("data/module1_scenarios.json")]  # extend as you add more modules
    records = []
    for p in data_files:
        if p.exists():
            with p.open("r", encoding="utf-8") as f:
                items = json.load(f)
                if isinstance(items, list):
                    records.extend(items)

    if not records:
        st.warning("No scenarios found. Add data/module1_scenarios.json.")
        return

    df = pd.DataFrame(records)
    df = df.dropna(subset=["lat", "lon"])
    if df.empty:
        st.warning("No scenarios have coordinates yet (lat/lon).")
        return

    df["tooltip"] = (df["title"].fillna("") +
                     df.get("period", "").fillna("").radd(" — ").replace(" — ", "", regex=False))

    view = pdk.ViewState(
        latitude=float(df["lat"].mean()),
        longitude=float(df["lon"].mean()),
        zoom=2.3,
        pitch=0
    )

    layer = pdk.Layer(
        "ScatterplotLayer",
        data=df,
        get_position="[lon, lat]",
        get_radius=200000,
        pickable=True,
        auto_highlight=True,
    )
    deck = pdk.Deck(layers=[layer], initial_view_state=view,
                    tooltip={"text": "{tooltip}"})
    st.pydeck_chart(deck)

    st.subheader("Scenarios")
    for _, r in df.iterrows():
        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown(f"**{r['title']}**")
            st.caption(" • ".join(x for x in [
                r.get("region"), r.get("period"), r.get("date")
            ] if x))
            if r.get("description"):
                st.write(r["description"])
        with col2:
            page = MODEL_MAP.get(r.get("linked_model"))
            if page and st.button("Open model →", key=f"open_{r['id']}"):
                go_to(page)
        st.divider()