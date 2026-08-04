import math

import numpy as np
import plotly.graph_objects as go
import streamlit as st

from apps.common import apply_grid


FACTOR_COLOR = "#6C7A61"
MRP_COLOR = "#1d511e"
MFC_COLOR = "#C49A6C"
POINT_COLOR = "#B38210"


def cobb_douglas_output(a, land, labor, capital, al, be, ga):
    return a * (land ** al) * (labor ** be) * (capital ** ga)


def marginal_product(output, factor_qty, exponent):
    return exponent * output / max(factor_qty, 1e-9)


def demand_wage(intercept, slope, q):
    return intercept - slope * q


def supply_wage(intercept, slope, q):
    return intercept + slope * q


def factor_equilibrium(d_intercept, d_slope, s_intercept, s_slope):
    den = d_slope + s_slope
    if den <= 0:
        return float("nan"), float("nan")
    q = (d_intercept - s_intercept) / den
    p = demand_wage(d_intercept, d_slope, q)
    return q, p


def factor_market_chart(name, price_label, d_intercept, d_slope, s_intercept, s_slope, xmax, ymax):
    q_vals = np.linspace(0, xmax, 300)
    d_vals = demand_wage(d_intercept, d_slope, q_vals)
    s_vals = supply_wage(s_intercept, s_slope, q_vals)
    q_eq, p_eq = factor_equilibrium(d_intercept, d_slope, s_intercept, s_slope)

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=q_vals[d_vals >= 0], y=d_vals[d_vals >= 0], mode="lines", name=f"Demand for {name}", line=dict(width=3, color=MRP_COLOR)))
    fig.add_trace(go.Scatter(x=q_vals[s_vals <= ymax * 1.2], y=s_vals[s_vals <= ymax * 1.2], mode="lines", name=f"Supply of {name}", line=dict(width=3, color=MFC_COLOR)))
    if not math.isnan(q_eq):
        fig.add_trace(go.Scatter(x=[q_eq], y=[p_eq], mode="markers+text", name="Equilibrium", text=[f"Q={q_eq:.1f}, {price_label}={p_eq:.1f}"], textposition="top center", marker=dict(size=12, color=POINT_COLOR)))
        fig.add_shape(type="line", x0=q_eq, y0=0, x1=q_eq, y1=p_eq, line=dict(dash="dot", width=1))
        fig.add_shape(type="line", x0=0, y0=p_eq, x1=q_eq, y1=p_eq, line=dict(dash="dot", width=1))
    fig.update_xaxes(range=[0, xmax], title=f"Quantity of {name}")
    fig.update_yaxes(range=[0, ymax], title=price_label)
    fig.update_layout(height=540, legend=dict(orientation="h", y=1.02, x=0), margin=dict(l=40, r=20, t=20, b=40))
    apply_grid(fig)
    return fig, q_eq, p_eq


def independent_factor_app(name, price_label, default_supply, default_productivity, default_other_factor):
    st.subheader(f"{name} Market")
    xmax = st.sidebar.number_input("Max quantity", 20, 1000, 120, 10, key=f"{name}_xmax")
    ymax = st.sidebar.number_input(f"Max {price_label}", 20, 1000, 120, 10, key=f"{name}_ymax")
    output_price = st.sidebar.slider("Output price", 1.0, 20.0, 6.0, 0.5, key=f"{name}_out_price")
    productivity = st.sidebar.slider("Factor productivity", 0.10, 5.00, default_productivity, 0.05, key=f"{name}_prod")
    other_factor = st.sidebar.slider("Other complementary inputs", 1.0, 200.0, default_other_factor, 1.0, key=f"{name}_other")
    supply_intercept = st.sidebar.slider("Supply intercept", 0.0, float(ymax), default_supply, 1.0, key=f"{name}_s_int")
    supply_slope = st.sidebar.slider("Supply slope", 0.05, 2.0, 0.35, 0.05, key=f"{name}_s_slope")

    demand_intercept = output_price * productivity * math.sqrt(other_factor)
    demand_slope = max(demand_intercept / (xmax * 1.25), 0.05)
    fig, q_eq, p_eq = factor_market_chart(name, price_label, demand_intercept, demand_slope, supply_intercept, supply_slope, xmax, ymax)
    st.plotly_chart(fig, use_container_width=True, key=f"{name}_chart")

    c1, c2, c3 = st.columns(3)
    c1.metric("Equilibrium quantity", f"{q_eq:.2f}")
    c2.metric(price_label, f"{p_eq:.2f}")
    c3.metric("Demand intercept", f"{demand_intercept:.2f}")

    if st.toggle("Full analysis", value=False, key=f"{name}_analysis"):
        st.markdown(
            f"""
Demand for {name.lower()} is derived demand: firms demand the input because it helps produce output that can be sold. Raising output price, productivity, or complementary inputs shifts factor demand outward. The equilibrium {price_label.lower()} is where the factor demand curve intersects the supply curve.
"""
        )
        st.latex(r"\text{MRP}_F = P_{output}\times MP_F")
