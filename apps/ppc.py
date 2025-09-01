import numpy as np
import streamlit as st
import plotly.graph_objects as go

def app():
    st.subheader("Production Possibilities Curve (PPC)")

    # --- Sidebar controls ---
    with st.sidebar.expander("Frontier Settings", True):
        x_max = st.number_input("Max output of Good X (intercept a)", 10.0, 10_000.0, 100.0, 5.0)
        y_max = st.number_input("Max output of Good Y (intercept b)", 10.0, 10_000.0, 100.0, 5.0)
        k = st.slider("Curvature (k)", 1.0, 6.0, 2.5, 0.1)  # k=1 linear; k>1 bowed out
        shift_pct = st.slider("Tech/Labor shift (%)", -50, 200, 0, 5)
        show_baseline = st.checkbox("Show baseline frontier", value=True)

    a = x_max
    b = y_max
    a_shift = a * (1 + shift_pct/100.0)
    b_shift = b * (1 + shift_pct/100.0)

    # superellipse frontier:  (x/a)^k + (y/b)^k = 1  ->  y(x) = b * (1 - (x/a)^k)^(1/k)
    def y_on_ppf(x, A, B, K):
        x = np.clip(x, 0, A)
        val = np.maximum(0.0, 1.0 - (x/A)**K)
        return B * (val ** (1.0/K))

    xs = np.linspace(0, a_shift, 400)
    ys_shift = y_on_ppf(xs, a_shift, b_shift, k)
    ys_base = y_on_ppf(np.linspace(0, a, 400), a, b, k)

    # pick a point on the shifted PPF to read opportunity cost
    qx = st.slider("Choose a production level of X to analyze", 0.0, float(a_shift), float(a_shift*0.4), step=0.5)
    # numeric derivative for OC at qx (dy/dx)
    h = max(1e-6, 0.001 * a_shift)
    y1 = y_on_ppf(qx, a_shift, b_shift, k)
    y2 = y_on_ppf(min(a_shift, qx + h), a_shift, b_shift, k)
    dydx = (y2 - y1) / h  # < 0 on bowed-out frontier
    oc_x = -dydx  # units of Y per +1 X

    fig = go.Figure()
    if show_baseline:
        xsb = np.linspace(0, a, 400)
        fig.add_trace(go.Scatter(x=xsb, y=ys_base, mode="lines", name="PPF (baseline)", line=dict(dash="dash")))
    fig.add_trace(go.Scatter(x=xs, y=ys_shift, mode="lines", name="PPF"))
    fig.add_trace(go.Scatter(x=[qx], y=[y1], mode="markers+text", text=["•"], textposition="top center", name="Point"))

    fig.update_layout(
        xaxis_title="Good X (quantity)", yaxis_title="Good Y (quantity)",
        xaxis=dict(range=[0, max(a, a_shift)], zeroline=False),
        yaxis=dict(range=[0, max(b, b_shift)], zeroline=False),
        height=520, margin=dict(l=40, r=20, t=20, b=40)
    )
    st.plotly_chart(fig, use_container_width=True,key="ppc_chart")
    st.caption(f"At X = {qx:.2f}, Y = {y1:.2f}.  Opportunity cost of 1 more X ≈ {oc_x:.3f} Y (rising as X increases when k>1).")
    show_adv = st.toggle("Advanced (show equations)", key="ppc_adv2")
    if show_adv:
        st.latex(r" \text{PPC}_A: \; y = a_y - \frac{a_y}{a_x} x \quad;\quad \text{PPC}_B: \; y = b_y - \frac{b_y}{b_x} x ")
        st.latex(r" \text{OC}_X^A = \frac{a_y}{a_x}, \quad \text{OC}_X^B = \frac{b_y}{b_x} \;\;\Rightarrow\;\; \text{CA in X} = \arg\min \text{OC}_X ")