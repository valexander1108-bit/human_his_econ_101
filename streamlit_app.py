# streamlit_app.py — CLEAN
import sys

import streamlit as st

# Guard against partially-initialized pandas (can break Plotly template validation)
try:
    import pandas as pd  # noqa: F401
    if not hasattr(pd, "Series"):
        sys.modules.pop("pandas", None)
except Exception:
    sys.modules.pop("pandas", None)

st.set_page_config(
    page_title="Econ-Velazquez",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded",
)

# === Custom CSS: Google Fonts + brand tokens ===
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@400;600;700&family=DM+Sans:wght@400;500;700&display=swap');

:root{
  --brand-primary: #71bb94;
  --bg: #ededed;
  --bg-2: #ebdbc9;
  --text: #1C1B1B;
  --accent: #a69651;
  --font-heading: "Cormorant Garamond", serif;
  --font-body: "DM Sans", system-ui, -apple-system, Segoe UI, Roboto, "Helvetica Neue", Arial, "Noto Sans", "Liberation Sans", sans-serif;
}

section[data-testid="stSidebar"] { background: var(--bg-2) !important; }

button[kind="primary"] { background: var(--brand-primary) !important; border: none !important; }
button[kind="secondary"] { color: var(--brand-primary) !important; border-color: var(--brand-primary) !important; }

