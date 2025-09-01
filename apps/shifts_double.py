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


def add_full_span_line(fig, alpha, beta, *, name, xmin, xmax, ymin, ymax, width=3, dash=None):
    """
    Plot P = alpha + beta*Q as a segment that spans the current axes box.
    Legends are disabled per-trace for a cleaner classroom view.
    """
    seg = clip_line_to_box(beta, alpha, xmin, xmax, ymin, ymax)
    if seg is None:
        return
    (x0, y0), (x1, y1) = seg
    fig.add_scatter(
        x=[x0, x1], y=[y0, y1],
        mode="lines",
        name=name,
        showlegend=False,  # <— legend removed
        line=dict(width=width, dash=dash) if dash else dict(width=width)),


def add_inline_label(fig, alpha, beta, *, text, xmax, ymin, ymax, pad=0.96, side="right"):
    """
    Place a small text label directly on the line (so we can remove the legend).
    - side="right" puts label near the right edge; "left" near the left edge.
    - pad is the fraction of xmax to use (e.g., 0.96 -> close to the right edge).
    We clamp the y position into [ymin, ymax] so labels never render off-screen.
    """
    x = pad * xmax if side == "right" else (1.0 - pad) * xmax
    y = alpha + beta * x
    # Clamp to be safely inside the frame
    y = min(max(y, ymin + 0.02 * (ymax - ymin)), ymax - 0.02 * (ymax - ymin))

    fig.add_annotation(
        x=x, y=y, text=text, showarrow=False,
        xanchor="left" if side == "right" else "right",
        yanchor="middle",
        bgcolor="rgba(255,255,255,0.7)",
        bordercolor="rgba(0,0,0,0.15)",
        borderwidth=1,
        font=dict(size=11)
    )

# ──────────────────────────────────────────────────────────────────────────────
# One pane (either Demand-shift or Supply-shift)
# ──────────────────────────────────────────────────────────────────────────────
def make_pane(title, D0, S0, xmax, ymax, which, *, hide_d, hide_s, show_baseline, show_grid):
    st.markdown(f"### {title}")

    # Parallel (vertical) shift only
    d_alpha = st.slider(f"{which} Δα (parallel shift)", -20.0, 20.0, 0.0, 0.5, key=f"{title}_a")

    # Build shifted lines
    if which == "Demand":
        D1, S1 = Line(D0.a + d_alpha, D0.b), S0
        tag = "Demand ↑ (Δα>0)" if d_alpha > 0 else ("Demand ↓ (Δα<0)" if d_alpha < 0 else "Demand (no change)")
    else:
        D1, S1 = D0, Line(S0.a + d_alpha, S0.b)
        tag = "Supply ↑ (Δα>0)" if d_alpha > 0 else ("Supply ↓ (Δα<0)" if d_alpha < 0 else "Supply (no change)")

    # Equilibria: baseline vs shifted
    q0, p0 = intersect(D0, S0)
    q1, p1 = intersect(D1, S1)

    # Figure and axes
    xmin, ymin = 0.0, 0.0
    fig = base_fig(xmax=xmax, ymax=ymax)

    # y_needed ensures intercepts and both P* values are visible
    y_needed = max(
        ymax, D0.a, S0.a, D1.a, S1.a,
        (p0 if not isnan(p0) else 0.0),
        (p1 if not isnan(p1) else 0.0)
    )

    # Axes styling + grid; automargins to avoid label clipping
    fig.update_xaxes(
        range=[xmin, xmax], title="Quantity (Q)",
        showgrid=show_grid, gridwidth=1, gridcolor="rgba(0,0,0,0.12)",
        zeroline=False, ticks="outside", automargin=True
    )
    fig.update_yaxes(
        range=[ymin, y_needed], title="Price (P)",
        showgrid=show_grid, gridwidth=1, gridcolor="rgba(0,0,0,0.12)",
        zeroline=False, ticks="outside", automargin=True
    )

    # Global layout tweaks for better rendering & stability
    fig.update_layout(
        plot_bgcolor="white",
        paper_bgcolor="white",
        height=560,
        margin=dict(l=40, r=24, t=24, b=40),
        uirevision="shifts-double",  # keep zoom/pan state while sliders move
        showlegend=False             # <— legend removed globally
    )

    # Baseline (ghost) lines — dashed, under current
    if show_baseline:
        if not hide_d:
            add_full_span_line(fig, D0.a, D0.b, name="D0",
                               xmin=xmin, xmax=xmax, ymin=ymin, ymax=y_needed,
                               dash="dash", width=2)
        if not hide_s:
            add_full_span_line(fig, S0.a, S0.b, name="S0",
                               xmin=xmin, xmax=xmax, ymin=ymin, ymax=y_needed,
                               dash="dash", width=2)

    # Current (shifted) lines — solid, on top
    if not hide_d:
        add_full_span_line(fig, D1.a, D1.b, name="New Demand",
                           xmin=xmin, xmax=xmax, ymin=ymin, ymax=y_needed, width=3)
    if not hide_s:
        add_full_span_line(fig, S1.a, S1.b, name="New Supply",
                           xmin=xmin, xmax=xmax, ymin=ymin, ymax=y_needed, width=3)

    # Inline labels instead of legends
    if not hide_d:
        if show_baseline:
            add_inline_label(fig, D0.a, D0.b, text="D(original)", xmax=xmax, ymin=ymin, ymax=y_needed, pad=0.06, side="left")
        add_inline_label(fig, D1.a, D1.b, text="Demand", xmax=xmax, ymin=ymin, ymax=y_needed, pad=0.96, side="right")
    if not hide_s:
        if show_baseline:
            add_inline_label(fig, S0.a, S0.b, text="S(original)", xmax=xmax, ymin=ymin, ymax=y_needed, pad=0.06, side="left")
        add_inline_label(fig, S1.a, S1.b, text="Supply", xmax=xmax, ymin=ymin, ymax=y_needed, pad=0.96, side="right")

    # Equilibrium markers & crosshairs
    if not (isnan(q0) or isnan(p0)) and show_baseline:
        add_point(fig, q0, p0, "(Q0*, P0*)")
        fig.add_shape(type="line", x0=q0, y0=0, x1=q0, y1=p0, line=dict(dash="dot", width=1))
        fig.add_shape(type="line", x0=0, y0=p0, x1=q0, y1=p0, line=dict(dash="dot", width=1))

    if not (isnan(q1) or isnan(p1)):
        add_point(fig, q1, p1, "(Q1*, P1*)")
        fig.add_shape(type="line", x0=q1, y0=0, x1=q1, y1=p1, line=dict(dash="dot", width=1))
        fig.add_shape(type="line", x0=0, y0=p1, x1=q1, y1=p1, line=dict(dash="dot", width=1))

    # Shift tag (small corner note)
    fig.add_annotation(x=0.75 * xmax, y=0.92 * y_needed, text=tag, showarrow=False)

    # Render pane with a lean config for crisp classroom display
    st.plotly_chart(
        fig,
        use_container_width=True,
        key=f"{title}_chart",
        config={"displayModeBar": False, "responsive": True, "scrollZoom": False}
    )

    # Direction readout
    price_dir = "↑" if p1 > p0 else ("↓" if p1 < p0 else "no change/ambiguous")
    qty_dir   = "↑" if q1 > q0 else ("↓" if q1 < q0 else "no change/ambiguous")
    st.markdown(f"**Price:** {price_dir} &nbsp; | &nbsp; **Quantity:** {qty_dir}")

