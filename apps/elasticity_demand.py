import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from apps.common import apply_grid, base_fig
from apps.elasticity_common import (
    CURVE_COLOR,
    DEMAND_COLOR,
    POINT_COLOR,
    add_guides,
    add_tangent,
    demand_price,
    elasticity_label,
    isoelastic_demand_price,
    isoelastic_demand_slope,
    linear_demand_elasticity,
)


def app():
    st.subheader("Price Elasticity of Demand")

    xmax = st.sidebar.number_input("Max Q", 20, 1000, 120, 10, key="ed_xmax")
    ymax = st.sidebar.number_input("Max P", 20, 1000, 120, 10, key="ed_ymax")
    curved = st.sidebar.toggle(
        "Curved demand",
        value=False,
        help="Off: linear demand has constant slope. On: fixed curved demand has constant elasticity.",
        key="ed_curved",
    )

    st.sidebar.markdown("**Linear demand**")
    alpha = st.sidebar.number_input("Price intercept", min_value=1.0, value=100.0, step=5.0, key="ed_alpha")
    beta = st.sidebar.number_input(
        "Slope magnitude",
        min_value=0.05,
        value=1.0,
        step=0.05,
        format="%.2f",
        help="The linear curve is P = intercept - slope magnitude * Q.",
        key="ed_beta",
    )

    max_linear_q = max(alpha / beta, 1.0)
    if curved:
        st.sidebar.markdown("**Curved demand**")
        anchor_q = st.sidebar.slider("Curve anchor Q", 1.0, float(xmax), min(50.0, float(xmax)), 1.0)
        anchor_p = st.sidebar.slider("Curve anchor P", 1.0, float(ymax), min(50.0, float(ymax)), 1.0)
        curve_elasticity = st.sidebar.slider("Curve elasticity", 0.20, 5.00, 1.00, 0.05)
        q0 = st.sidebar.slider("Highlighted Q", 1.0, float(xmax), min(anchor_q, float(xmax)), 1.0)
        p0 = float(isoelastic_demand_price(anchor_q, anchor_p, curve_elasticity, q0))
        point_elasticity = curve_elasticity
        slope_at_point = float(isoelastic_demand_slope(anchor_q, anchor_p, curve_elasticity, q0))
    else:
        target_elasticity = st.sidebar.slider("Elasticity at highlighted point", 0.20, 5.00, 1.00, 0.05)
        q0 = alpha / (beta * (target_elasticity + 1.0))
        p0 = demand_price(alpha, beta, q0)
        point_elasticity = target_elasticity
        slope_at_point = -beta

    q_min = max(0.01, xmax * 0.01)
    q_values = np.linspace(q_min, xmax, 400)
    linear_p = demand_price(alpha, beta, q_values)
    visible_linear = linear_p >= 0

    fig = base_fig(xmax=xmax, ymax=ymax)
    fig.update_layout(height=560, legend=dict(orientation="h", yanchor="bottom", y=1.02, x=0))
    fig.update_xaxes(range=[0, xmax], title="Quantity (Q)")
    fig.update_yaxes(range=[0, ymax], title="Price (P)")
    apply_grid(fig)

    fig.add_trace(
        go.Scatter(
            x=q_values[visible_linear],
            y=linear_p[visible_linear],
            mode="lines",
            name="Linear demand",
            line=dict(width=3, color=DEMAND_COLOR, dash="dash" if curved else None),
            hovertemplate="Q=%{x:.2f}<br>P=%{y:.2f}<extra></extra>",
        )
    )

    if curved:
        curved_p = isoelastic_demand_price(anchor_q, anchor_p, curve_elasticity, q_values)
        visible_curve = (curved_p >= 0) & (curved_p <= ymax * 1.3)
        fig.add_trace(
            go.Scatter(
                x=q_values[visible_curve],
                y=curved_p[visible_curve],
                mode="lines",
                name="Fixed curved demand",
                line=dict(width=4, color=CURVE_COLOR),
                hovertemplate="Q=%{x:.2f}<br>P=%{y:.2f}<extra></extra>",
            )
        )

    fig.add_trace(
        go.Scatter(
            x=[q0],
            y=[p0],
            mode="markers+text",
            name="Highlighted point",
            text=[f"E={point_elasticity:.2f}"],
            textposition="top center",
            marker=dict(size=12, color=POINT_COLOR, line=dict(width=1, color="white")),
            hovertemplate="Q=%{x:.2f}<br>P=%{y:.2f}<extra></extra>",
        )
    )
    add_tangent(fig, q0, p0, slope_at_point, xmax, "Tangent slope" if curved else "Slope segment")
    add_guides(fig, q0, p0)

    left, right = st.columns([2, 1])
    with left:
        st.plotly_chart(fig, use_container_width=True, key="elasticity_demand_chart")

    with right:
        mode_name = "Fixed curved demand" if curved else "Linear demand"
        st.markdown(f"**Mode:** {mode_name}")
        st.metric("Point elasticity", f"{point_elasticity:.2f}", elasticity_label(point_elasticity))
        st.metric("Slope at point", f"{slope_at_point:.3f}")
        st.metric("Point price", f"{p0:.2f}")
        st.metric("Point quantity", f"{q0:.2f}")

    if curved:
        sample_qs = np.array([max(q0 * 0.60, q_min), q0, min(q0 * 1.40, xmax)])
    else:
        sample_qs = np.array([max(q0 * 0.60, q_min), q0, min(q0 * 1.40, max_linear_q * 0.98, xmax)])

    rows = []
    for q in sample_qs:
        if curved:
            p = float(isoelastic_demand_price(anchor_q, anchor_p, curve_elasticity, q))
            slope = float(isoelastic_demand_slope(anchor_q, anchor_p, curve_elasticity, q))
            elasticity = curve_elasticity
        else:
            p = float(demand_price(alpha, beta, q))
            if p <= 0:
                continue
            slope = -beta
            elasticity = linear_demand_elasticity(alpha, beta, q)
        rows.append(
            {
                "Q": round(float(q), 2),
                "P": round(float(p), 2),
                "slope dP/dQ": round(float(slope), 3),
                "elasticity": round(float(elasticity), 3),
            }
        )

    st.dataframe(pd.DataFrame(rows), hide_index=True, use_container_width=True)

    show_math = st.toggle("Advanced (show equations)", value=False, key="elasticity_demand_adv")
    if show_math:
        if curved:
            st.latex(r"P = P_0\left(\frac{Q}{Q_0}\right)^{-1/E}")
            st.caption("The curved demand curve is fixed by its anchor and elasticity. Moving along it changes slope, not elasticity.")
        else:
            st.latex(r"P = \alpha - \beta Q")
            st.latex(r"|E_d| = \frac{P}{\beta Q}")
            st.caption("Linear demand keeps the same slope at every point, but elasticity changes along the curve.")
