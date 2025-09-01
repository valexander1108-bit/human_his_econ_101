import streamlit as st
from apps.common import Line, base_fig, add_point, intersect

# ---------- Geometry helpers ----------
EPS = 1e-12

def clip_line_to_box(m, b, xmin, xmax, ymin, ymax):
    """
    Given a line y = m*x + b and an axis-aligned box [xmin,xmax]x[ymin,ymax],
    return two points (x0,y0), (x1,y1) where the infinite line intersects the box.
    This ensures the plotted segment touches the visible edges of the chart.

    If the line does not cross the box, return None.
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

    # Deduplicate (within float tolerance)
    uniq = []
    for x, y in pts:
        k = (round(x, 9), round(y, 9))
        if k not in [(round(px, 9), round(py, 9)) for px, py in uniq]:
            uniq.append((x, y))

    if len(uniq) < 2:
        return None

    # Sort and return two extreme points for a stable, full-span segment
    uniq.sort()
    return uniq[0], uniq[-1]


def add_full_span_line(fig, alpha, beta, name, xmin, xmax, ymin, ymax, width=3):
    """
    Plot P = alpha + beta*Q as a segment that spans the full visible axes box.
    """
    m, b = beta, alpha
    seg = clip_line_to_box(m, b, xmin, xmax, ymin, ymax)
    if seg is None:
        return  # line is outside the visible viewport
    (x0, y0), (x1, y1) = seg
    fig.add_scatter(x=[x0, x1], y=[y0, y1], mode="lines",
                    name=name, line=dict(width=width))


# ---------- App ----------
def app():
    st.subheader("Market Model")

    # ---- Axes bounds (define the visible 'box' we will clip to) ----
    xmax = st.sidebar.number_input("Max Q", 10, 1000, 200, 10)
    ymax = st.sidebar.number_input("Max P", 10, 1000, 50, 5)
    xmin, ymin = 0.0, 0.0  # we teach in the non-negative quadrant

    # ---- Demand inputs ----
    st.sidebar.markdown("**DEMAND**")
    ad = st.sidebar.number_input("α (intercept)", value=float(st.session_state.get("alpha_d", 30.0)),
                                 step=1.0)
    bd = st.sidebar.number_input("β (negative slope)", value=float(st.session_state.get("beta_d", -0.2)),
                                 step=0.05, format="%.3f")

    # ---- Supply inputs ----
    st.sidebar.markdown("**SUPPLY**")
    as_ = st.sidebar.number_input("α (intercept)", value=float(st.session_state.get("alpha_s", 5.0)),
                                  step=1.0)
    bs  = st.sidebar.number_input("β (positive slope)", value=float(st.session_state.get("beta_s", 0.1)),
                                  step=0.05, format="%.3f")

    # Build Line objects for algebraic utilities / intersection
    D, S = Line(ad, bd), Line(as_, bs)
    q_star, p_star = intersect(D, S)

    # Persist previous equilibrium for continuity cues
    if "prev_eq" not in st.session_state:
        st.session_state.prev_eq = None

    # ---- Visibility toggles ----
    c1, c2, c3 = st.columns(3)
    with c1:
        hide_d = st.toggle("Hide Demand", value=False, key="d_hd")
    with c2:
        hide_s = st.toggle("Hide Supply", value=False, key="s_hd")
    with c3:
        show_grid = st.toggle("Show grid", value=True, key="show_grid")

    # ---- Figure ----
    fig = base_fig(xmax=xmax, ymax=ymax)

    # Ensure our box is exactly what the helper expects
    fig.update_xaxes(range=[xmin, xmax], title="Quantity (Q)")
    fig.update_yaxes(range=[ymin, ymax], title="Price (P)")

    # Grid + background (clean & readable)
    fig.update_xaxes(showgrid=show_grid, gridwidth=1, gridcolor="rgba(0,0,0,0.12)", zeroline=False, ticks="outside")
    fig.update_yaxes(showgrid=show_grid, gridwidth=1, gridcolor="rgba(0,0,0,0.12)", zeroline=False, ticks="outside")
    fig.update_layout(plot_bgcolor="white", paper_bgcolor="white")

    # Full-span lines (touch edges)
    if not hide_d:
        add_full_span_line(fig, ad, bd, "Demand", xmin, xmax, ymin, ymax)
    if not hide_s:
        add_full_span_line(fig, as_, bs, "Supply", xmin, xmax, ymin, ymax)

    # Equilibrium marker & continuity label
    from math import isnan
    if not hide_d and not hide_s and not (isnan(q_star) or isnan(p_star)):
        add_point(fig, q_star, p_star, "(Q*, P*)")
        st.session_state.prev_eq = (q_star, p_star)

        # dashed guide lines to axes
        fig.add_shape(type="line", x0=q_star, y0=0, x1=q_star, y1=p_star,
                      line=dict(dash="dot", width=1))
        fig.add_shape(type="line", x0=0, y0=p_star, x1=q_star, y1=p_star,
                      line=dict(dash="dot", width=1))

        # axis labels for Q* and P*
        fig.add_annotation(x=q_star, y=0, text=f"Q*={q_star:.2f}",
                           showarrow=False, yshift=-10)
        fig.add_annotation(x=0, y=p_star, text=f"P*={p_star:.2f}",
                           showarrow=False, xshift=-20)
    elif st.session_state.prev_eq:
        q0, p0 = st.session_state.prev_eq
        add_point(fig, q0, p0, "previous equilibrium")

    st.plotly_chart(fig, use_container_width=True, key="eq_chart")
    st.markdown(f"**Equilibrium:** Q* = {q_star:.2f}, P* = {p_star:.2f}")

    # ---- Advanced math panel (kept inside the app for neatness) ----
    show_adv = st.toggle("Advanced (show equations)", value=False, key="stat_equ__adv")
    if show_adv:
        st.latex(r"P = \alpha + \beta Q")
        st.caption("Demand typically has β < 0; Supply has β > 0.")

    # Detect whether we preloaded coefficients from a schedule page
    prefilled = any(k in st.session_state for k in ("alpha_d","beta_d","alpha_s","beta_s"))
    if prefilled:
        st.caption("Loaded coefficients from a schedule page.")
