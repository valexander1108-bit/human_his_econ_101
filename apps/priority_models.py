import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from apps.common import apply_grid


GREEN = "#1d511e"
GOLD = "#C49A6C"
SAGE = "#6C7A61"
BLUE = "#33658A"
RED = "#B23F35"
POINT = "#B38210"


def finish(fig):
    fig.update_layout(
        height=540,
        margin=dict(l=40, r=20, t=30, b=40),
        legend=dict(orientation="h", y=1.08, x=0),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
    )
    apply_grid(fig)
    return fig


def public_goods_common_resources_app():
    st.subheader("Public Goods and Common Resources")

    model = st.sidebar.radio("Model", ["Public good", "Common resource"], horizontal=True)
    group_size = st.sidebar.slider("Group size", 2, 100, 25, 1)
    private_benefit = st.sidebar.slider("Private marginal benefit", 1.0, 30.0, 8.0, 0.5)
    spillover = st.sidebar.slider("Benefit or crowding externality", 0.0, 30.0, 10.0, 0.5)
    marginal_cost = st.sidebar.slider("Marginal cost", 1.0, 80.0, 30.0, 1.0)

    q = np.linspace(0, 100, 300)
    if model == "Public good":
        private_mb = np.maximum(private_benefit - 0.04 * q, 0)
        social_mb = private_mb + (group_size - 1) * spillover / group_size
        cost = np.full_like(q, marginal_cost)
        q_private = q[np.argmin(np.abs(private_mb - cost))]
        q_social = q[np.argmin(np.abs(social_mb - cost))]
        gap_label = "underprovided"
        title = "Vertical summation of benefits"
    else:
        private_mb = np.maximum(private_benefit + spillover - 0.10 * q, 0)
        social_mb = np.maximum(private_mb - spillover * (q / 60), 0)
        cost = np.full_like(q, marginal_cost * 0.45)
        q_private = q[np.argmin(np.abs(private_mb - cost))]
        q_social = q[np.argmin(np.abs(social_mb - cost))]
        gap_label = "overused"
        title = "Open access and crowding costs"

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=q, y=private_mb, name="Private marginal benefit", line=dict(width=3, color=GREEN)))
    fig.add_trace(go.Scatter(x=q, y=social_mb, name="Social marginal benefit", line=dict(width=3, color=BLUE, dash="dash")))
    fig.add_trace(go.Scatter(x=q, y=cost, name="Marginal cost", line=dict(width=3, color=GOLD)))
    fig.add_trace(go.Scatter(x=[q_private], y=[np.interp(q_private, q, cost)], mode="markers+text", text=["Private"], textposition="top center", marker=dict(size=12, color=POINT), name="Private outcome"))
    fig.add_trace(go.Scatter(x=[q_social], y=[np.interp(q_social, q, cost)], mode="markers+text", text=["Efficient"], textposition="top center", marker=dict(size=12, color=RED), name="Efficient outcome"))
    fig.update_xaxes(title="Quantity")
    fig.update_yaxes(title="Marginal value / cost")
    st.plotly_chart(finish(fig), use_container_width=True, key="public_common_chart")

    c1, c2, c3 = st.columns(3)
    c1.metric("Private Q", f"{q_private:.1f}")
    c2.metric("Efficient Q", f"{q_social:.1f}")
    c3.metric("Market failure", gap_label)
    st.caption(title)

    if st.toggle("Full analysis", value=False, key="public_common_analysis"):
        st.markdown(
            "Public goods are nonrival and nonexcludable, so private willingness to pay understates social value. Common resources are rival and hard to exclude, so individual use ignores crowding or depletion costs imposed on others."
        )


def income_substitution_app():
    st.subheader("Income and Substitution Effects")

    income = st.sidebar.slider("Income", 20.0, 400.0, 120.0, 5.0)
    px0 = st.sidebar.slider("Original price of X", 0.5, 20.0, 4.0, 0.5)
    px1 = st.sidebar.slider("New price of X", 0.5, 20.0, 2.0, 0.5)
    py = st.sidebar.slider("Price of Y", 0.5, 20.0, 3.0, 0.5)
    alpha = st.sidebar.slider("Preference for X", 0.10, 0.90, 0.50, 0.05)

    x0 = alpha * income / px0
    y0 = (1 - alpha) * income / py
    u0 = (x0 ** alpha) * (y0 ** (1 - alpha))
    x1 = alpha * income / px1
    y1 = (1 - alpha) * income / py
    compensated_income = u0 / ((alpha / px1) ** alpha * ((1 - alpha) / py) ** (1 - alpha))
    xc = alpha * compensated_income / px1
    yc = (1 - alpha) * compensated_income / py

    xmax = max(income / min(px0, px1), compensated_income / px1) * 1.15
    ymax = max(income / py, compensated_income / py) * 1.15
    x = np.linspace(0.1, xmax, 300)
    y_indiff = (u0 / (x ** alpha)) ** (1 / (1 - alpha))

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=[0, income / px0], y=[income / py, 0], name="Original budget", line=dict(width=3, color=SAGE)))
    fig.add_trace(go.Scatter(x=[0, income / px1], y=[income / py, 0], name="New budget", line=dict(width=3, color=GREEN)))
    fig.add_trace(go.Scatter(x=[0, compensated_income / px1], y=[compensated_income / py, 0], name="Compensated budget", line=dict(width=2, color=GOLD, dash="dash")))
    fig.add_trace(go.Scatter(x=x[y_indiff <= ymax], y=y_indiff[y_indiff <= ymax], name="Original utility", line=dict(width=2, color=BLUE)))
    for xx, yy, name, color in [(x0, y0, "A original", SAGE), (xc, yc, "B substitution", GOLD), (x1, y1, "C final", POINT)]:
        fig.add_trace(go.Scatter(x=[xx], y=[yy], mode="markers+text", text=[name], textposition="top center", marker=dict(size=12, color=color), name=name))
    fig.update_xaxes(title="Good X", range=[0, xmax])
    fig.update_yaxes(title="Good Y", range=[0, ymax])
    st.plotly_chart(finish(fig), use_container_width=True, key="income_substitution_chart")

    c1, c2, c3 = st.columns(3)
    c1.metric("Total effect on X", f"{x1 - x0:.2f}")
    c2.metric("Substitution effect", f"{xc - x0:.2f}")
    c3.metric("Income effect", f"{x1 - xc:.2f}")

    if st.toggle("Full analysis", value=False, key="income_substitution_analysis"):
        st.markdown(
            "The substitution effect moves along the original indifference curve after the relative price changes. The income effect moves from the compensated bundle to the final bundle because purchasing power has changed."
        )


