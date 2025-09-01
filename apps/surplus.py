import streamlit as st
import plotly.graph_objects as go
from math import isnan

# Your shared helpers
from apps.common import Line, base_fig, add_point, intersect

# ───────────────────────────
# Geometry: make lines span the full axes box
# ───────────────────────────
EPS = 1e-12
def clip_line_to_box(m, b, xmin, xmax, ymin, ymax):
    """
    Clip the infinite line y = m*x + b to the axes-aligned box [xmin,xmax]×[ymin,ymax].
    Returns two boundary points (x0,y0), (x1,y1) so the segment touches the plot edges.
    """
    pts = []
    # Intersections with x = xmin, xmax
    for x in (xmin, xmax):
        y = m * x + b
        if ymin - EPS <= y <= ymax + EPS:
            pts.append((x, y))
    # Intersections with y = ymin, ymax
    if abs(m) > EPS:
        for y in (ymin, ymax):
            x = (y - b) / m
            if xmin - EPS <= x <= xmax + EPS:
                pts.append((x, y))

    # Deduplicate within a small tolerance
    uniq = []
    for x, y in pts:
        k = (round(x, 9), round(y, 9))
        if k not in [(round(px, 9), round(py, 9)) for px, py in uniq]:
            uniq.append((x, y))

    if len(uniq) < 2:
        return None
    uniq.sort()
    return uniq[0], uniq[-1]


def add_full_span_line(fig, alpha, beta, *, name, xmin, xmax, ymin, ymax, width=3, dash=None, legendgroup=None):
    """
    Plot P = alpha + beta*Q as a segment that spans the current axes box.
    """
    seg = clip_line_to_box(beta, alpha, xmin, xmax, ymin, ymax)
    if seg is None:
        return
    (x0, y0), (x1, y1) = seg
    fig.add_scatter(
        x=[x0, x1], y=[y0, y1],
        mode="lines",
        name=name,
        line=dict(width=width, dash=dash) if dash else dict(width=width),
        legendgroup=legendgroup
    )

# ───────────────────────────
# Surplus shading for the shifted equilibrium
# ───────────────────────────
def add_consumer_surplus(fig, a_d, b_d, q_star, p_star, color="rgba(33, 150, 243, 0.25)"):
    """
    Shade Consumer Surplus for the *shifted* equilibrium:
    polygon between demand and the price line P = P* from Q=0..Q*.
    """
    p_d0 = a_d
    p_dq = a_d + b_d * q_star
    if q_star > 0 and p_d0 > p_star:
        fig.add_trace(go.Scatter(
            x=[0, q_star, q_star, 0],
            y=[p_star, p_star, p_dq, p_d0],
            mode="lines",
            fill="toself",
            name="Consumer Surplus",
            hoverinfo="skip",
            line=dict(width=0),
            fillcolor=color,
            showlegend=True
        ))
        return 0.5 * (p_d0 - p_star) * q_star
    return 0.0


def add_producer_surplus(fig, a_s, b_s, q_star, p_star, color="rgba(255, 152, 0, 0.28)"):
    """
    Shade Producer Surplus for the *shifted* equilibrium:
    polygon between the price line P = P* and supply from Q=0..Q*.
    """
    p_s0 = a_s
    p_sq = a_s + b_s * q_star
    if q_star > 0 and p_star > p_s0:
        fig.add_trace(go.Scatter(
            x=[0, q_star, q_star, 0],
            y=[p_s0, p_sq, p_star, p_star],
            mode="lines",
            fill="toself",
            name="Producer Surplus",
            hoverinfo="skip",
            line=dict(width=0),
            fillcolor=color,
            showlegend=True
        ))
        return 0.5 * (p_star - p_s0) * q_star
    return 0.0