a, .stMarkdown a { color: var(--accent) !important; text-decoration: none; }
a:hover { text-decoration: underline; }
</style>
""", unsafe_allow_html=True)

# --- Plotly template (optional) ---
import plotly.io as pio
pio.templates["ecn101"] = dict(
    layout=dict(
        paper_bgcolor="#555252",
        plot_bgcolor="#ededed",
        font=dict(family="DM Sans, sans-serif", color="#1C1B1B"),
        colorway=["#1d511e", "#C49A6C", "#6C7A61", "#8B6B4A", "#563b19"],
        xaxis=dict(gridcolor="#696867", zerolinecolor="#B5881F"),
        yaxis=dict(gridcolor="#696867", zerolinecolor="#B38210"),
        legend=dict(borderwidth=0),
        margin=dict(l=40, r=20, t=40, b=40),
    )
)
pio.templates.default = "ecn101"

# ---------- Catalog (match course syllabus modules) ----------
MODULES = {
    "Module 1 — Economic Thought & Modeling": [
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
    "Module 4 — Welfare & Intervention": [
        "Surplus",
        "Government Intervention: Price Floor",
        "Government Intervention: Price Ceiling",
        "Deadweight Loss",
    ],
    "Module 5 — Factors of Production": [
        "Interdependent Factors",
        "Land + Rent",
        "Labor + Wage",
        "Labor Market Policy",
        "Capital + Interest",
    ],
    "Module 6 — Choices & Constraints": [
        "Utility",
        "Income and Substitution Effects",
        "Optimal Choice",
        "Intertemporal Choice",
    ],
    "Module 7 — Capitalism": [
        "Capitalism and Climate Change",
        "Capitalism and Global Inequality",
    ],
    "Module 8 — Inequality": [
        "Global Inequality Model",
        "Competition and Fairness",
    ],
    "Module 9 — Cost of Production": [
        "Cost of Production",
        "Economies of Scale",
    ],
    "Module 10 — Profit Maximization": [
        "Perfect Competition: Profit Maximization",
        "Perfect Competition: Shutdown Point",
        "Long-Run Equilibrium and Firm Exit",
        "Monopoly and Monopolistic Competition",
    ],
    "Module 11 — Competition & Information": [
        "Game Theory",
        "Types of Goods",
        "Public Goods and Common Resources",
        "Competition, Information, and Fairness",
    ],
    "Module 12 — Policy, Paradox & Human Perspective": [
        "Policy: Public Goods and Common Resources",
        "Externalities: Positive and Negative",
        "Externality: Social Cost (Pigouvian Tax)",
        "Externality: Social Benefit (Pigouvian Subsidy)",
        "Climate Policy and Capitalism",
    ],
}
ALL_PAGES = [p for arr in MODULES.values() for p in arr]

# ---------- Session defaults ----------
DEFAULTS = {
    "mode": "Home",                   # "Home" | "Course Syllabus" | "Historical Map" | "Economic Models"
    "current_page": ALL_PAGES[0],
    "selected_scenario": None,
}
for k, v in DEFAULTS.items():
    if k not in st.session_state:
        st.session_state[k] = v
# Track when a non-radio action (e.g., a button) changed the canonical mode so we can sync the radio on the next run
if "mode_sync_needed" not in st.session_state:
    st.session_state["mode_sync_needed"] = False

# Honor deep links like ?model=Budget%20Constraint
params = st.query_params
if "model" in params:
    target = params.get("model")
    if target in ALL_PAGES:
        st.session_state["mode"] = "Economic Models"
        st.session_state["current_page"] = target
        st.session_state["mode_sync_needed"] = True

# The radio owns its own key; seed it once, and only resync when a button flagged it
if "mode_radio" not in st.session_state:
    st.session_state["mode_radio"] = st.session_state["mode"]
if st.session_state["mode_sync_needed"]:
    st.session_state["mode_radio"] = st.session_state["mode"]
    st.session_state["mode_sync_needed"] = False

# ---------- Lazy page dispatcher ----------
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
    elif page_name == "Externality: Social Cost (Pigouvian Tax)":
        from apps.externality_tax import app as ext_tax_app; ext_tax_app()
    elif page_name == "Externality: Social Benefit (Pigouvian Subsidy)":
        from apps.externality_subsidy import app as ext_sub_app; ext_sub_app()
    elif page_name == "Interdependent Factors":
        from apps.all_factors import app as af_app; af_app()
    elif page_name == "Land + Rent":
        from apps.land import app as lan_app; lan_app()
    elif page_name == "Labor + Wage":
        from apps.labor import app as lab_app; lab_app()
    elif page_name == "Labor Market Policy":
        from apps.priority_models import labor_policy_app; labor_policy_app()
    elif page_name == "Capital + Interest":
        from apps.capital import app as cap_app; cap_app()
    elif page_name == "Utility":
        from apps.utility import app as util_app; util_app()
    elif page_name == "Income and Substitution Effects":
        from apps.priority_models import income_substitution_app; income_substitution_app()
    elif page_name == "Optimal Choice":
        from apps.optimal_choice import app as oc_app; oc_app()
    elif page_name == "Intertemporal Choice":
        from apps.intertemporal_choice import app as ic_app; ic_app()
    elif page_name == "Capitalism and Climate Change":
        from apps.remaining_models import capitalism_climate_app; capitalism_climate_app()
    elif page_name in ("Capitalism and Global Inequality", "Global Inequality Model"):
        from apps.remaining_models import capitalism_inequality_app; capitalism_inequality_app()
    elif page_name == "Cost of Production":
        from apps.remaining_models import cost_production_app; cost_production_app()
    elif page_name == "Perfect Competition: Profit Maximization":
        from apps.remaining_models import pc_profit_app; pc_profit_app()
    elif page_name == "Perfect Competition: Shutdown Point":
        from apps.remaining_models import shutdown_app; shutdown_app()
    elif page_name == "Long-Run Equilibrium and Firm Exit":
        from apps.remaining_models import long_run_exit_app; long_run_exit_app()
    elif page_name == "Economies of Scale":
        from apps.remaining_models import economies_scale_app; economies_scale_app()
    elif page_name == "Monopoly and Monopolistic Competition":
        from apps.remaining_models import imperfect_competition_app; imperfect_competition_app()
    elif page_name == "Game Theory":
        from apps.remaining_models import game_theory_app; game_theory_app()
    elif page_name == "Types of Goods":
        from apps.remaining_models import types_goods_app; types_goods_app()
    elif page_name in ("Public Goods and Common Resources", "Policy: Public Goods and Common Resources"):
        from apps.priority_models import public_goods_common_resources_app; public_goods_common_resources_app()
    elif page_name == "Externalities: Positive and Negative":
        from apps.remaining_models import externalities_combined_app; externalities_combined_app()
    elif page_name in ("Competition and Fairness", "Competition, Information, and Fairness"):
        from apps.remaining_models import competition_fairness_app; competition_fairness_app()
    elif page_name == "Climate Policy and Capitalism":
        from apps.remaining_models import capitalism_climate_app; capitalism_climate_app()
    else:
        st.info("Coming soon…")
# ---------- Home ----------
def render_home():
    st.title("ECON 101: Introduction to Microeconomics")
    st.subheader("Course Hub — Alexander R. Velazquez")

    st.markdown("""**Welcome!** This app brings together three ways to explore **microeconomics** with Professor Velazquez:""")

    st.markdown("---")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("### 1. Course Syllabus")
        st.write(""" A structured, module-by-module knowledge base with:
   - Intuition & big ideas  
   - Tiered learning objectives """)
        if st.button("Go to Syllabus"):
            st.session_state["mode"] = "Course Syllabus"
            st.session_state["mode_sync_needed"] = True

    with col2:
        st.markdown("### 2. Historical Map")
        st.write(""" A global, interactive way to see how microeconomic ideas show up in:
   - Ancient and modern societies  
   - Real policies, institutions, and lived experience""")
        if st.button("Go to Historical Map"):
            st.session_state["mode"] = "Historical Map"
            st.session_state["mode_sync_needed"] = True

    with col3:
        st.markdown("### 3. Economic Models")
        st.write(""" A microeconomic **model playground** where you can:
   - Experiment with budget constraints, PPCs, supply & demand, elasticity, and more!  
   - Use models for demos, review, or “just messing around” with no extra context.
    """)
        if st.button("Go to Model Playground"):
            st.session_state["mode"] = "Economic Models"
            st.session_state["mode_sync_needed"] = True

    st.markdown("---")
    st.markdown("#### About Your Instructor")
    st.markdown("""
