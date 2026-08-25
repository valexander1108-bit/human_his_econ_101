import streamlit as st
import pandas as pd
from apps.common import Line, base_fig, add_line

def app(scenario=None, **params):
    st.subheader("Build the Demand Curve")
    params = {**st.session_state.get("selected_model_params", {}), **params}
    if params.get("worksheet_note"):
        st.info(params["worksheet_note"])

    colA, colB = st.columns([1,2])

    with colA:
        st.caption("Enter Data:")
        default_df = pd.DataFrame(params.get("schedule", [{"Q": 10, "P": 28}, {"Q": 30, "P": 20}, {"Q": 50, "P": 12}]))
        df = st.data_editor(
            default_df,
            num_rows="dynamic",
            use_container_width=True,
            key="dem_sched",
        )
        st.caption("Adjust Scale:")
        xmax = st.number_input("Max Q", 10, 1000, int(params.get("xmax", 100)), 10)
        ymax = st.number_input("Max P", 10, 1000, int(params.get("ymax", 50)), 5)

    # Fit P = a + bQ from the table
    if len(df) >= 2:
        Q = df["Q"].astype(float).values
        P = df["P"].astype(float).values
        b = ((Q - Q.mean())*(P - P.mean())).sum() / max(((Q - Q.mean())**2).sum(), 1e-9)
        a = P.mean() - b*Q.mean()
        D = Line(a=float(a), b=float(b))
    else:
        D = Line(a=30.0, b=-0.2)

    with colB:
        fig = base_fig(xmax=xmax, ymax=ymax)
        add_line(fig, D, "Demand (fit)")
        st.plotly_chart(fig, use_container_width=True, key="dem_chart")
        st.caption(f"Estimated: **P = {D.a:.2f} + ({D.b:.3f})Q**  (β should be negative)")

    # --- Send fitted coefficients to Static Equilibrium ---
    if st.button("Send Demand Curve to Market Model", type="primary", use_container_width=True):
        st.session_state["alpha_d"] = float(D.a)
        st.session_state["beta_d"]  = float(D.b)
        st.session_state["nav_default"] = "Static Equilibrium"
        st.success("Demand coefficients sent. Opening Static Equilibrium…")
        st.rerun()
