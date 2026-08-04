import numpy as np
import plotly.graph_objects as go
import streamlit as st

from apps.common import apply_grid


def app():
    st.subheader("Optimal Consumer Choice")

    income = st.sidebar.slider("Income", 1.0, 300.0, 100.0, 1.0)
    px = st.sidebar.slider("Price of X", 0.5, 20.0, 2.0, 0.5)
    py = st.sidebar.slider("Price of Y", 0.5, 20.0, 2.0, 0.5)
    alpha = st.sidebar.slider("Preference for X", 0.10, 0.90, 0.50, 0.05)

    x_star = alpha * income / px
    y_star = (1 - alpha) * income / py
    u_star = (x_star ** alpha) * (y_star ** (1 - alpha))
    x_int = income / px
    y_int = income / py
    xmax = max(x_int * 1.1, x_star * 1.4, 10)
    ymax = max(y_int * 1.1, y_star * 1.4, 10)

    x_vals = np.linspace(0.1, xmax, 300)
    y_indiff = (u_star / (x_vals ** alpha)) ** (1 / (1 - alpha))
    visible = y_indiff <= ymax

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=[0, x_int], y=[y_int, 0], mode="lines", name="Budget line", line=dict(width=3, color="#6C7A61")))
    fig.add_trace(go.Scatter(x=x_vals[visible], y=y_indiff[visible], mode="lines", name="Best affordable indifference curve", line=dict(width=3, color="#1d511e")))
    fig.add_trace(go.Scatter(x=[x_star], y=[y_star], mode="markers+text", name="Optimum", text=["Optimum"], textposition="top center", marker=dict(size=12, color="#B38210")))
    fig.update_xaxes(range=[0, xmax], title="Good X")
    fig.update_yaxes(range=[0, ymax], title="Good Y")
    fig.update_layout(height=540, legend=dict(orientation="h", y=1.04, x=0), margin=dict(l=40, r=20, t=20, b=40))
    apply_grid(fig)
    st.plotly_chart(fig, use_container_width=True, key="optimal_choice_chart")

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("X*", f"{x_star:.2f}")
    c2.metric("Y*", f"{y_star:.2f}")
    c3.metric("Utility", f"{u_star:.2f}")
    c4.metric("MRS at optimum", f"{px / py:.2f}")

    if st.toggle("Full analysis", value=False, key="optimal_choice_analysis"):
        st.markdown("With Cobb-Douglas preferences, the consumer spends share alpha of income on X and share 1-alpha on Y. At the interior optimum, the indifference curve is tangent to the budget line.")
        st.latex(r"X^*=\alpha\frac{M}{P_X},\quad Y^*=(1-\alpha)\frac{M}{P_Y}")
        st.latex(r"MRS_{XY}=\frac{P_X}{P_Y}")