# ──────────────────────────
def app():
    st.subheader("Shifts — Demand or Supply (single curve)")

    # Axes (visible box)
    xmax = st.sidebar.number_input("Max Q", 10, 1000, 200, 10)
    ymax = st.sidebar.number_input("Max P", 10, 1000, 50, 5)
    xmin, ymin = 0.0, 0.0

    # Baseline coefficients: P = α + βQ
    st.sidebar.markdown("**Baseline curves** *(P = α + βQ)*")
    ad = st.sidebar.number_input("Demand α (baseline)", value=30.0, step=1.0)
    bd = st.sidebar.number_input("Demand β (baseline; <0)", value=-0.2, step=0.05, format="%.3f")
    as_ = st.sidebar.number_input("Supply α (baseline)", value=5.0, step=1.0)
    bs  = st.sidebar.number_input("Supply β (baseline; >0)", value=0.1, step=0.05, format="%.3f")

    D0, S0 = Line(ad, bd), Line(as_, bs)

    # Shift controls (absolute deltas; simple & explicit for teaching)
    which = st.radio("Shift which curve?", ["Demand", "Supply"], horizontal=True)
    d_alpha = st.slider("Vertical shift Δα (parallel shift)", -20.0, 20.0, 0.0, 0.5)
    d_beta  = st.slider("Pivot Δβ (slope change)", -0.5, 0.5, 0.0, 0.05)

    # Build shifted lines
    if which == "Demand":
        D1, S1 = Line(D0.a + d_alpha, D0.b + d_beta), S0
        tag = "Demand parallel ↑" if d_alpha > 0 else ("Demand parallel ↓" if d_alpha < 0 else "Demand pivot")
    else:
        D1, S1 = D0, Line(S0.a + d_alpha, S0.b + d_beta)
        tag = "Supply parallel ↑" if d_alpha > 0 else ("Supply parallel ↓" if d_alpha < 0 else "Supply pivot")

    # Equilibria
    q0, p0 = intersect(D0, S0)  # baseline
    q1, p1 = intersect(D1, S1)  # shifted

    # Display options
    c1, c2, c3, c4, c5 = st.columns(5)
    with c1:
        hide_d = st.toggle("Hide Demand", value=False)
    with c2:
        hide_s = st.toggle("Hide Supply", value=False)
    with c3:
        show_grid = st.toggle("Show grid", value=True)
    with c4:
        show_cs = st.toggle("Show CS (shifted)", value=True)
    with c5:
        show_ps = st.toggle("Show PS (shifted)", value=True)

    # Figure and axes
    fig = base_fig(xmax=xmax, ymax=ymax)

    # Make sure axes match our clipping box and show a readable grid
    y_needed = max(
        ymax, ad, as_, D1.a, S1.a,
        (p0 if not isnan(p0) else 0.0),
        (p1 if not isnan(p1) else 0.0)
    )
    fig.update_xaxes(range=[xmin, xmax], title="Quantity (Q)",
                     showgrid=show_grid, gridwidth=1, gridcolor="rgba(0,0,0,0.12)", zeroline=False, ticks="outside")
    fig.update_yaxes(range=[ymin, y_needed], title="Price (P)",
                     showgrid=show_grid, gridwidth=1, gridcolor="rgba(0,0,0,0.12)", zeroline=False, ticks="outside")
    fig.update_layout(plot_bgcolor="white", paper_bgcolor="white")

    # Optional surplus shading for the *shifted* equilibrium (place BELOW lines)
    cs_val = ps_val = 0.0
    if not (isnan(q1) or isnan(p1)):
        if show_cs and not hide_d:
            cs_val = add_consumer_surplus(fig, D1.a, D1.b, q1, p1)
        if show_ps and not hide_s:
            ps_val = add_producer_surplus(fig, S1.a, S1.b, q1, p1)

    # Baseline lines (ghost, dashed)
    if not hide_d:
        add_full_span_line(fig, D0.a, D0.b, name="Demand (baseline)", xmin=xmin, xmax=xmax, ymin=ymin, ymax=y_needed, dash="dash", width=2, legendgroup="D")
    if not hide_s:
        add_full_span_line(fig, S0.a, S0.b, name="Supply (baseline)",  xmin=xmin, xmax=xmax, ymin=ymin, ymax=y_needed, dash="dash", width=2, legendgroup="S")

    # Shifted (current) lines — on top
    if not hide_d:
        add_full_span_line(fig, D1.a, D1.b, name="Demand", xmin=xmin, xmax=xmax, ymin=ymin, ymax=y_needed, width=3, legendgroup="D")
    if not hide_s:
        add_full_span_line(fig, S1.a, S1.b, name="Supply", xmin=xmin, xmax=xmax, ymin=ymin, ymax=y_needed, width=3, legendgroup="S")

    # Equilibrium markers & guides
    if not (isnan(q0) or isnan(p0)):
        add_point(fig, q0, p0, "(Q0*, P0*)")
        fig.add_shape(type="line", x0=q0, y0=0, x1=q0, y1=p0, line=dict(dash="dot", width=1))
        fig.add_shape(type="line", x0=0, y0=p0, x1=q0, y1=p0, line=dict(dash="dot", width=1))
    if not (isnan(q1) or isnan(p1)):
        add_point(fig, q1, p1, "(Q1*, P1*)")
        fig.add_shape(type="line", x0=q1, y0=0, x1=q1, y1=p1, line=dict(dash="dot", width=1))
        fig.add_shape(type="line", x0=0, y0=p1, x1=q1, y1=p1, line=dict(dash="dot", width=1))

    # Tag in the corner describing the shift
    fig.add_annotation(x=0.75 * xmax, y=0.92 * y_needed, text=tag, showarrow=False)

    st.plotly_chart(fig, use_container_width=True, key="shift_single_chart")

    # Direction summary
    price_dir = "↑" if p1 > p0 else ("↓" if p1 < p0 else "no change")
    qty_dir   = "↑" if q1 > q0 else ("↓" if q1 < q0 else "no change")
    st.markdown(
        f"**Price:** {price_dir} &nbsp; | &nbsp; **Quantity:** {qty_dir}"
        + (f" &nbsp; | &nbsp; **CS ≈ {cs_val:.2f}**" if show_cs and not isnan(p1) else "")
        + (f" &nbsp; | &nbsp; **PS ≈ {ps_val:.2f}**" if show_ps and not isnan(p1) else "")
    )

    # Advanced toggle
    show_adv = st.toggle("Advanced (show equations)", value=False, key="single_shift_adv")
    if show_adv:
        st.latex(r"P = \alpha + \beta Q")
        st.caption("Demand typically has β < 0; Supply has β > 0.")    