# ──────────────────────────────────────────────────────────────────────────────
# App
# ──────────────────────────────────────────────────────────────────────────────
def app():
    st.subheader("Double Shifts — Demand vs Supply (side-by-side)")

    # Global axes (visible box for both panes)
    xmax = st.sidebar.number_input("Max Q", 10, 1000, 200, 10)
    ymax = st.sidebar.number_input("Max P", 10, 1000, 50, 5)

    # Baseline curves: P = α + βQ
    st.sidebar.markdown("**Baseline curves** *(P = α + βQ)*")
    ad = st.sidebar.number_input("Demand α ", value=30.0, step=1.0)
    bd = st.sidebar.number_input("Demand β", value=-0.2, step=0.05, format="%.3f")
    as_ = st.sidebar.number_input("Supply α", value=5.0, step=1.0)
    bs  = st.sidebar.number_input("Supply β", value=0.1, step=0.05, format="%.3f")

    D0, S0 = Line(ad, bd), Line(as_, bs)

    # Global display toggles (apply to both panes)
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        hide_d = st.toggle("Hide Demand", value=False)
    with c2:
        hide_s = st.toggle("Hide Supply", value=False)
    with c3:
        show_grid = st.toggle("Show grid", value=True)
    with c4:
        show_baseline = st.toggle("Show baseline (ghost)", value=True)

    # Two panes: left = demand shift; right = supply shift
    col1, col2 = st.columns(2)
    with col1:
        make_pane("Demand shift", D0, S0, xmax, ymax, "Demand",
                  hide_d=hide_d, hide_s=hide_s, show_baseline=show_baseline, show_grid=show_grid)
    with col2:
        make_pane("Supply shift", D0, S0, xmax, ymax, "Supply",
                  hide_d=hide_d, hide_s=hide_s, show_baseline=show_baseline, show_grid=show_grid)

    # Advanced toggle
    show_adv = st.toggle("Advanced (show equations)", value=False, key="shifts_double_adv")
    if show_adv:
        st.latex(r"P = \alpha + \beta Q")
        st.caption("Demand typically has β < 0; Supply has β > 0.")
