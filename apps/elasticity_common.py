import numpy as np
import plotly.graph_objects as go


DEMAND_COLOR = "#1d511e"
SUPPLY_COLOR = "#6C7A61"
CURVE_COLOR = "#C49A6C"
POINT_COLOR = "#B38210"
TANGENT_COLOR = "#563b19"
TR_COLOR = "#33658A"


def elasticity_label(value):
    if value < 1:
        return "inelastic"
    if value > 1:
        return "elastic"
    return "unit elastic"


def demand_price(alpha, slope_abs, q):
    return alpha - slope_abs * q


def supply_price(alpha, slope, q):
    return alpha + slope * q


def linear_demand_elasticity(alpha, slope_abs, q):
    p = demand_price(alpha, slope_abs, q)
    if q <= 0 or slope_abs <= 0:
        return float("nan")
    return abs(p / (slope_abs * q))


def linear_supply_elasticity(alpha, slope, q):
    p = supply_price(alpha, slope, q)
    if q <= 0 or slope <= 0:
        return float("nan")
    return p / (slope * q)


def isoelastic_demand_price(anchor_q, anchor_p, elasticity, q):
    q = np.maximum(q, 1e-9)
    return anchor_p * (q / anchor_q) ** (-1.0 / elasticity)


def isoelastic_supply_price(anchor_q, anchor_p, elasticity, q):
    q = np.maximum(q, 1e-9)
    return anchor_p * (q / anchor_q) ** (1.0 / elasticity)


def isoelastic_demand_slope(anchor_q, anchor_p, elasticity, q):
    p = isoelastic_demand_price(anchor_q, anchor_p, elasticity, q)
    return -p / (elasticity * q)


def isoelastic_supply_slope(anchor_q, anchor_p, elasticity, q):
    p = isoelastic_supply_price(anchor_q, anchor_p, elasticity, q)
    return p / (elasticity * q)


def add_tangent(fig, q0, p0, slope, xmax, name):
    span = xmax * 0.18
    q1 = max(0.0, q0 - span)
    q2 = min(xmax, q0 + span)
    fig.add_trace(
        go.Scatter(
            x=[q1, q2],
            y=[p0 + slope * (q1 - q0), p0 + slope * (q2 - q0)],
            mode="lines",
            name=name,
            line=dict(width=2, dash="dot", color=TANGENT_COLOR),
        )
    )


def add_guides(fig, q0, p0):
    fig.add_shape(type="line", x0=q0, y0=0, x1=q0, y1=p0, line=dict(dash="dot", width=1))
    fig.add_shape(type="line", x0=0, y0=p0, x1=q0, y1=p0, line=dict(dash="dot", width=1))
    fig.add_annotation(x=q0, y=0, text=f"Q={q0:.2f}", showarrow=False, yshift=-12)
    fig.add_annotation(x=0, y=p0, text=f"P={p0:.2f}", showarrow=False, xshift=-24)
