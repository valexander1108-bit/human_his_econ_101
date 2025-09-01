import copy
import streamlit as st
import plotly.graph_objects as go

# ---------- helpers ----------
def intercepts(M, px, py):
    """Return x- and y-intercepts for budget line M = px*x + py*y."""
    x_int = M / max(px, 1e-9)
    y_int = M / max(py, 1e-9)
    return x_int, y_int

def slope(px, py):
    """Slope of budget line in (x,y) space is -px/py."""
    return -(px / max(py, 1e-9))

def apply_shift(cur, shift_type, mode, delta):
    """
    Return a NEW dict (M, px, py) after applying a shift to the current parameters.
      - shift_type ∈ {"M", "px", "py"}
      - mode ∈ {"percent", "absolute"}
      - delta is the change amount (float)
    """
    nxt = copy.deepcopy(cur)
    key = shift_type

    if mode == "percent":
        # percent like +10 means +10%
        factor = 1.0 + (delta / 100.0)
        nxt[key] = max(nxt[key] * factor, 1e-9)
    else:
        # absolute shift: add delta directly (guard positivity)
        nxt[key] = max(nxt[key] + delta, 1e-9)

    return nxt


# ---------- main app ----------
def app():
    st.subheader("Budget Constraint - A Choice Between Two Quantities")

    # ---- Sidebar: 1) Baseline inputs ----
    with st.sidebar.expander("1) Baseline (starting inputs)", expanded=False):
        base_M  = st.number_input("Income M", min_value=0.01, value=30.0, step=1.0, format="%.2f", key="bl_base_M")
        base_px = st.number_input("Price of X (pₓ)", min_value=0.01, value=1.0, step=0.1, format="%.2f", key="bl_base_px")
        base_py = st.number_input("Price of Y (pᵧ)", min_value=0.01, value=1.0, step=0.1, format="%.2f", key="bl_base_py")

        colA, colB = st.columns([1, 1])
        with colA:
            set_current = st.button("Set to Baseline", help="Initialize/overwrite the current line with these inputs.")
        with colB:
            reset_all = st.button("Set to Budget Changes", help="Clear the baseline trace so only the current line shows.")

    # ---- Sidebar: 2) Shift controls ----
    with st.sidebar.expander("2) Budget Changes", expanded=False):
        shift_type = st.selectbox("What changes?",
                                  options=["Income (M)", "Price of X (pₓ)", "Price of Y (pᵧ)"],
                                  index=0)
        mode = st.radio("Change type", options=["Percent", "Absolute"], horizontal=True, index=0)
        delta = st.number_input("Change amount", value=10.0, step=1.0, format="%.2f",
                                help="If Percent, 10 means +10%. If Absolute, 10 adds 10 units to M or price.")

        follow = st.checkbox("Follow Mode", value=True,
                             help="Keeps a ghost of the last line so you can compare step-by-step.")

        apply_btn = st.button("SEND")

    # ---- Sidebar: 3) Plot ranges ----
    with st.sidebar.expander("3) Graphing Range", expanded=False):
        xmax = st.number_input("Max X-axis", min_value=10.0, value=40.0, step=5.0, format="%.0f")
        ymax = st.number_input("Max Y-axis", min_value=10.0, value=40.0, step=5.0, format="%.0f")

    # ---- Session state bootstrapping ----
    if "bl_current" not in st.session_state:
        st.session_state.bl_current = {"M": base_M, "px": base_px, "py": base_py}
    if "bl_baseline" not in st.session_state:
        st.session_state.bl_baseline = None  # will hold previous line when follow-mode is on

    # ---- Button: set current from baseline inputs ----
    if set_current:
        st.session_state.bl_current = {"M": base_M, "px": base_px, "py": base_py}
        st.session_state.bl_baseline = None  # fresh start

    # ---- Button: reset baseline only ----
    if reset_all:
        st.session_state.bl_baseline = None

    # ---- Apply shift ----
    if apply_btn:
        # 1) If follow-mode, store the old current as the new baseline
        if follow:
            st.session_state.bl_baseline = copy.deepcopy(st.session_state.bl_current)

        # 2) Decide which key to shift
        key_map = {"Income (M)": "M", "Price of X (pₓ)": "px", "Price of Y (pᵧ)": "py"}
        key = key_map[shift_type]
        mode_key = "percent" if mode == "Percent" else "absolute"

        # 3) Apply to CURRENT
        st.session_state.bl_current = apply_shift(st.session_state.bl_current, key, mode_key, delta)

    # ---- Compute intercepts and slope for plotting + caption ----
    cur = st.session_state.bl_current
    cur_xi, cur_yi = intercepts(cur["M"], cur["px"], cur["py"])
    cur_slope = slope(cur["px"], cur["py"])

    # If we have a baseline, compute it too
    bl_xi = bl_yi = bl_slope = None
    if st.session_state.bl_baseline is not None:
        bl = st.session_state.bl_baseline
        bl_xi, bl_yi = intercepts(bl["M"], bl["px"], bl["py"])
        bl_slope = slope(bl["px"], bl["py"])

    # ---- Build plot ----
    fig = go.Figure()

    # Baseline (dashed, muted)
    if bl_xi is not None:
        fig.add_trace(go.Scatter(
            x=[0, bl_xi], y=[bl_yi, 0],
            mode="lines",
            name="Baseline (previous)",
            line=dict(width=2, dash="dash"),
            hovertemplate="x: %{x:.2f}<br>y: %{y:.2f}<extra>Baseline</extra>"
        ))

    # Current (solid, emphasized)
    fig.add_trace(go.Scatter(
        x=[0, cur_xi], y=[cur_yi, 0],
        mode="lines",
        name="Current",
        line=dict(width=3),
        hovertemplate="x: %{x:.2f}<br>y: %{y:.2f}<extra>Current</extra>"
    ))

    # Dynamic axes so both lines fit nicely
    x_max_auto = max(xmax, cur_xi, bl_xi or 0)
    y_max_auto = max(ymax, cur_yi, bl_yi or 0)

    fig.update_xaxes(range=[0, x_max_auto], title="Good X (units)")
    fig.update_yaxes(range=[0, y_max_auto], title="Good Y (units)")
    fig.update_layout(
        height=520,
        margin=dict(l=10, r=10, t=10, b=10),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1.0)
    )

    st.plotly_chart(fig, use_container_width=True, key="budget_line_chart")

    # ---- Text panel with math details ----
    with st.expander("Show details & equations", expanded=False):
        st.markdown(
            f"""
**Current line**:  M = pₓ·x + pᵧ·y  
Intercepts → x-int = {cur_xi:.2f},  y-int = {cur_yi:.2f}  
Slope → dy/dx = −pₓ/pᵧ = {cur_slope:.3f}
"""
        )
        if bl_xi is not None:
            st.markdown(
                f"""
**Baseline (previous)**:  
Intercepts → x-int = {bl_xi:.2f},  y-int = {bl_yi:.2f}  
Slope → dy/dx = {bl_slope:.3f}
"""
            )
        st.latex(r"\text{Budget line: } M = p_x x + p_y y \quad \Rightarrow \quad y = \frac{M}{p_y} - \frac{p_x}{p_y} x")

if __name__ == "__main__":
    app()