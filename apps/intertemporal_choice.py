import numpy as np
import plotly.graph_objects as go
import streamlit as st

from apps.common import apply_grid


def app():
    st.subheader("Intertemporal Choice")

    y_now = st.sidebar.slider("Income today", 0.0, 500.0, 120.0, 5.0)
    y_future = st.sidebar.slider("Income next period", 0.0, 500.0, 160.0, 5.0)
    r = st.sidebar.slider("Interest rate", -0.50, 1.00, 0.10, 0.01)
    alpha = st.sidebar.slider("Preference for consumption today", 0.10, 0.90, 0.50, 0.05)

    present_value = y_now + y_future / (1 + r)
    c_now = alpha * present_value
    c_future = (1 - alpha) * present_value * (1 + r)
    saving = y_now - c_now
    future_from_budget = (1 + r) * (present_value - c_now)
    u = (c_now ** alpha) * (c_future ** (1 - alpha)) if c_now > 0 and c_future > 0 else 0

    x_int = present_value
    y_int = present_value * (1 + r)
    xmax = max(x_int * 1.1, 10)
    ymax = max(y_int * 1.1, 10)
    c_vals = np.linspace(0.1, xmax, 300)
    indiff = (u / (c_vals ** alpha)) ** (1 / (1 - alpha)) if u > 0 else np.zeros_like(c_vals)
    visible = indiff <= ymax

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=[0, x_int], y=[y_int, 0], mode="lines", name="Intertemporal budget", line=dict(width=3, color="#6C7A61")))
    if u > 0:
        fig.add_trace(go.Scatter(x=c_vals[visible], y=indiff[visible], mode="lines", name="Best indifference curve", line=dict(width=3, color="#1d511e")))
    fig.add_trace(go.Scatter(x=[y_now], y=[y_future], mode="markers+text", name="Endowment", text=["Endowment"], textposition="top center", marker=dict(size=11, color="#C49A6C")))
    fig.add_trace(go.Scatter(x=[c_now], y=[c_future], mode="markers+text", name="Choice", text=["Choice"], textposition="top center", marker=dict(size=12, color="#B38210")))
    fig.update_xaxes(range=[0, xmax], title="Consumption today")
    fig.update_yaxes(range=[0, ymax], title="Consumption next period")
    fig.update_layout(height=540, legend=dict(orientation="h", y=1.04, x=0), margin=dict(l=40, r=20, t=20, b=40))
    apply_grid(fig)
    st.plotly_chart(fig, use_container_width=True, key="intertemporal_choice_chart")

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("C today", f"{c_now:.2f}")
    c2.metric("C next period", f"{future_from_budget:.2f}")
    c3.metric("Saving", f"{saving:.2f}", "borrower" if saving < 0 else "saver")
    c4.metric("PV resources", f"{present_value:.2f}")

    if st.toggle("Full analysis", value=False, key="intertemporal_analysis"):
        st.markdown("The consumer can shift resources across time by saving or borrowing. The interest rate rotates the intertemporal budget line around the endowment in present-value terms and changes the relative price of consuming today.")
        st.latex(r"C_1+\frac{C_2}{1+r}=Y_1+\frac{Y_2}{1+r}")
        st.latex(r"C_1^*=\alpha PV,\quad C_2^*=(1-\alpha)(1+r)PV")
