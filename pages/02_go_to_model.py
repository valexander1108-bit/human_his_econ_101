# pages/02_go_to_model.py
import importlib
import inspect
import streamlit as st

st.set_page_config(page_title="Open Selected Model", layout="wide")
st.title("Go to model")

sel = st.session_state.get("selected_scenario")

# ---------- Guards ----------
if not sel:
    st.warning("No scenario selected yet. Go back to **Timeline Map** and choose one.")
    st.stop()

# soft display even if some keys are missing
title = sel.get("title", "Untitled Scenario")
module_label = sel.get("module", "Unknown Module")
concept_label = sel.get("concept", "Unknown Concept")
desc = sel.get("description", "")

st.markdown(f"**Scenario:** {title}")
st.caption(f"{module_label} • {concept_label}")
if desc:
    st.write(desc)

# ---------- Model registry ----------
MODEL_MAP = {
    "budget_line": "apps.budget_line",
    "ppc": "apps.ppc",
    "comparative_advantage": "apps.comparative_advantage",
    "supply_demand": "apps.supply_demand",
    "demand_schedule": "apps.demand_schedule",
    "supply_schedule": "apps.supply_schedule",
    "elasticity_demand": "apps.elasticity_demand",
    "elasticity_supply": "apps.elasticity_supply",
    "elasticity_tr": "apps.elasticity_tr",
    "static_equilibrium": "apps.static_equilibrium",
    "deadweight_loss": "apps.deadweight_loss",
    "surplus": "apps.surplus",
    "shifts_single": "apps.shifts_single",
    "shifts_double": "apps.shifts_double",
    "gov_int_p_floor": "apps.gov_int_p_floor",
    "gov_int_p_ceiling": "apps.gov_int_p_ceiling",
    "all_factors": "apps.all_factors",
    "land": "apps.land",
    "labor": "apps.labor",
    "labor_policy": "apps.labor_policy",
    "capital": "apps.capital",
    "utility": "apps.utility",
    "income_substitution": "apps.income_substitution",
    "optimal_choice": "apps.optimal_choice",
    "intertemporal_choice": "apps.intertemporal_choice",
    "capitalism_climate": "apps.capitalism_climate",
    "capitalism_inequality": "apps.capitalism_inequality",
    "cost_production": "apps.cost_production",
    "pc_profit": "apps.pc_profit",
    "shutdown_point": "apps.shutdown_point",
    "long_run_exit": "apps.long_run_exit",
    "economies_scale": "apps.economies_scale",
    "imperfect_competition": "apps.imperfect_competition",
    "game_theory": "apps.game_theory",
    "types_goods": "apps.types_goods",
    "public_goods_common_resources": "apps.public_goods_common_resources",
    "externalities_combined": "apps.externalities_combined",
    "competition_fairness": "apps.competition_fairness",
}

# linked_model can be a string or a dict with {"name": "...", "params": {...}}
linked = sel.get("linked_model")
if not linked:
    st.error("This scenario does not have a `linked_model` field.")
    st.stop()

if isinstance(linked, dict):
    linked_name = linked.get("name")
    linked_params = linked.get("params", {})
else:
    linked_name = str(linked)
    linked_params = {}

module_path = MODEL_MAP.get(linked_name)
if not module_path:
    st.error(
        f"Unknown linked_model '{linked_name}'.\n\n"
        "Fix either your JSON (linked_model) or add a mapping in `MODEL_MAP`."
    )
    with st.expander("Available MODEL_MAP keys"):
        st.write(sorted(MODEL_MAP.keys()))
    st.stop()

# ---------- Import & launch ----------
try:
    mod = importlib.import_module(module_path)
except Exception as e:
    st.error(f"Could not import module `{module_path}`.")
    st.exception(e)
    st.stop()

if not hasattr(mod, "app"):
    st.error(f"Module '{module_path}' has no `app()` function.")
    # help the user discover callable names
    funcs = [n for n, o in inspect.getmembers(mod, inspect.isfunction)]
    if funcs:
        st.info(f"Functions found in module: {funcs}")
    st.stop()

# Try to pass scenario if app(sel) is supported; otherwise call app() with no args
app_sig = inspect.signature(mod.app)
st.info(f"Launching **{linked_name}** …")

try:
    if len(app_sig.parameters) >= 1:
        # Common pattern: app(sel) or app(scenario=sel, **params)
        if "scenario" in app_sig.parameters:
            mod.app(scenario=sel, **linked_params)
        else:
            # pass as first positional if not named
            mod.app(sel, **linked_params)
    else:
        mod.app()
except TypeError:
    # Fallback: some apps only accept zero args
    mod.app()

# ---------- Debug panel (collapsible) ----------
with st.expander("Debug: selected_scenario payload"):
    st.json(sel)
