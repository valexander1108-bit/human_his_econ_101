import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import streamlit as st

from apps.common import apply_grid
from apps.elasticity_common import (
    CURVE_COLOR,
    DEMAND_COLOR,
    POINT_COLOR,
    TR_COLOR,
    demand_price,
    elasticity_label,
    isoelastic_demand_price,
    isoelastic_demand_slope,
    linear_demand_elasticity,
)


def app():
    st.subheader("Elasticity and Total Revenue")

    xmax = st.sidebar.number_input("Max Q", 20, 1000, 120, 10, key="etr_xmax")
    ymax = st.sidebar.number_input("Max P", 20, 1000, 120, 10, key="etr_ymax")
    curved = st.sidebar.toggle(
        "Curved demand",
        value=False,
        help="Compare total revenue under linear demand or fixed isoelastic demand.",
        key="etr_curved",
    )

    st.sidebar.markdown("**Linear demand**")
    alpha = st.sidebar.number_input("Price intercept", min_value=1.0, value=100.0, step=5.0, key="etr_alpha")
    beta = st.sidebar.number_input(
        "Slope magnitude",
        min_value=0.05,
        value=1.0,
        step=0.05,
        format="%.2f",
        key="etr_beta",
    )

    q_min = max(0.01, xmax * 0.01)
    q_values = np.linspace(q_min, xmax, 500)

    if curved:
        st.sidebar.markdown("**Curved demand**")
        anchor_q = st.sidebar.slider("Curve anchor Q", 1.0, float(xmax), min(50.0, float(xmax)), 1.0)
        anchor_p = st.sidebar.slider("Curve anchor P", 1.0, float(ymax), min(50.0, float(ymax)), 1.0)
        curve_elasticity = st.sidebar.slider("Curve elasticity", 0.20, 5.00, 1.00, 0.05)
        q0 = st.sidebar.slider("Highlighted Q", 1.0, float(xmax), min(anchor_q, float(xmax)), 1.0)
        prices = isoelastic_demand_price(anchor_q, anchor_p, curve_elasticity, q_values)
        p0 = float(isoelastic_demand_price(anchor_q, anchor_p, curve_elasticity, q0))
        point_elasticity = curve_elasticity
        slope_at_point = float(isoelastic_demand_slope(anchor_q, anchor_p, curve_elasticity, q0))
        curve_name = "Fixed curved demand"
    else:
        max_linear_q = max(alpha / beta, 1.0)
        q0 = st.sidebar.slider("Highlighted Q", 1.0, float(min(xmax, max_linear_q)), min(50.0, float(min(xmax, max_linear_q))), 1.0)
        prices = demand_price(alpha, beta, q_values)
        p0 = float(demand_price(alpha, beta, q0))
        point_elasticity = linear_demand_elasticity(alpha, beta, q0)
        slope_at_point = -beta
        curve_name = "Linear demand"

    visible = (prices >= 0) & (prices <= ymax * 1.3)
    tr_values = q_values * prices
    tr0 = q0 * p0
    tr_ymax = max(float(np.nanmax(tr_values[visible])) * 1.12 if visible.any() else tr0 * 1.2, tr0 * 1.2, 1.0)

    fig = make_subplots(
        rows=1,
        cols=2,
        subplot_titles=("Demand", "Total revenue"),
        horizontal_spacing=0.12,
    )
    fig.add_trace(
        go.Scatter(
            x=q_values[visible],
            y=prices[visible],
            mode="lines",
            name=curve_name,
            line=dict(width=4 if curved else 3, color=CURVE_COLOR if curved else DEMAND_COLOR),
            hovertemplate="Q=%{x:.2f}<br>P=%{y:.2f}<extra></extra>",
        ),
        row=1,
        col=1,
    )
    fig.add_trace(
        go.Scatter(
            x=[0, q0, q0, 0, 0],
            y=[0, 0, p0, p0, 0],
            mode="lines",
            fill="toself",
            name="Revenue rectangle",
            fillcolor="rgba(51, 101, 138, 0.18)",
            line=dict(width=1, color=TR_COLOR),
            hoverinfo="skip",
        ),
        row=1,
        col=1,
    )
    fig.add_trace(
        go.Scatter(
            x=[q0],
            y=[p0],
            mode="markers+text",
            name="Demand point",
            text=[f"E={point_elasticity:.2f}"],
            textposition="top center",
            marker=dict(size=12, color=POINT_COLOR, line=dict(width=1, color="white")),
            hovertemplate="Q=%{x:.2f}<br>P=%{y:.2f}<extra></extra>",
        ),
        row=1,
        col=1,
    )
    fig.add_trace(
        go.Scatter(
            x=q_values[visible],
            y=tr_values[visible],
            mode="lines",
            name="TR = P x Q",
            line=dict(width=4, color=TR_COLOR),
            hovertemplate="Q=%{x:.2f}<br>TR=%{y:.2f}<extra></extra>",
        ),
        row=1,
        col=2,
    )
    fig.add_trace(
        go.Scatter(
            x=[q0],
            y=[tr0],
            mode="markers+text",
            name="Current TR",
            text=[f"TR={tr0:.0f}"],
            textposition="top center",
            marker=dict(size=12, color=POINT_COLOR, line=dict(width=1, color="white")),
            hovertemplate="Q=%{x:.2f}<br>TR=%{y:.2f}<extra></extra>",
        ),
        row=1,
        col=2,
    )

    fig.update_xaxes(range=[0, xmax], title_text="Quantity (Q)", row=1, col=1)
    fig.update_yaxes(range=[0, ymax], title_text="Price (P)", row=1, col=1)
    fig.update_xaxes(range=[0, xmax], title_text="Quantity (Q)", row=1, col=2)
    fig.update_yaxes(range=[0, tr_ymax], title_text="Total revenue", row=1, col=2)
    fig.update_layout(height=560, plot_bgcolor="white", paper_bgcolor="white", legend=dict(orientation="h", y=1.12, x=0))
    apply_grid(fig)

    st.plotly_chart(fig, use_container_width=True, key="elasticity_tr_chart")

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Price", f"{p0:.2f}")
    c2.metric("Quantity", f"{q0:.2f}")
    c3.metric("Total revenue", f"{tr0:.2f}")
    c4.metric("Elasticity", f"{point_elasticity:.2f}", elasticity_label(point_elasticity))

    rows = []
    for q in [max(q0 - 10, q_min), q0, min(q0 + 10, xmax)]:
        if curved:
            p = float(isoelastic_demand_price(anchor_q, anchor_p, curve_elasticity, q))
            elasticity = curve_elasticity
            slope = float(isoelastic_demand_slope(anchor_q, anchor_p, curve_elasticity, q))
        else:
            p = float(demand_price(alpha, beta, q))
            if p <= 0:
                continue
            elasticity = linear_demand_elasticity(alpha, beta, q)
            slope = -beta
        rows.append(
            {
                "Q": round(float(q), 2),
                "P": round(float(p), 2),
                "TR": round(float(q * p), 2),
                "slope dP/dQ": round(float(slope), 3),
                "elasticity": round(float(elasticity), 3),
            }
        )
    st.dataframe(pd.DataFrame(rows), hide_index=True, use_container_width=True)

    show_math = st.toggle("Advanced (show equations)", value=False, key="elasticity_tr_adv")
    if show_math:
        st.latex(r"TR = P \times Q")
        st.caption("For linear demand, total revenue rises until unit elasticity and then falls. For isoelastic demand, revenue follows the fixed elasticity setting.")
