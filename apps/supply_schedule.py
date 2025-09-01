import streamlit as st
import pandas as pd
from apps.common import Line, base_fig, add_line

def app():
    st.subheader("Build the Supply Curve")

    colA, colB = st.columns([1,2])

    with colA:
        st.caption("Enter Data:")
        df = st.data_editor(
            pd.DataFrame({"Q":[10,30,50], "P":[8,15,24]}),
            num_rows="dynamic",
            use_container_width=True,
            key="sup_sched",
        )
        st.caption("Adjust Scale:")
        xmax = st.number_input("Max Q", 10, 1000, 100, 10)
        ymax = st.number_input("Max P", 10, 1000, 50, 5)

    # Fit P = a + bQ from the table
    if len(df) >= 2:
        Q = df["Q"].astype(float).values
        P = df["P"].astype(float).values
        b = ((Q - Q.mean())*(P - P.mean())).sum() / max(((Q - Q.mean())**2).sum(), 1e-9)
        a = P.mean() - b*Q.mean()
        S = Line(a=float(a), b=float(b))
    else:
        S = Line(a=5.0, b=0.1)

    with colB:
        fig = base_fig(xmax=xmax, ymax=ymax)
        add_line(fig, S, "Supply (fit)")
        st.plotly_chart(fig, use_container_width=True,key="sup_chart")
        st.caption(f"Estimated: **P = {S.a:.2f} + ({S.b:.3f})Q**  (β should be positive)")

    # --- Send fitted coefficients to Static Equilibrium ---
    if st.button("Send Supply Curve to Market Model", type="primary", use_container_width=True):
        st.session_state["alpha_s"] = float(S.a)
        st.session_state["beta_s"]  = float(S.b)
        st.session_state["nav_default"] = "Static Equilibrium"
        st.success("Supply coefficients sent. Opening Static Equilibrium…")
        st.rerun()