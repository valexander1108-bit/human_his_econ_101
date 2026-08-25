# pages/explore_map_timeline.py
import json
import pathlib
import re
import math
from typing import Any, Dict, Optional, Tuple

import pandas as pd
import streamlit as st
import folium
from folium.plugins import MarkerCluster, MiniMap, Fullscreen, HeatMap, TimestampedGeoJson
from streamlit_folium import st_folium


# =========================
# Year parsing & formatting
# =========================
def parse_year(value) -> Optional[int]:
    """
    Convert common historical year strings to an integer timeline.
    Rules:
      - '1200 BCE' → -1200
      - '200 CE' or '200' → 200
      - '-350' → -350
      - 'c. 1200 BCE', '1200–1000 BCE', '1200-1000 BCE' → midpoint
      - None / unparsable → None
    """
    if value is None:
        return None
    if isinstance(value, (int, float)) and not (isinstance(value, float) and math.isnan(value)):
        return int(value)

    s = str(value).strip().upper()
    if not s:
        return None

    # quick numeric like "-350" or "350"
    if re.fullmatch(r"-?\d{1,5}", s):
        return int(s)

    # remove circa and normalize dashes
    s = re.sub(r"\bC\.?\s*", "", s)  # remove leading "c." or "C."
    s = s.replace("–", "-")

    # range, e.g. "1200-1000 BCE" or "200-100 CE" or "200-100"
    m = re.match(r"^(\d{1,5})\s*-\s*(\d{1,5})\s*(BCE|BC|CE|AD)?$", s)
    if m:
        a, b, era = m.groups()
        a, b = int(a), int(b)
        if era in ("BCE", "BC"):
            a, b = -a, -b
        # midpoint of the range
        return int(round((a + b) / 2))

    # single with/without era, e.g. "1200 BCE", "200 CE", "AD 200"
    m = re.match(r"^(AD\s+)?(\d{1,5})\s*(BCE|BC|CE|AD)?$", s)
    if m:
        _, n, era = m.groups()
        n = int(n)
        if era in ("BCE", "BC"):
            return -n
        # CE/AD or no era defaults to positive
        return n

    return None


def pretty_year(n: int) -> str:
    return f"{abs(int(n))} BCE" if int(n) < 0 else (f"{int(n)} CE" if int(n) != 0 else "0")


def pretty_year_safe(val: Any) -> str:
    try:
        s = str(val).strip()
        if any(x in s.upper() for x in ["BCE", "CE"]):
            return s
        y = int(s)
        return pretty_year(y)
    except Exception:
        return str(val) if val else "—"


# =========================
# UI helpers
# =========================
def badge(text: str, variant: str = "neutral"):
    colors = {"neutral": "#E9E3D5", "concept": "#D6E4FF", "module": "#E8F5E9", "time": "#FFF3E0"}
    return f"""<span style="display:inline-block;margin-right:.35rem;margin-bottom:.35rem;
        padding:.18rem .55rem;border-radius:999px;background:{colors.get(variant, colors['neutral'])};
        font-size:.85rem;line-height:1;">{text}</span>"""


def field(label: str, value: Any):
    v = value if (value not in [None, "", [], {}]) else "—"
    return f"<div style='margin:.2rem 0;'><b>{label}:</b> {v}</div>"


def external_link(label: str, url: str):
    if not url:
        return ""
    return f"<a href='{url}' target='_blank' rel='noopener noreferrer'>{label} ↗</a>"


