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
    st.subheader("Externality: Social Benefit (Pigouvian Subsidy)")
    st.info("Model a positive externality: private benefit vs. social benefit, with Pigouvian subsidy and DWL.")

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

    ext_benefit = st.sidebar.number_input("External benefit per unit (Pigouvian subsidy target)", value=10.0, step=1.0, min_value=0.0)

    c1, c2, c3 = st.columns(3)
    with c1:
        show_smb = st.toggle("Show SMB (social benefit)", value=False)
    with c2:
        show_dwl = st.toggle("Show DWL wedge", value=False)
    with c3:
        show_subsidy = st.toggle("Show Pigouvian subsidy marker", value=True)

    D_private = Line(ad, bd)
    D_social = Line(ad + ext_benefit, bd)  # vertical shift up
    S = Line(as_, bs)

    q_priv, p_priv = intersect(D_private, S)
    q_soc, p_soc = intersect(D_social, S)

    # Figure
    fig = base_fig(xmax=xmax, ymax=ymax, x_title="Quantity (Q)", y_title="Price (P)")
    fig.update_xaxes(range=[xmin, xmax])
    fig.update_yaxes(range=[ymin, ymax])

    # Lines
    add_full_span_line(fig, ad, bd, name="Demand (PMB)", xmin=xmin, xmax=xmax, ymin=ymin, ymax=ymax, color="#1f77b4")
    if show_smb:
        add_full_span_line(fig, ad + ext_benefit, bd, name="Social Benefit (SMB)", xmin=xmin, xmax=xmax, ymin=ymin, ymax=ymax, dash="dash", color="#2ca02c")
    add_full_span_line(fig, as_, bs, name="Supply (PMC)", xmin=xmin, xmax=xmax, ymin=ymin, ymax=ymax, color="#ff7f0e")

    # Wedge shading (DWL between Q_priv and Q_soc, inside PMB/PMC)
    if show_dwl and q_soc == q_soc and q_priv == q_priv and q_soc > q_priv:
        add_wedge(fig, S, D_private, q_priv, q_soc, name="DWL (under-provided)", color="rgba(44, 160, 44, 0.22)")

    # Equilibria markers
    from math import isnan
    if not (isnan(q_priv) or isnan(p_priv)):
        add_point(fig, q_priv, p_priv, "(Q_private, P_private)")
        fig.add_shape(type="line", x0=q_priv, y0=0, x1=q_priv, y1=p_priv, line=dict(dash="dot", width=1))
        fig.add_shape(type="line", x0=0, y0=p_priv, x1=q_priv, y1=p_priv, line=dict(dash="dot", width=1))
    if show_smb and not (isnan(q_soc) or isnan(p_soc)):
        add_point(fig, q_soc, p_soc, "(Q_social, P_social)")
        fig.add_shape(type="line", x0=q_soc, y0=0, x1=q_soc, y1=p_soc, line=dict(dash="dot", width=1, color="#2ca02c"))
        fig.add_shape(type="line", x0=0, y0=p_soc, x1=q_soc, y1=p_soc, line=dict(dash="dot", width=1, color="#2ca02c"))

    # Pigouvian subsidy at Q_social
    subsidy_needed = max(0.0, line_y(D_social, q_soc) - line_y(D_private, q_soc)) if (show_smb and not isnan(q_soc)) else float("nan")

    st.plotly_chart(fig, use_container_width=True)

    c1, c2, c3 = st.columns(3)
    with c1:
        st.metric("Q_private, P_private", f"{q_priv:.2f}, {p_priv:.2f}")
    with c2:
        st.metric("Q_social, P_social", f"{q_soc:.2f}, {p_soc:.2f}")
    with c3:
        st.metric("Pigouvian subsidy (per unit)", f"{subsidy_needed:.2f}" if subsidy_needed == subsidy_needed else "—")

    st.markdown("""
- Private outcome: Demand (PMB) intersects Supply (PMC).
- Socially efficient outcome: SMB = PMB + external benefit intersects Supply.
- DWL shown between PMB and PMC from Q_private to Q_social (underproduction).
- A Pigouvian subsidy equal to the external benefit per unit at Q_social shifts the market to the efficient quantity and removes the DWL wedge.
    """)
