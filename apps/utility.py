import numpy as np
import plotly.graph_objects as go
import streamlit as st

from apps.common import apply_grid


def utility(x, y, alpha):
    return (x ** alpha) * (y ** (1 - alpha))


def app():
    st.subheader("Utility and Indifference Curves")

    alpha = st.sidebar.slider("Preference for X", 0.10, 0.90, 0.50, 0.05)
    x0 = st.sidebar.slider("Bundle X", 1.0, 100.0, 30.0, 1.0)
    y0 = st.sidebar.slider("Bundle Y", 1.0, 100.0, 30.0, 1.0)
    xmax = st.sidebar.number_input("Max X", 20, 300, 100, 10)
    ymax = st.sidebar.number_input("Max Y", 20, 300, 100, 10)

    u0 = utility(x0, y0, alpha)
    x_vals = np.linspace(1, xmax, 300)
    y_curve = (u0 / (x_vals ** alpha)) ** (1 / (1 - alpha))

    fig = go.Figure()
    for scale in [0.7, 1.0, 1.3]:
        u = u0 * scale
        y_vals = (u / (x_vals ** alpha)) ** (1 / (1 - alpha))
        visible = y_vals <= ymax
        fig.add_trace(go.Scatter(x=x_vals[visible], y=y_vals[visible], mode="lines", name=f"U={u:.1f}", line=dict(width=3 if scale == 1 else 2, dash=None if scale == 1 else "dash")))
    fig.add_trace(go.Scatter(x=[x0], y=[y0], mode="markers+text", name="Chosen bundle", text=[f"U={u0:.1f}"], textposition="top center", marker=dict(size=12, color="#B38210")))
    fig.update_xaxes(range=[0, xmax], title="Good X")
    fig.update_yaxes(range=[0, ymax], title="Good Y")
    fig.update_layout(height=540, legend=dict(orientation="h", y=1.04, x=0), margin=dict(l=40, r=20, t=20, b=40))
    apply_grid(fig)
    st.plotly_chart(fig, use_container_width=True, key="utility_chart")

    c1, c2, c3 = st.columns(3)
    c1.metric("Utility", f"{u0:.2f}")
    c2.metric("MRS", f"{(alpha / (1 - alpha)) * (y0 / x0):.2f}")
    c3.metric("Preference alpha", f"{alpha:.2f}")

    if st.toggle("Full analysis", value=False, key="utility_analysis"):
        st.latex(r"U=X^\alpha Y^{1-\alpha}")
        st.latex(r"MRS_{XY}=\frac{\alpha}{1-\alpha}\frac{Y}{X}")
        st.markdown("Higher indifference curves represent higher utility. The MRS is the amount of Y the consumer is willing to give up for one more unit of X at the current bundle.")
