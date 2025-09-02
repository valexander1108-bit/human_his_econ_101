# streamlit_app.py
import streamlit as st

st.set_page_config(
    page_title="ECN101 Models",
    page_icon="📚",         # optional: replace with your favicon
    layout="wide",
    initial_sidebar_state="expanded",
)
# === Custom CSS: Google Fonts + brand tokens ===
st.markdown("""
<style>

/* 2) Design tokens—KEEP IN SYNC with .streamlit/config.toml */
:root{
  --brand-primary: #2B3A2E;         /* same as primaryColor */
  --bg: #F7F3E9;                    /* same as backgroundColor */
  --bg-2: #E9E3D5;                  /* same as secondaryBackgroundColor */
  --text: #1E1B16;                  /* same as textColor */
  --accent: #C49A6C;                /* optional: pick another Canva color */
  --font-heading: "Cormorant Garamond", serif;   /* Canva heading font */
  --font-body: "DM Sans", system-ui, -apple-system, Segoe UI, Roboto, "Helvetica Neue", Arial, "Noto Sans", "Liberation Sans", sans-serif;
}

/* 5) Sidebar background to Canva card color */
section[data-testid="stSidebar"] {
  background: var(--bg-2) !important;
}

/* 6) Buttons */
button[kind="primary"] {
  background: var(--brand-primary) !important;
  border: none !important;
}
button[kind="secondary"] {
  color: var(--brand-primary) !important;
  border-color: var(--brand-primary) !important;
}

/* 7) Links */
a, .stMarkdown a {
  color: var(--accent) !important;
  text-decoration: none;
}
a:hover { text-decoration: underline; }

""", unsafe_allow_html=True)
import plotly.io as pio

pio.templates["ecn101"] = dict(
    layout=dict(
        paper_bgcolor="#F7F3E9",   # match --bg
        plot_bgcolor="#F7F3E9",    # match --bg
        font=dict(family="DM Sans, sans-serif", color="#1E1B16"),
        colorway=[
            "#2B3A2E",  # primary
            "#C49A6C",  # accent
            "#6C7A61",  # muted green
            "#8B6B4A",  # warm brown
            "#3D4C3F",  # deep green
        ],
        xaxis=dict(gridcolor="#E0D9C9", zerolinecolor="#E0D9C9"),
        yaxis=dict(gridcolor="#E0D9C9", zerolinecolor="#E0D9C9"),
        legend=dict(borderwidth=0),
        margin=dict(l=40, r=20, t=40, b=40),
    )
)
pio.templates.default = "ecn101"
import streamlit as st

st.set_page_config(page_title="ECN101 Models", page_icon="🌍", layout="wide")

# ---------- Catalog ----------
MODULES = {
    "Module 1 — Modeling Foundations": [
        "Budget Constraint",
        "PPC",
        "Comparative Advantage",
    ],
    "Module 2 — Supply & Demand": [
        "Demand (schedule → line)",
        "Supply (schedule → line)",
        "Market Model (Supply & Demand)",
        "Single Shifts",
        "Double Shifts",
    ],
    "Module 3 — Elasticity": [
        "Price Elasticity of Demand",
        "Elasticity and Total Revenue",
        "Price Elasticity of Supply",
    ],
    "Module 4 — Welfare Economics": [
        "Surplus",
        "Government Intervention: Price Floor",
        "Government Intervention: Price Ceiling",
        "Deadweight Loss",
    ],
    "Module 5 — Factors of Production": [
        "Interdependent Factors",
        "Land + Rent",
        "Labor + Wage",
        "Capital + Interest",
    ],
}
ALL_PAGES = [p for arr in MODULES.values() for p in arr]

# ---------- Dispatch (lazy imports) ----------
def run_page(page_name: str):
    if page_name == "Budget Constraint":
        from apps.budget_line import app as bl_app; bl_app()
    elif page_name == "PPC":
        from apps.ppc import app as ppc_app; ppc_app()
    elif page_name == "Comparative Advantage":
        from apps.comparative_advantage import app as cp_app; cp_app()
    elif page_name == "Demand (schedule → line)":
        from apps.demand_schedule import app as ds_app; ds_app()
    elif page_name == "Supply (schedule → line)":
        from apps.supply_schedule import app as ss_app; ss_app()
    elif page_name == "Market Model (Supply & Demand)":
        from apps.supply_demand import app as sd_app; sd_app()
    elif page_name == "Single Shifts":
        from apps.shifts_single import app as sin_app; sin_app()
    elif page_name == "Double Shifts":
        from apps.shifts_double import app as dou_app; dou_app()
    elif page_name == "Price Elasticity of Demand":
        from apps.elasticity_demand import app as ed_app; ed_app()
    elif page_name == "Elasticity and Total Revenue":
        from apps.elasticity_tr import app as etr_app; etr_app()
    elif page_name == "Price Elasticity of Supply":
        from apps.elasticity_supply import app as es_app; es_app()
    elif page_name == "Surplus":
        from apps.surplus import app as sur_app; sur_app()
    elif page_name == "Government Intervention: Price Floor":
        from apps.gov_int_p_floor import app as flo_app; flo_app()
    elif page_name == "Government Intervention: Price Ceiling":
        from apps.gov_int_p_ceiling import app as cei_app; cei_app()
    elif page_name == "Deadweight Loss":
        from apps.deadweight_loss import app as dl_app; dl_app()
    elif page_name == "Interdependent Factors":
        from apps.all_factors import app as af_app; af_app()
    elif page_name == "Land + Rent":
        from apps.land import app as lan_app; lan_app()
    elif page_name == "Labor + Wage":
        from apps.labor import app as lab_app; lab_app()
    elif page_name == "Capital + Interest":
        from apps.capital import app as cap_app; cap_app()
    else:
        st.info("Coming soon…")

# ---------- Defaults (allow map deep-link) ----------
default_page = st.session_state.get("nav_default_page", ALL_PAGES[0])
default_module = next((m for m, pages in MODULES.items() if default_page in pages),
                      list(MODULES.keys())[0])

# ---------- Mode switch ----------
with st.sidebar:
    st.subheader("Mode")
    mode = st.radio("How should students start?",
                    ["Timeline Map", "Module Navigator"],
                    index=0, key="mode_radio")

    if mode == "Module Navigator":
        module = st.selectbox("Module", list(MODULES.keys()),
                              index=list(MODULES.keys()).index(default_module))
        page = st.selectbox("Page", MODULES[module],
                            index=MODULES[module].index(default_page)
                            if default_page in MODULES[module] else 0)
        st.session_state["nav_default_page"] = page

# consume one-shot defaults set by the map
st.session_state.pop("nav_default_page_once", None)

# ---------- Render ----------
if mode == "Timeline Map":
    from pages.explore_map_timeline import timeline_app as timeline_app
    timeline_app(MODULES, ALL_PAGES)  # pass for optional use
else:
    run_page(st.session_state["nav_default_page"])