def render_selected_card(selected: Dict[str, Any]):
    title = selected.get("title") or "Untitled Scenario"
    # Prefer year_num for formatting; fall back to original text
    year_num = selected.get("year_num")
    year_txt = selected.get("year") or selected.get("date")
    concept = selected.get("concept") or "—"
    module = selected.get("module") or "—"
    period = selected.get("period") or "—"
    region = selected.get("region") or selected.get("Region/Civ") or "—"
    desc = selected.get("description") or selected.get("Narrative") or ""
    lat, lon = selected.get("lat"), selected.get("lon")
    rr_link = selected.get("rr") or selected.get("period")  # if you sometimes tuck RR in 'period'
    source = selected.get("source") or selected.get("Source")
    model = selected.get("linked_model") or selected.get("linked model")
    actors = selected.get("actors")
    tradeoffs = (selected.get("tradeoffs") or selected.get("Trade-offs") or selected.get("econ_concept"))
    links = selected.get("links") or []
    tags = selected.get("tags") or []
    coordinate_note = selected.get("coordinate_note")
    artifact = selected.get("historical_artifact") or selected.get("artifact")

    st.markdown(f"## {title}")
    chips = "".join([
        badge(pretty_year(year_num) if year_num is not None else pretty_year_safe(year_txt), "time"),
        badge(concept, "concept"),
        badge(module, "module"),
    ])
    if isinstance(tags, str):
        tags = [t.strip() for t in tags.split(",") if t.strip()]
    chips += "".join([badge(t, "neutral") for t in tags[:8]])
    st.markdown(chips, unsafe_allow_html=True)
    st.markdown("**Overview**")
    facts = ""
    facts += field("Region", region)
    facts += field("Period", period)
    if lat is not None and lon is not None:
        facts += field("Coordinates", f"{float(lat):.4f}, {float(lon):.4f}")
    if coordinate_note:
        facts += field("Coordinate note", coordinate_note)
    if artifact:
        if isinstance(artifact, dict):
            artifact_value = artifact.get("name") or artifact.get("title") or artifact
        else:
            artifact_value = artifact
        facts += field("Historical artifact", artifact_value)
    if source:
        facts += field("Source", source)
    if model:
        facts += field("Model", model)
    st.markdown(facts, unsafe_allow_html=True)
    if desc:
            st.write(desc)
    with st.expander("Economic Decision", expanded=False):
            if tradeoffs:
                if isinstance(tradeoffs, (list, tuple)):
                    for t in tradeoffs:
                        st.write(f"- {t}")
                else:
                    st.write(tradeoffs)
            else:
                st.caption("Add a `tradeoffs` field in your JSON to show key decisions here.")
    if actors:
            with st.expander("Actors", expanded=False):
                if isinstance(actors, (list, tuple)):
                    for a in actors:
                        st.write(f"- {a}")
                else:
                    st.write(actors)


    link_lines = []

    if rr_link and isinstance(rr_link, str) and rr_link.startswith("http"):
            link_lines.append(external_link("RunningReality", rr_link))
    if links and isinstance(links, str) and links.startswith("http"):
            link_lines.append(external_link("Artifacts", links))
    if link_lines:
            st.markdown("Time Machines")
            for L in link_lines:
                st.markdown(f"- {L}", unsafe_allow_html=True)

