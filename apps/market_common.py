import math

import plotly.graph_objects as go

from apps.common import Line, add_point, base_fig, intersect, line_y


DEMAND_COLOR = "#1d511e"
SUPPLY_COLOR = "#6C7A61"
CONTROL_COLOR = "#B38210"
DWL_COLOR = "rgba(178, 63, 53, 0.24)"
CS_COLOR = "rgba(51, 101, 138, 0.24)"
PS_COLOR = "rgba(196, 154, 108, 0.30)"


def is_valid_point(q, p):
    return not (math.isnan(q) or math.isnan(p)) and q >= 0 and p >= 0


def quantity_at_price(line: Line, price):
    if abs(line.b) < 1e-12:
        return float("nan")
    return (price - line.a) / line.b


def add_full_span_line(fig, alpha, beta, name, xmin, xmax, ymin, ymax, width=3, dash=None, color=None):
    span = max(xmax - xmin, ymax - ymin, 10) * 100
    x0, x1 = -span, span
    fig.add_scatter(
        x=[x0, x1],
        y=[beta * x0 + alpha, beta * x1 + alpha],
        mode="lines",
        name=name,
        line=dict(width=width, dash=dash, color=color) if dash or color else dict(width=width),
    )


def add_market_lines(fig, demand, supply, xmax, ymax):
    add_full_span_line(fig, demand.a, demand.b, "Demand", 0, xmax, 0, ymax, color=DEMAND_COLOR)
    add_full_span_line(fig, supply.a, supply.b, "Supply", 0, xmax, 0, ymax, color=SUPPLY_COLOR)


def add_price_line(fig, price, xmax, name="Price control"):
    fig.add_shape(type="line", x0=0, y0=price, x1=xmax, y1=price, line=dict(width=2, dash="dash", color=CONTROL_COLOR))
    fig.add_annotation(x=xmax * 0.92, y=price, text=f"{name}: {price:.2f}", showarrow=False, yshift=12)


def add_guides(fig, q, p, label):
    add_point(fig, q, p, label)
    fig.add_shape(type="line", x0=q, y0=0, x1=q, y1=p, line=dict(dash="dot", width=1))
    fig.add_shape(type="line", x0=0, y0=p, x1=q, y1=p, line=dict(dash="dot", width=1))


def add_surplus_areas(fig, demand, supply, q, price, show_cs=True, show_ps=True):
    cs = max(0.0, 0.5 * max(line_y(demand, 0) - price, 0) * q)
    ps = max(0.0, 0.5 * max(price - line_y(supply, 0), 0) * q)
    if q <= 0:
        return 0.0, 0.0
    if show_cs and cs > 0:
        fig.add_trace(go.Scatter(
            x=[0, q, q, 0],
            y=[price, price, line_y(demand, q), line_y(demand, 0)],
            mode="lines",
            fill="toself",
            name="Consumer surplus",
            line=dict(width=0),
            fillcolor=CS_COLOR,
            hoverinfo="skip",
        ))
    if show_ps and ps > 0:
        fig.add_trace(go.Scatter(
            x=[0, q, q, 0],
            y=[line_y(supply, 0), line_y(supply, q), price, price],
            mode="lines",
            fill="toself",
            name="Producer surplus",
            line=dict(width=0),
            fillcolor=PS_COLOR,
            hoverinfo="skip",
        ))
    return cs, ps


def add_dwl(fig, demand, supply, q_traded, q_eq):
    if q_traded >= q_eq:
        return 0.0
    fig.add_trace(go.Scatter(
        x=[q_traded, q_eq, q_traded],
        y=[line_y(supply, q_traded), line_y(demand, q_eq), line_y(demand, q_traded)],
        mode="lines",
        fill="toself",
        name="Deadweight loss",
        line=dict(width=0),
        fillcolor=DWL_COLOR,
        hoverinfo="skip",
    ))
    return max(0.0, 0.5 * (line_y(demand, q_traded) - line_y(supply, q_traded)) * (q_eq - q_traded))


def market_inputs(prefix, default_ymax=80):
    import streamlit as st

    xmax = st.sidebar.number_input("Max Q", 10, 1000, 160, 10, key=f"{prefix}_xmax")
    ymax = st.sidebar.number_input("Max P", 10, 1000, default_ymax, 5, key=f"{prefix}_ymax")
    st.sidebar.markdown("**Demand**")
    ad = st.sidebar.number_input("Demand intercept", value=70.0, step=1.0, key=f"{prefix}_ad")
    bd = -abs(st.sidebar.number_input("Demand slope magnitude", value=0.35, step=0.05, format="%.3f", key=f"{prefix}_bd"))
    st.sidebar.markdown("**Supply**")
    as_ = st.sidebar.number_input("Supply intercept", value=10.0, step=1.0, key=f"{prefix}_as")
    bs = abs(st.sidebar.number_input("Supply slope", value=0.25, step=0.05, format="%.3f", key=f"{prefix}_bs"))
    return xmax, ymax, Line(ad, bd), Line(as_, bs)


def market_figure(xmax, ymax):
    fig = base_fig(xmax=xmax, ymax=ymax, x_title="Quantity (Q)", y_title="Price (P)")
    fig.update_xaxes(range=[0, xmax])
    fig.update_yaxes(range=[0, ymax])
    fig.update_layout(height=560, legend=dict(orientation="h", yanchor="bottom", y=1.02, x=0))
    return fig


def equilibrium(demand, supply):
    return intersect(demand, supply)
