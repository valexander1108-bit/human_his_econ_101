import streamlit as st
from math import isnan

# Shared helpers from your project
from apps.common import Line, base_fig, add_point, intersect

# ──────────────────────────────────────────────────────────────────────────────
# Geometry helpers: draw lines that touch the plot edges
# ──────────────────────────────────────────────────────────────────────────────
EPS = 1e-12

def clip_line_to_box(m, b, xmin, xmax, ymin, ymax):
    """
    Clip the infinite line y = m*x + b to the axis-aligned box [xmin,xmax]×[ymin,ymax].
    Returns two boundary points (x0,y0), (x1,y1) so the segment spans the visible area.
    If the line doesn't cross the box, return None.
    """
    pts = []

    # Intersections with vertical borders x = xmin, xmax
    for x in (xmin, xmax):
        y = m * x + b
        if ymin - EPS <= y <= ymax + EPS:
            pts.append((x, y))

    # Intersections with horizontal borders y = ymin, ymax
    if abs(m) > EPS:
        for y in (ymin, ymax):
            x = (y - b) / m
            if xmin - EPS <= x <= xmax + EPS:
                pts.append((x, y))

    # Deduplicate within tolerance
    uniq = []
    for x, y in pts:
        key = (round(x, 9), round(y, 9))
        if key not in [(round(px, 9), round(py, 9)) for px, py in uniq]:
            uniq.append((x, y))

    if len(uniq) < 2:
        return None

    # Stable ordering and extremes → full-width segment
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

# ──────────────────────────────────────────────────────────────────────────────
# App
# ──────────────────────────────────────────────────────────────────────────────
def app():
    st.subheader("Shifts — Demand or Supply (single curve)")

    # Visible axes box (students stay in the non-negative quadrant)
    xmax = st.sidebar.number_input("Max Q", 10, 1000, 200, 10)
    ymax = st.sidebar.number_input("Max P", 10, 1000, 50, 5)
    xmin, ymin = 0.0, 0.0

    # Baseline coefficients: P = α + βQ
    st.sidebar.markdown("**Baseline Curves** *(P = α + βQ)*")
    ad = st.sidebar.number_input("Demand α", value=30.0, step=1.0)
    bd = st.sidebar.number_input("Demand β", value=-0.2, step=0.05, format="%.3f")
    as_ = st.sidebar.number_input("Supply α", value=5.0, step=1.0)
    bs  = st.sidebar.number_input("Supply β", value=0.1, step=0.05, format="%.3f")

    # Build baseline lines
    D0, S0 = Line(ad, bd), Line(as_, bs)

    # SINGLE SHIFT ONLY: remove pivot, keep vertical (parallel) shift Δα
    which = st.radio("Shift which curve?", ["Demand", "Supply"], horizontal=True)
    d_alpha = st.slider("Vertical shift Δα (parallel shift only)", -20.0, 20.0, 0.0, 0.5)

    # Apply the shift (parallel only)
    if which == "Demand":
        D1, S1 = Line(D0.a + d_alpha, D0.b), S0
        tag = "Demand ↑ (Δα>0)" if d_alpha > 0 else ("Demand ↓ (Δα<0)" if d_alpha < 0 else "Demand (no change)")
    else:
        D1, S1 = D0, Line(S0.a + d_alpha, S0.b)
        tag = "Supply ↑ (Δα>0)" if d_alpha > 0 else ("Supply ↓ (Δα<0)" if d_alpha < 0 else "Supply (no change)")

    # Equilibria
    q0, p0 = intersect(D0, S0)  # baseline equilibrium
    q1, p1 = intersect(D1, S1)  # shifted equilibrium

    # Display options
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        hide_d = st.toggle("Hide Demand", value=False)
    with c2:
        hide_s = st.toggle("Hide Supply", value=False)
    with c3:
        show_grid = st.toggle("Show grid", value=True)
    with c4:
        show_baseline = st.toggle("Show baseline (ghost)", value=True)

    # Figure
    fig = base_fig(xmax=xmax, ymax=ymax)

    # Axes ranges + grid → match the clipping box and keep it readable
    y_needed = max(
        ymax, ad, as_,
        (p0 if not isnan(p0) else 0.0),
        (p1 if not isnan(p1) else 0.0)
    )
    fig.update_xaxes(
        range=[xmin, xmax], title="Quantity (Q)",
        showgrid=show_grid, gridwidth=1, gridcolor="rgba(0,0,0,0.12)",
        zeroline=False, ticks="outside"
    )
    fig.update_yaxes(
        range=[ymin, y_needed], title="Price (P)",
        showgrid=show_grid, gridwidth=1, gridcolor="rgba(0,0,0,0.12)",
        zeroline=False, ticks="outside"
    )
    fig.update_layout(plot_bgcolor="white", paper_bgcolor="white")

    # Baseline lines (ghost, dashed)
    if show_baseline:
        if not hide_d:
            add_full_span_line(fig, D0.a, D0.b, name="Demand (baseline)", xmin=xmin, xmax=xmax, ymin=ymin, ymax=y_needed, dash="dash", width=2, legendgroup="D")
        if not hide_s:
            add_full_span_line(fig, S0.a, S0.b, name="Supply (baseline)",  xmin=xmin, xmax=xmax, ymin=ymin, ymax=y_needed, dash="dash", width=2, legendgroup="S")

    # Shifted/current lines — solid, on top
    if not hide_d:
        add_full_span_line(fig, D1.a, D1.b, name="Demand", xmin=xmin, xmax=xmax, ymin=ymin, ymax=y_needed, width=3, legendgroup="D")
    if not hide_s:
        add_full_span_line(fig, S1.a, S1.b, name="Supply", xmin=xmin, xmax=xmax, ymin=ymin, ymax=y_needed, width=3, legendgroup="S")

    # Equilibrium markers & guides
    if not (isnan(q0) or isnan(p0)) and show_baseline:
        add_point(fig, q0, p0, "(Q0*, P0*)")
        fig.add_shape(type="line", x0=q0, y0=0, x1=q0, y1=p0, line=dict(dash="dot", width=1))
        fig.add_shape(type="line", x0=0, y0=p0, x1=q0, y1=p0, line=dict(dash="dot", width=1))

    if not (isnan(q1) or isnan(p1)):
        add_point(fig, q1, p1, "(Q1*, P1*)")
        fig.add_shape(type="line", x0=q1, y0=0, x1=q1, y1=p1, line=dict(dash="dot", width=1))
        fig.add_shape(type="line", x0=0, y0=p1, x1=q1, y1=p1, line=dict(dash="dot", width=1))

    # Shift tag
    fig.add_annotation(x=0.75 * xmax, y=0.92 * y_needed, text=tag, showarrow=False)

    # Render
    st.plotly_chart(fig, use_container_width=True, key="shift_single_chart")

    # Direction summary
    if not (isnan(q0) or isnan(p0) or isnan(q1) or isnan(p1)):
        price_dir = "↑" if p1 > p0 else ("↓" if p1 < p0 else "no change")
        qty_dir   = "↑" if q1 > q0 else ("↓" if q1 < q0 else "no change")
        st.markdown(f"**Price:** {price_dir} &nbsp; | &nbsp; **Quantity:** {qty_dir}")

    # Advanced toggle
    show_adv = st.toggle("Advanced (show equations)", value=False, key="single_shift_adv")
    if show_adv:
        st.latex(r"P = \alpha + \beta Q")
        st.caption("Demand typically has β < 0; Supply has β > 0.")
