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

# === Custom CSS: typography only; colors come from .streamlit/config.toml ===
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@400;600;700&family=DM+Sans:wght@400;500;700&display=swap');

:root {
  --font-heading: "Cormorant Garamond", Georgia, serif;
  --font-body: "DM Sans", system-ui, -apple-system, Segoe UI, Roboto, Helvetica, Arial, sans-serif;
}

h1, h2, h3 { font-family: var(--font-heading); }
body, p, div, span, label { font-family: var(--font-body); }
</style>
""", unsafe_allow_html=True)

# --- Plotly template (optional) ---
import plotly.io as pio

pio.templates["ecn101"] = dict(
    layout=dict(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="DM Sans, sans-serif"),
        colorway=["#2f6f4e", "#b08b3e", "#4f6f8f", "#9a5b45", "#6f5d8c"],
        xaxis=dict(gridcolor="rgba(128,128,128,0.28)", zerolinecolor="rgba(128,128,128,0.45)"),
        yaxis=dict(gridcolor="rgba(128,128,128,0.28)", zerolinecolor="rgba(128,128,128,0.45)"),
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
    "Module 2 — ASYNC — Choice": [
        "Production Function and Marginal Product",
        "Labor-Leisure Choice",
        "Utility",
        "Optimal Choice",
        "Intertemporal Choice",
    ],
    "Module 3 — Supply and Demand": [
        "Demand (schedule → line)",
        "Supply (schedule → line)",
        "Market Model (Supply & Demand)",
        "Single Shifts",
        "Double Shifts",
    ],
    "Module 4 — Market Analysis: Elasticity & Efficiency": [
        "Price Elasticity of Demand",
        "Elasticity and Total Revenue",
        "Price Elasticity of Supply",
        "Surplus",
        "Government Intervention: Price Floor",
        "Government Intervention: Price Ceiling",
        "Deadweight Loss",
        "Tax Incidence",
    ],
    "Module 5 — Factor Markets": [
        "Derived Demand and VMP",
        "Land + Rent",
        "Labor + Wage",
        "Labor Market Policy",
        "Capital + Interest",
    ],
    "Module 6 — BRIDGE — Markets, History & Global Economy": [
        "Malthusian Trap and Demographic Transition",
        "Three Engines and the Great Divergence",
        "Poverty, GDP, and the Kuznets Curve",
        "Climate Externality and the Atmosphere Commons",
    ],
    "Module 7 — ASYNC — Structural Inequality: Core + Game Theory Preview": [
        "Structural Inequality Model",
        "Lorenz Curve and Gini Coefficient",
        "Credit Exclusion and Labor Power",
        "Game Theory Preview",
    ],
    "Module 8 — Structural Inequality: Extensions": [
        "Technology, AI Bias, and Climate Inequality",
        "Climate as Distributional Injustice",
        "AI Bias and Algorithmic Fairness",
    ],
    "Module 9 — Firms & Cost of Production": [
        "Economic vs Accounting Profit",
        "Cost of Production",
        "Economies of Scale",
    ],
    "Module 10 — Profit Maximization": [
        "Perfect Competition: Profit Maximization",
        "Perfect Competition: Shutdown Point",
        "Long-Run Equilibrium and Firm Exit",
        "Monopoly and Monopolistic Competition",
        "Price Discrimination",
    ],
    "Module 11 — Imperfect Competition & Game Theory": [
        "Monopolistic Competition and Oligopoly",
        "Game Theory",
        "Antitrust HHI and Merger Analysis",
        "Competition, Information, and Fairness",
    ],
    "Module 12 — Policy, Paradox & Human Perspectives": [
        "Types of Goods",
        "Public Goods and Common Resources",
        "Externalities and Pigouvian Policy",
        "Tax Incidence",
        "Game Theory",
        "Behavioral Policy",
        "GDP and Wellbeing Limits",
    ],
}
ALL_PAGES = [p for arr in MODULES.values() for p in arr]

# ---------- Session defaults ----------
DEFAULTS = {
    "mode": "Home",                   # "Home" | "Course Syllabus" | "Historical Map" | "Economic Models"
    "current_page": ALL_PAGES[0],
}
for k, v in DEFAULTS.items():
    if k not in st.session_state:
        st.session_state[k] = v
# Track when a non-radio action (e.g., a button) changed the canonical mode so we can sync the radio on the next run
if "mode_sync_needed" not in st.session_state:
    st.session_state["mode_sync_needed"] = False

# Honor deep links like ?model=Budget%20Constraint or ?view=syllabus.
# Query params are processed once per URL state so they do not keep
# overriding the sidebar mode selector after initial navigation.
params = st.query_params
VIEW_MODES = {
    "home": "Home",
    "syllabus": "Course Syllabus",
    "map": "Historical Map",
    "models": "Economic Models",
}
query_snapshot = tuple(sorted((key, str(value)) for key, value in params.items()))
if query_snapshot and query_snapshot != st.session_state.get("last_query_nav"):
    requested_view = params.get("view")
    if requested_view in VIEW_MODES:
        st.session_state["mode"] = VIEW_MODES[requested_view]
        st.session_state["mode_sync_needed"] = True
    elif "open_module" in params:
        st.session_state["mode"] = "Course Syllabus"
        st.session_state["mode_sync_needed"] = True

    if "model" in params:
        target = params.get("model")
        if target in ALL_PAGES:
            st.session_state["mode"] = "Economic Models"
            st.session_state["current_page"] = target
            st.session_state["mode_sync_needed"] = True
    st.session_state["last_query_nav"] = query_snapshot
elif not query_snapshot:
    st.session_state["last_query_nav"] = None

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
    elif page_name == "Production Function and Marginal Product":
        from apps.remaining_models import production_function_mp_app; production_function_mp_app()
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
    elif page_name == "Externalities and Pigouvian Policy":
        from apps.externality_subsidy import app as ext_sub_app; ext_sub_app()
    elif page_name == "Types of Goods":
        from apps.remaining_models import types_goods_app; types_goods_app()
    elif page_name == "Public Goods and Common Resources":
        from apps.priority_models import public_goods_common_resources_app; public_goods_common_resources_app()
    elif page_name == "Land + Rent":
        from apps.land import app as lan_app; lan_app()
    elif page_name == "Derived Demand and VMP":
        from apps.remaining_models import vmp_derived_demand_app; vmp_derived_demand_app()
    elif page_name == "Labor + Wage":
        from apps.labor import app as lab_app; lab_app()
    elif page_name == "Labor Market Policy":
        from apps.priority_models import labor_policy_app; labor_policy_app()
    elif page_name == "Credit Exclusion and Labor Power":
        from apps.remaining_models import credit_exclusion_labor_power_app; credit_exclusion_labor_power_app()
    elif page_name == "Capital + Interest":
        from apps.capital import app as cap_app; cap_app()
    elif page_name == "Utility":
        from apps.utility import app as util_app; util_app()
    elif page_name == "Optimal Choice":
        from apps.optimal_choice import app as oc_app; oc_app()
    elif page_name == "Labor-Leisure Choice":
        from apps.remaining_models import labor_leisure_app; labor_leisure_app()
    elif page_name == "Intertemporal Choice":
        from apps.intertemporal_choice import app as ic_app; ic_app()
    elif page_name == "Behavioral Policy":
        from apps.remaining_models import behavioral_policy_app; behavioral_policy_app()
    elif page_name in ("Malthus and Growth", "Malthusian Trap and Demographic Transition"):
        from apps.remaining_models import malthus_growth_app; malthus_growth_app()
    elif page_name in ("GDP and Wellbeing Limits", "Poverty, GDP, and the Kuznets Curve"):
        from apps.remaining_models import gdp_wellbeing_app; gdp_wellbeing_app()
    elif page_name in ("Capitalism and Climate Change", "Climate Externality and the Atmosphere Commons"):
        from apps.remaining_models import capitalism_climate_app; capitalism_climate_app()
    elif page_name in ("Capitalism and Global Inequality", "Global Inequality Model", "Structural Inequality Model", "Three Engines and the Great Divergence"):
        from apps.remaining_models import capitalism_inequality_app; capitalism_inequality_app()
    elif page_name == "Lorenz Curve and Gini Coefficient":
        from apps.remaining_models import lorenz_gini_app; lorenz_gini_app()
    elif page_name == "Economic vs Accounting Profit":
        from apps.remaining_models import economic_accounting_profit_app; economic_accounting_profit_app()
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
    elif page_name in ("Monopoly and Monopolistic Competition", "Monopolistic Competition and Oligopoly"):
        from apps.remaining_models import imperfect_competition_app; imperfect_competition_app()
    elif page_name == "Price Discrimination":
        from apps.remaining_models import price_discrimination_app; price_discrimination_app()
    elif page_name == "Game Theory":
        from apps.remaining_models import game_theory_app; game_theory_app()
    elif page_name == "Game Theory Preview":
        from apps.remaining_models import game_theory_preview_app; game_theory_preview_app()
    elif page_name == "Antitrust HHI and Merger Analysis":
        from apps.remaining_models import hhi_antitrust_app; hhi_antitrust_app()
    elif page_name == "Tax Incidence":
        from apps.remaining_models import tax_incidence_app; tax_incidence_app()
    elif page_name == "Technology, AI Bias, and Climate Inequality":
        from apps.remaining_models import technology_ai_climate_inequality_app; technology_ai_climate_inequality_app()
    elif page_name in ("Competition, Information, and Fairness", "AI Bias and Algorithmic Fairness"):
        from apps.remaining_models import competition_fairness_app; competition_fairness_app()
    elif page_name == "Climate as Distributional Injustice":
        from apps.remaining_models import climate_distributional_injustice_app; climate_distributional_injustice_app()
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
            st.session_state["syllabus_open_module"] = None
            st.session_state["last_query_nav"] = None
            st.query_params.clear()

    with col2:
        st.markdown("### 2. Historical Map")
        st.write(""" A global, interactive way to see how microeconomic ideas show up in:
   - Ancient and modern societies  
   - Real policies, institutions, and lived experience""")
        if st.button("Go to Historical Map"):
            st.session_state["mode"] = "Historical Map"
            st.session_state["mode_sync_needed"] = True
            st.session_state["syllabus_open_module"] = None
            st.session_state["last_query_nav"] = None
            st.query_params.clear()

    with col3:
        st.markdown("### 3. Economic Models")
        st.write(""" A microeconomic **model playground** where you can:
   - Experiment with budget constraints, PPCs, supply & demand, elasticity, and more!  
   - Use models for demos, review, or “just messing around” with no extra context.
    """)
        if st.button("Go to Model Playground"):
            st.session_state["mode"] = "Economic Models"
            st.session_state["mode_sync_needed"] = True
            st.session_state["syllabus_open_module"] = None
            st.session_state["last_query_nav"] = None
            st.query_params.clear()

    st.markdown("---")
    st.markdown("#### About Your Instructor")
    st.markdown("""
Prof. Alexander Velazquez's academic and professional work focuses on personal finance, public policy, and community-based organizing.

Prof. Velazquez grew up in South Jersey, graduated from Saint Joseph's University with an AB in Economics in 2020, and began teaching with Teach For America in Philadelphia at Boys' Latin Middle School. He later earned an MSEd in Urban Education from the University of Pennsylvania in 2022.

After teaching Special Education and Math in West Philadelphia for three years, Prof. Velazquez moved into personal finance, working as a tax specialist with H&R Block and as a financial specialist with ECS, a community-based nonprofit focused on ending intergenerational poverty for BIPOC communities.
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
        st.session_state["last_query_nav"] = None
        if mode != "Course Syllabus":
            st.session_state["syllabus_open_module"] = None
        st.query_params.clear()

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