_Placeholder: a short bio line about you here — your role, institution(s), and what you care about in teaching econ._

You can mention office hours, email, or a link to your full syllabus/website if you want.
    """)

# ---------- Sidebar ----------
with st.sidebar:
    st.subheader("Mode Selector")

    mode_options = ["Home", "Course Syllabus", "Historical Map", "Economic Models"]
    mode = st.radio(
        "How would you like to explore economics?",
        mode_options,
        key="mode_radio",
    )
    # Single source of truth for mode; radio writes it here when changed
    if mode != st.session_state["mode"]:
        st.session_state["mode"] = mode

    if mode == "Economic Models":
        # pick module/page; update single source of truth
        modules_list = list(MODULES.keys())
        current_page = st.session_state.get("current_page", ALL_PAGES[0])
        current_module = next((m for m, pages in MODULES.items() if current_page in pages), modules_list[0])
        module_index = modules_list.index(current_module) if current_module in modules_list else 0

        module = st.selectbox("Module", modules_list, index=module_index)
        pages = MODULES[module]

        if pages:
            page_index = pages.index(current_page) if current_page in pages else 0
            page = st.selectbox("Page", pages, index=page_index)
            st.session_state["current_page"] = page
        else:
            st.info("No interactive models for this module yet.")
            st.session_state["current_page"] = current_page

# ---------- Render ----------
mode = st.session_state.get("mode", "Home")

if mode == "Home":
    render_home()

elif mode == "Course Syllabus":
    from pages.course_syllabus import app as syllabus_app
    syllabus_app()

elif mode == "Historical Map":
    from pages.explore_map_timeline import timeline_app
    timeline_app(MODULES, ALL_PAGES)

elif mode == "Economic Models":
    run_page(st.session_state["current_page"])
