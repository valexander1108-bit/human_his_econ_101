# pages/explore_map_timeline.py
import json
import pathlib
import pandas as pd
import streamlit as st
import folium
from streamlit_folium import st_folium

def timeline_app(MODULES=None, ALL_PAGES=None):
    # set_page_config can only be called once per run; guard to avoid duplicate-call errors
    try:
        st.set_page_config(page_title="Timeline Map", layout="wide")
    except Exception:
        pass

    # ---------- Load scenarios ----------
    DATA_PATH = pathlib.Path(__file__).resolve().parents[1] / "data" / "module1_scenarios.json"
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        scenarios = json.load(f)

    # Expect keys:
    # id, module, scenario, title, concept, date ("430 BCE" etc.), region, description, lat, lon, linked_model
    df = pd.DataFrame(scenarios)

    # Convert date -> numeric year (BCE negative)
    def to_year_num(s):
        s = str(s).strip()
        if s.lower().endswith("bce"):
            return -int("".join([c for c in s if c.isdigit()]))
        if s.lower().endswith("ce"):
            return int("".join([c for c in s if c.isdigit()]))
        # bare year defaults to CE
        return int("".join([c for c in s if (c.isdigit() or c == "-")]))

    if "year" not in df.columns:
        df["year"] = df["date"].apply(to_year_num)

    def pretty_year(y: int) -> str:
        return f"{abs(int(y))} BCE" if int(y) < 0 else f"{int(y)} CE"

    # ---------- Sidebar filters ----------
    st.sidebar.header("Filter")
    min_year, max_year = int(df["year"].min()), int(df["year"].max())
    year_min, year_max = st.sidebar.slider(
        "Time range",
        min_value=min_year,
        max_value=max_year,
        value=(min_year, max_year),
        step=1,
        format="%d",
        help="Drag to filter pins by year."
    )

    concepts = ["All"] + sorted(df["concept"].dropna().unique().tolist())
    concept_sel = st.sidebar.selectbox("Concept", concepts, index=0)

    modules = ["All"] + sorted(df["module"].dropna().unique().tolist())
    module_sel = st.sidebar.selectbox("Module", modules, index=0)

    f = df[(df["year"] >= year_min) & (df["year"] <= year_max)]
    if concept_sel != "All":
        f = f[f["concept"] == concept_sel]
    if module_sel != "All":
        f = f[f["module"] == module_sel]

    # ---------- Layout ----------
    left, right = st.columns([2, 1], vertical_alignment="top")

    with left:
        st.markdown(
            f"### Timeline Map — Showing {len(f)} scenario(s) "
            f"from **{pretty_year(year_min)}** to **{pretty_year(year_max)}**"
        )

        if not f.empty:
            center_lat, center_lon = f["lat"].mean(), f["lon"].mean()
            zoom_start = 3 if len(f) > 1 else 5
        else:
            center_lat, center_lon, zoom_start = 20, 0, 2

        # Clean academic basemap
        m = folium.Map(
            location=[center_lat, center_lon],
            zoom_start=zoom_start,
            tiles="CartoDB positron"
        )

        # Add clickable markers
        for _, row in f.iterrows():
            popup_html = f"""
            <b>{row['title']}</b><br>
            {row['module']}<br>
            {row['concept']} • {pretty_year(row['year'])}<br>
            <i>Click near this pin, then use the panel on the right.</i>
            """
            folium.Marker(
                location=[row["lat"], row["lon"]],
                tooltip=row["title"],
                popup=folium.Popup(popup_html, max_width=320),
                icon=folium.Icon(color="darkpurple", icon="book", prefix="fa")
            ).add_to(m)

        # Capture map interactions (lat/lon of last click)
        map_state = st_folium(m, width=None, height=620)

    with right:
        st.markdown("### Selected Scenario")

        selected = None

        # 1) If the user clicked the map, pick the nearest scenario in the filtered set
        last = map_state.get("last_object_clicked", None)
        if last and "lat" in last and "lng" in last and not f.empty:
            lat_clicked, lon_clicked = last["lat"], last["lng"]
            # simple L1 distance to nearest pin
            idx = ((f["lat"] - lat_clicked).abs() + (f["lon"] - lon_clicked).abs()).idxmin()
            selected = f.loc[idx].to_dict()

        # 2) Fallback: selection box
        labels = ["—"] + [f"{r['title']} ({pretty_year(int(r['year']))})" for _, r in f.iterrows()]
        label = st.selectbox("Or pick from list:", labels, index=0)
        if label != "—":
            ttl = label.split(" (")[0]
            yr_str = label.split("(")[-1].split(")")[0]
            yr = -int(yr_str.replace(" BCE", "")) if "BCE" in yr_str else int(yr_str.replace(" CE", ""))
            row = f[(f["title"] == ttl) & (f["year"] == yr)]
            if not row.empty:
                selected = row.iloc[0].to_dict()

        # Show details + navigation button
        if selected:
            st.subheader(selected["title"])
            st.caption(f"{selected['module']} • {selected['concept']} • {pretty_year(int(selected['year']))}")
            st.write(selected.get("description", ""))
            st.write(f"**Region:** {selected.get('region', '—')}")
            st.code(f"Scenario ID: {selected['id']}", language="text")

            # Stash selection for the model page
            if st.button("Open model", type="primary", use_container_width=True):
                st.session_state["selected_scenario"] = selected
                # Jump to the “Go to model” page (your 02_go_to_model.py)
                try:
                    st.switch_page("pages/02_go_to_model.py")
                except Exception:
                    st.success("Scenario stored. Use the sidebar to open ‘Go to model’.")
        else:
            st.info("Click a pin (or near it) on the map, or choose from the list.")