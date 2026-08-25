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
    st.subheader("Externalities and Pigouvian Policy")
    st.info(
        "Use the Module 12 worksheet logic to compare private market outcomes with social optima. "
        "Switch between positive externalities, which need subsidies, and negative externalities, "
        "which need taxes or equivalent carbon-pricing policies."
    )

    policy_case = st.sidebar.selectbox(
        "Policy case",
        ["Positive externality: subsidy", "Negative externality: tax"],
    )
    positive_externality = policy_case.startswith("Positive")

    # Axes
    xmax = st.sidebar.number_input("Max Q", 10, 1000, 25, 1)
    ymax = st.sidebar.number_input("Max benefit/cost", 10, 1000, 130, 5)
    xmin, ymin = 0.0, 0.0

    st.sidebar.markdown("**Demand / Private Marginal Benefit (PMB)**")
    ad = st.sidebar.number_input("PMB intercept", value=100.0, step=1.0)
    bd_mag = st.sidebar.number_input("PMB slope magnitude", value=5.0, step=0.5, min_value=0.0)
    bd = -abs(bd_mag)

    st.sidebar.markdown("**Private Marginal Cost (PMC)**")
    as_ = st.sidebar.number_input("PMC intercept", value=10.0, step=1.0)
    bs = st.sidebar.number_input("PMC slope", value=2.0, step=0.5, min_value=0.0)

    external_value = st.sidebar.number_input(
        "External benefit/cost per unit",
        value=20.0,
        step=1.0,
        min_value=0.0,
        help="For a positive externality this shifts SMB above PMB. For a negative externality this shifts SMC above PMC.",
    )

    c1, c2, c3 = st.columns(3)
    with c1:
        show_social_curve = st.toggle("Show social curve", value=True)
    with c2:
        show_dwl = st.toggle("Show DWL wedge", value=True)
    with c3:
        show_policy = st.toggle("Show tax/subsidy marker", value=True)

    D_private = Line(ad, bd)
    D_social = Line(ad + external_value, bd)
    S = Line(as_, bs)
    S_social = Line(as_ + external_value, bs)

    if positive_externality:
        q_priv, p_priv = intersect(D_private, S)
        q_soc, p_soc = intersect(D_social, S)
        private_line = D_private
        social_line = D_social
        policy_label = "Subsidy"
        quantity_gap_label = "Underprovision"
        dwl_name = "DWL from under-provision"
    else:
        q_priv, p_priv = intersect(D_private, S)
        q_soc, p_soc = intersect(D_private, S_social)
        private_line = S
        social_line = S_social
        policy_label = "Tax"
        quantity_gap_label = "Overproduction"
        dwl_name = "DWL from over-production"

    # Figure
    fig = base_fig(xmax=xmax, ymax=ymax, x_title="Quantity", y_title="Marginal benefit / cost")
    fig.update_xaxes(range=[xmin, xmax])
    fig.update_yaxes(range=[ymin, ymax])

    # Lines
    add_full_span_line(fig, ad, bd, name="PMB / Demand", xmin=xmin, xmax=xmax, ymin=ymin, ymax=ymax, color="#1f77b4")
    add_full_span_line(fig, as_, bs, name="PMC = private supply", xmin=xmin, xmax=xmax, ymin=ymin, ymax=ymax, color="#ff7f0e")
    if show_social_curve and positive_externality:
        add_full_span_line(fig, ad + external_value, bd, name="SMB = PMB + external benefit", xmin=xmin, xmax=xmax, ymin=ymin, ymax=ymax, dash="dash", color="#2ca02c")
    elif show_social_curve:
        add_full_span_line(fig, as_ + external_value, bs, name="SMC = PMC + external cost", xmin=xmin, xmax=xmax, ymin=ymin, ymax=ymax, dash="dash", color="#d62728")

    # Wedge shading: lost social surplus from under-provision.
    if show_dwl and q_soc == q_soc and q_priv == q_priv:
        if positive_externality and q_soc > q_priv:
            add_wedge(fig, S, D_social, q_priv, q_soc, name=dwl_name, color="rgba(44, 160, 44, 0.22)")
        elif not positive_externality and q_priv > q_soc:
            add_wedge(fig, D_private, S_social, q_soc, q_priv, name=dwl_name, color="rgba(214, 39, 40, 0.20)")

    # Equilibria markers
    from math import isnan
    if not (isnan(q_priv) or isnan(p_priv)):
        add_point(fig, q_priv, p_priv, "(Q_private, P_private)")
        fig.add_shape(type="line", x0=q_priv, y0=0, x1=q_priv, y1=p_priv, line=dict(dash="dot", width=1))
        fig.add_shape(type="line", x0=0, y0=p_priv, x1=q_priv, y1=p_priv, line=dict(dash="dot", width=1))
    if show_social_curve and not (isnan(q_soc) or isnan(p_soc)):
        add_point(fig, q_soc, p_soc, "(Q_social, P_social)")
        fig.add_shape(type="line", x0=q_soc, y0=0, x1=q_soc, y1=p_soc, line=dict(dash="dot", width=1, color="#2ca02c"))
        fig.add_shape(type="line", x0=0, y0=p_soc, x1=q_soc, y1=p_soc, line=dict(dash="dot", width=1, color="#2ca02c"))

    policy_needed = max(0.0, line_y(social_line, q_soc) - line_y(private_line, q_soc)) if not isnan(q_soc) else float("nan")
    total_policy_value = policy_needed * q_soc if policy_needed == policy_needed and not isnan(q_soc) else float("nan")
    quantity_gap = abs(q_soc - q_priv) if not (isnan(q_soc) or isnan(q_priv)) else float("nan")
    if positive_externality:
        dwl_height = max(0.0, line_y(D_social, q_priv) - line_y(S, q_priv)) if not isnan(q_priv) else float("nan")
    else:
        dwl_height = max(0.0, line_y(S_social, q_priv) - line_y(D_private, q_priv)) if not isnan(q_priv) else float("nan")
    dwl = 0.5 * quantity_gap * dwl_height if quantity_gap == quantity_gap and dwl_height == dwl_height else float("nan")

    if show_policy and policy_needed == policy_needed:
        y_private = line_y(private_line, q_soc)
        y_social = line_y(social_line, q_soc)
        fig.add_shape(type="line", x0=q_soc, y0=y_private, x1=q_soc, y1=y_social, line=dict(width=3, color="#B38210"))
        fig.add_annotation(x=q_soc, y=(y_private + y_social) / 2, text=f"{policy_label.lower()} = {policy_needed:.2f}", showarrow=False, xshift=52)

    st.plotly_chart(fig, use_container_width=True)

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.metric("Market Q, P", f"{q_priv:.2f}, {p_priv:.2f}")
    with c2:
        st.metric("Social Q, P", f"{q_soc:.2f}, {p_soc:.2f}")
    with c3:
        st.metric(quantity_gap_label, f"{quantity_gap:.2f}" if quantity_gap == quantity_gap else "—")
    with c4:
        st.metric(f"{policy_label} per unit", f"{policy_needed:.2f}" if policy_needed == policy_needed else "—")

    st.metric("Estimated total policy value", f"{total_policy_value:.2f}" if total_policy_value == total_policy_value else "—")
    st.metric("Deadweight loss", f"{dwl:.2f}" if dwl == dwl else "—")

    st.markdown("""
- Market equilibrium: **PMB = PMC**.
- Positive externality social optimum: **SMB = PMC**, corrected with a subsidy.
- Negative externality social optimum: **PMB = SMC**, corrected with a tax or equivalent carbon price.
- Corrective policy per unit: the vertical gap between social and private value/cost at the social optimum.
    """)

    if st.toggle("Show algebra check", value=True):
        st.latex(r"PMB = a - bQ")
        st.latex(r"PMC = c + dQ")
        st.latex(r"SMB = PMB + ExternalBenefit")
        st.latex(r"SMC = PMC + ExternalCost")
        st.latex(r"Market: PMB = PMC")
        st.latex(r"Social\\ optimum: SMB = PMC\\ \\text{or}\\ PMB = SMC")