# =========================
# Main app
# =========================
def timeline_app(MODULES=None, ALL_PAGES=None):
    # set_page_config can only be called once per run; guard to avoid duplicate-call errors
    try:
        st.set_page_config(page_title="Timeline Map", layout="wide")
    except Exception:
        pass

    # ---------- Load scenarios ----------
    data_dir = pathlib.Path(__file__).resolve().parents[1] / "data"
    DATA_PATH = data_dir / "historical_map_scenarios.json"
    if not DATA_PATH.exists():
        DATA_PATH = data_dir / "final_build_scenarios.json"
    if not DATA_PATH.exists():
        DATA_PATH = data_dir / "module1_scenarios.json"
    if not DATA_PATH.exists():
        st.error(f"Could not find scenarios file at: {DATA_PATH}")
        return

    with open(DATA_PATH, "r", encoding="utf-8") as f:
        scenarios = json.load(f)

    df = pd.DataFrame(scenarios)

    # Determine source column for year parsing
    source_col = "year" if "year" in df.columns else ("date" if "date" in df.columns else None)
    if source_col is None:
        st.error("Scenarios need a 'year' or 'date' field.")
        return

    # Normalize to numeric year
    df["year_num"] = df[source_col].map(parse_year)
    df = df.dropna(subset=["year_num"]).copy()
    df["year_num"] = df["year_num"].astype(int)

    # ---------- Sidebar filters ----------
    st.sidebar.header("Filter")
    yr_min = int(df["year_num"].min())
    yr_max = int(df["year_num"].max())
    year_min, year_max = st.sidebar.slider(
        "Time range (BCE negative, CE positive)",
        min_value=yr_min,
        max_value=yr_max,
        value=(yr_min, yr_max),
        step=10,
        format="%d",
        help="Drag to filter pins by year."
    )

    concepts = ["All"] + sorted([c for c in df.get("concept", pd.Series(dtype=str)).dropna().unique().tolist()])
    concept_sel = st.sidebar.selectbox("Concept", concepts, index=0)

    modules = ["All"] + sorted([m for m in df.get("module", pd.Series(dtype=str)).dropna().unique().tolist()])
    module_sel = st.sidebar.selectbox("Module", modules, index=0)

    st.sidebar.header("Map Layers")
    cluster_pins = st.sidebar.checkbox(
        "Cluster nearby pins",
        value=False,
        help="Turn on for dense views; leave off to see individual scenarios while zoomed out.",
    )
    show_heat = st.sidebar.checkbox("Show heat/density", value=False)
    show_time = st.sidebar.checkbox(
        "Show time slider",
        value=False,
        help="Animate pins over time; can be slow with many points",
    )

    f = df[(df["year_num"] >= year_min) & (df["year_num"] <= year_max)]
    if concept_sel != "All" and "concept" in f.columns:
        f = f[f["concept"] == concept_sel]
    if module_sel != "All" and "module" in f.columns:
        f = f[f["module"] == module_sel]
    # ---------- Layout ----------
    left, right = st.columns([2, 1])

    with left:
        st.markdown(
            f"### Historical Map "
            f"from **{pretty_year(year_min)}** to **{pretty_year(year_max)}**"
        )
        st.caption(f"{len(f)} scenario(s) shown.")

        if not f.empty and {"lat", "lon"}.issubset(f.columns):
            center_lat, center_lon = f["lat"].mean(), f["lon"].mean()
            zoom_start = 3 if len(f) > 1 else 5
        else:
            center_lat, center_lon, zoom_start = 20, 0, 2

        # Standard light basemap
        m = folium.Map(
            location=[center_lat, center_lon],
            zoom_start=zoom_start,
            tiles="OpenStreetMap",
            control_scale=False,
        )
        Fullscreen(position="topleft").add_to(m)
        MiniMap(toggle_display=True, position="bottomleft").add_to(m)

        bounds = []
        if not f.empty and {"lat", "lon"}.issubset(f.columns):
            marker_layer = (
                MarkerCluster(name="Scenarios", disableClusteringAtZoom=7)
                if cluster_pins
                else folium.FeatureGroup(name="Scenarios")
            )
            heat_points = []
            for _, row in f.iterrows():
                if pd.isna(row.get("lat")) or pd.isna(row.get("lon")):
                    continue
                bounds.append((row["lat"], row["lon"]))
                heat_points.append([row["lat"], row["lon"], 1])
                desc_snip = (row.get("description") or row.get("Narrative") or "")
                if len(desc_snip) > 140:
                    desc_snip = desc_snip[:140] + "..."
                artifact = row.get("historical_artifact")
                if isinstance(artifact, dict):
                    artifact_name = artifact.get("name", "")
                else:
                    artifact_name = artifact or ""
                popup_html = f"""
                <div style="font-size:14px; line-height:1.4;">
                    <b>{row.get('title','Untitled')}</b><br>
                    <span style="color:#71bb94;">{pretty_year(int(row['year_num']))}</span><br>
                    <i>{row.get('concept','—')} • {row.get('module','—')}</i><br>
                    <div style="margin-top:4px; font-size:12px;"><b>Artifact:</b> {artifact_name}</div>
                    <div style="margin-top:4px; font-size:12px;">{desc_snip}</div>
                </div>
                """
                folium.Marker(
                    location=[row["lat"], row["lon"]],
                    tooltip=row.get("title", "Scenario"),
                    popup=folium.Popup(popup_html, max_width=300),
                    icon=folium.Icon(color="green", icon="book", prefix="fa")
                ).add_to(marker_layer)
            marker_layer.add_to(m)

            if show_heat and heat_points:
                HeatMap(heat_points, radius=18, blur=24, min_opacity=0.3, name="Density").add_to(m)

            if show_time:
                if len(f) > 400:
                    st.warning("Time slider disabled (too many points for smooth playback). Filter more or turn off.")
                else:
                    features = []
                    for _, row in f.iterrows():
                        if pd.isna(row.get("lat")) or pd.isna(row.get("lon")):
                            continue
                        year_label = pretty_year(int(row["year_num"]))
                        feat = {
                            "type": "Feature",
                            "geometry": {"type": "Point", "coordinates": [row["lon"], row["lat"]]},
                            "properties": {
                                "time": f"{int(row['year_num'])}",
                                "popup": f"{row.get('title','Untitled')} — {year_label} — {row.get('concept','—')} • {row.get('module','—')}",
                            },
                        }
                        features.append(feat)
                if features:
                    TimestampedGeoJson(
                        {"type": "FeatureCollection", "features": features},
                        transition_time=500,
                        loop=False,
                        add_last_point=True,
                        period="PT1S",
                        auto_play=False,
                        time_slider_drag_update=True,
                    ).add_to(m)

            if bounds:
                m.fit_bounds(bounds, padding=(20, 20))
            folium.LayerControl(collapsed=True).add_to(m)

        map_state = st_folium(m, width=None, height=620)

    with right:
        st.markdown("### Selected Scenario")

        selected = None

        # 1) If the user clicked the map, pick nearest scenario in filtered set
        last = map_state.get("last_object_clicked", None) if isinstance(map_state, dict) else None
        if last and "lat" in last and "lng" in last and not f.empty and {"lat", "lon"}.issubset(f.columns):
            lat_clicked, lon_clicked = last["lat"], last["lng"]
            idx = ((f["lat"] - lat_clicked).abs() + (f["lon"] - lon_clicked).abs()).idxmin()
            selected = f.loc[idx].to_dict()

        # 2) Fallback: selection box
        labels = ["—"] + [f"{r.get('title','Untitled')} ({pretty_year(int(r['year_num']))})" for _, r in f.iterrows()]
        label = st.selectbox("Or pick from list:", labels, index=0)
        if label != "—":
            ttl = label.split(" (")[0]
            yr_str = label.split("(")[-1].split(")")[0]
            yr = -int(yr_str.replace(" BCE", "")) if "BCE" in yr_str else int(yr_str.replace(" CE", ""))
            row = f[(f["title"] == ttl) & (f["year_num"] == yr)]
            if not row.empty:
                selected = row.iloc[0].to_dict()

        # Show details
        if selected:
            render_selected_card(selected)
        else:
            st.info("Click a pin on the map, or choose from the list.")
