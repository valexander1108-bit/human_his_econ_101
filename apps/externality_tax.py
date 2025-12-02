import streamlit as st
import plotly.graph_objects as go

from apps.common import Line, base_fig, add_point, intersect, line_y


def add_full_span_line(fig, alpha, beta, *, name, xmin, xmax, ymin, ymax, width=3, dash=None, color=None):
    """Plot P = alpha + beta*Q as a long segment that spans the viewport."""
    span = max(xmax - xmin, ymax - ymin, 10) * 100
    x0, x1 = -span, span
    y0, y1 = beta * x0 + alpha, beta * x1 + alpha
    fig.add_scatter(
        x=[x0, x1],
        y=[y0, y1],
        mode="lines",
        name=name,
        line=dict(width=width, dash=dash, color=color) if dash or color else dict(width=width),
    )


def add_wedge(fig, lower_line, upper_line, x0, x1, *, name, color):
    """Shade the gap between two lines (upper - lower) on [x0, x1]."""
    if x0 >= x1:
        return
    y0_lower = line_y(lower_line, x0)
    y1_lower = line_y(lower_line, x1)
    y0_upper = line_y(upper_line, x0)
    y1_upper = line_y(upper_line, x1)
    fig.add_trace(
        go.Scatter(
            x=[x0, x1, x1, x0],
            y=[y0_lower, y1_lower, y1_upper, y0_upper],
            fill="toself",
            mode="lines",
            name=name,
            hoverinfo="skip",
            showlegend=True,
            line=dict(width=0),
            fillcolor=color,
        )
    )


def app():
    st.subheader("Externality: Social Cost (Pigouvian Tax)")
    st.info("Model a negative externality: private supply vs. social cost, with Pigouvian tax and DWL.")

    # Axes
    xmax = st.sidebar.number_input("Max Q", 10, 1000, 200, 10)
    ymax = st.sidebar.number_input("Max P", 10, 1000, 50, 5)
    xmin, ymin = 0.0, 0.0

    # Demand & Supply
    st.sidebar.markdown("**Demand (PMB)**  P = α + βQ (β < 0)")
    ad = st.sidebar.number_input("Demand α", value=30.0, step=1.0)
    bd = st.sidebar.number_input("Demand β", value=-0.2, step=0.05, format="%.3f")

    st.sidebar.markdown("**Supply (PMC)**  P = α + βQ (β > 0)")
    as_ = st.sidebar.number_input("Supply α", value=5.0, step=1.0)
    bs = st.sidebar.number_input("Supply β", value=0.1, step=0.05, format="%.3f")

    ext_cost = st.sidebar.number_input("External cost per unit (Pigouvian tax target)", value=10.0, step=1.0, min_value=0.0)

    c1, c2, c3 = st.columns(3)
    with c1:
        show_msc = st.toggle("Show MSC (social cost)", value=False)
    with c2:
        show_dwl = st.toggle("Show DWL wedge", value=False)
    with c3:
        show_tax = st.toggle("Show Pigouvian tax marker", value=True)

    D = Line(ad, bd)
    S_private = Line(as_, bs)
    S_social = Line(as_ + ext_cost, bs)

    q_priv, p_priv = intersect(D, S_private)
    q_soc, p_soc = intersect(D, S_social)

    # Figure
    fig = base_fig(xmax=xmax, ymax=ymax, x_title="Quantity (Q)", y_title="Price (P)")
    fig.update_xaxes(range=[xmin, xmax])
    fig.update_yaxes(range=[ymin, ymax])

    # Lines
    add_full_span_line(fig, ad, bd, name="Demand (PMB)", xmin=xmin, xmax=xmax, ymin=ymin, ymax=ymax, color="#1f77b4")
    add_full_span_line(fig, as_, bs, name="Supply (PMC)", xmin=xmin, xmax=xmax, ymin=ymin, ymax=ymax, color="#ff7f0e")
    if show_msc:
        add_full_span_line(fig, as_ + ext_cost, bs, name="Social Cost (MSC)", xmin=xmin, xmax=xmax, ymin=ymin, ymax=ymax, dash="dash", color="#d62728")

    # Wedge shading (DWL between Q_soc and Q_priv, inside PMB/PMC)
    if show_dwl and q_priv == q_priv and q_soc == q_soc and q_priv > q_soc:
        add_wedge(fig, S_private, D, q_soc, q_priv, name="DWL (under-taxed)", color="rgba(214, 39, 40, 0.22)")

    # Equilibria markers
    from math import isnan
    if not (isnan(q_priv) or isnan(p_priv)):
        add_point(fig, q_priv, p_priv, "(Q_private, P_private)")
        fig.add_shape(type="line", x0=q_priv, y0=0, x1=q_priv, y1=p_priv, line=dict(dash="dot", width=1))
        fig.add_shape(type="line", x0=0, y0=p_priv, x1=q_priv, y1=p_priv, line=dict(dash="dot", width=1))
    if show_msc and not (isnan(q_soc) or isnan(p_soc)):
        add_point(fig, q_soc, p_soc, "(Q_social, P_social)")
        fig.add_shape(type="line", x0=q_soc, y0=0, x1=q_soc, y1=p_soc, line=dict(dash="dot", width=1, color="#d62728"))
        fig.add_shape(type="line", x0=0, y0=p_soc, x1=q_soc, y1=p_soc, line=dict(dash="dot", width=1, color="#d62728"))

    # Pigouvian tax at Q_social
    tax_needed = max(0.0, line_y(S_social, q_soc) - line_y(S_private, q_soc)) if (show_msc and not isnan(q_soc)) else float("nan")

    st.plotly_chart(fig, use_container_width=True)

    c1, c2, c3 = st.columns(3)
    with c1:
        st.metric("Q_private, P_private", f"{q_priv:.2f}, {p_priv:.2f}")
    with c2:
        st.metric("Q_social, P_social", f"{q_soc:.2f}, {p_soc:.2f}")
    with c3:
        st.metric("Pigouvian tax (per unit)", f"{tax_needed:.2f}" if tax_needed == tax_needed else "—")

    st.markdown("""
- Private outcome: Demand (PMB) intersects Supply (PMC).
- Socially efficient outcome: Demand (PMB) intersects MSC = PMC + external cost.
- DWL shown between PMB and PMC from Q_social to Q_private (overproduction).
- A Pigouvian tax equal to the external cost per unit at Q_social shifts the market to the efficient quantity and removes the DWL wedge.
    """)