def labor_policy_app():
    st.subheader("Labor Market Policy")

    policy = st.sidebar.selectbox("Policy", ["Minimum wage", "Payroll tax", "Wage subsidy"])
    demand_intercept = st.sidebar.slider("Labor demand intercept", 20.0, 150.0, 90.0, 5.0)
    demand_slope = st.sidebar.slider("Labor demand slope", 0.10, 2.00, 0.55, 0.05)
    supply_intercept = st.sidebar.slider("Labor supply intercept", 0.0, 80.0, 20.0, 2.0)
    supply_slope = st.sidebar.slider("Labor supply slope", 0.10, 2.00, 0.45, 0.05)
    wedge = st.sidebar.slider("Policy wedge", 0.0, 50.0, 12.0, 1.0)

    q = np.linspace(0, 120, 300)
    demand = demand_intercept - demand_slope * q
    supply = supply_intercept + supply_slope * q
    q_eq = (demand_intercept - supply_intercept) / (demand_slope + supply_slope)
    w_eq = demand_intercept - demand_slope * q_eq

    if policy == "Minimum wage":
        wage = max(w_eq, wedge + w_eq * 0.8)
        qd = max((demand_intercept - wage) / demand_slope, 0)
        qs = max((wage - supply_intercept) / supply_slope, 0)
        q_trade = min(qd, qs)
        worker_wage = firm_cost = wage
        label = f"unemployment = {max(qs - qd, 0):.1f}"
    elif policy == "Payroll tax":
        taxed_supply = supply + wedge
        q_trade = (demand_intercept - supply_intercept - wedge) / (demand_slope + supply_slope)
        firm_cost = demand_intercept - demand_slope * q_trade
        worker_wage = firm_cost - wedge
        label = "tax incidence wedge"
    else:
        subsidy_demand = demand + wedge
        q_trade = (demand_intercept + wedge - supply_intercept) / (demand_slope + supply_slope)
        worker_wage = supply_intercept + supply_slope * q_trade
        firm_cost = worker_wage - wedge
        label = "subsidy expands employment"

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=q[demand >= 0], y=demand[demand >= 0], name="Labor demand / MRP", line=dict(width=3, color=GREEN)))
    fig.add_trace(go.Scatter(x=q, y=supply, name="Labor supply", line=dict(width=3, color=GOLD)))
    if policy == "Payroll tax":
        fig.add_trace(go.Scatter(x=q, y=supply + wedge, name="Supply incl. tax", line=dict(width=3, color=RED, dash="dash")))
    if policy == "Wage subsidy":
        fig.add_trace(go.Scatter(x=q[demand + wedge >= 0], y=(demand + wedge)[demand + wedge >= 0], name="Demand incl. subsidy", line=dict(width=3, color=BLUE, dash="dash")))
    if policy == "Minimum wage":
        fig.add_shape(type="line", x0=0, x1=120, y0=worker_wage, y1=worker_wage, line=dict(width=2, dash="dash", color=RED))
    fig.add_trace(go.Scatter(x=[q_eq], y=[w_eq], mode="markers+text", text=["Market"], textposition="top center", marker=dict(size=11, color=SAGE), name="Market equilibrium"))
    fig.add_trace(go.Scatter(x=[q_trade], y=[worker_wage], mode="markers+text", text=["Policy"], textposition="top center", marker=dict(size=12, color=POINT), name="Policy outcome"))
    fig.update_xaxes(title="Labor hours / employment")
    fig.update_yaxes(title="Wage or labor cost")
    st.plotly_chart(finish(fig), use_container_width=True, key="labor_policy_chart")

    c1, c2, c3 = st.columns(3)
    c1.metric("Employment", f"{q_trade:.1f}")
    c2.metric("Worker wage", f"{worker_wage:.2f}")
    c3.metric("Firm labor cost", f"{firm_cost:.2f}")
    st.caption(label)

    if st.toggle("Full analysis", value=False, key="labor_policy_analysis"):
        st.markdown(
            "Labor demand is derived from marginal revenue product. Labor policy changes the wage, the cost to firms, or the wedge between them. The employment effect depends on which side of the market adjusts and on the elasticities of labor demand and supply."
        )
