import streamlit as st

from apps.common import line_y
from apps.market_common import (
    add_dwl,
    add_guides,
    add_market_lines,
    add_price_line,
    add_surplus_areas,
    equilibrium,
    is_valid_point,
    market_figure,
    market_inputs,
    quantity_at_price,
)


def app():
    st.subheader("Government Intervention: Price Floor")
    params = st.session_state.get("selected_model_params", {})
    if params.get("worksheet_note"):
        st.info(params["worksheet_note"])

    xmax, ymax, demand, supply = market_inputs("floor")
    q_eq, p_eq = equilibrium(demand, supply)
    default_floor = max(p_eq + 8.0, 1.0) if is_valid_point(q_eq, p_eq) else 45.0
    floor_price = st.sidebar.slider("Price floor", 0.0, float(ymax), float(min(params.get("price_floor", default_floor), ymax)), 1.0)

    c1, c2, c3 = st.columns(3)
    show_surplus = c1.toggle("Show CS and PS", value=True, key="floor_surplus")
    show_dwl = c2.toggle("Show DWL", value=True, key="floor_dwl")
    show_analysis = c3.toggle("Full analysis", value=False, key="floor_analysis")

    qs = max(0.0, quantity_at_price(supply, floor_price))
    qd = max(0.0, quantity_at_price(demand, floor_price))
    binding = is_valid_point(q_eq, p_eq) and floor_price > p_eq
    q_traded = min(qs, qd) if binding else q_eq
    market_price = floor_price if binding else p_eq
    excess_supply = max(qs - qd, 0.0) if binding else 0.0

    fig = market_figure(xmax, ymax)
    if show_surplus:
        add_surplus_areas(fig, demand, supply, q_traded, market_price)
    dwl = add_dwl(fig, demand, supply, q_traded, q_eq) if show_dwl and binding else 0.0
    add_market_lines(fig, demand, supply, xmax, ymax)
    add_price_line(fig, floor_price, xmax, "Floor")
    if is_valid_point(q_eq, p_eq):
        add_guides(fig, q_eq, p_eq, "Equilibrium")
    if binding:
        fig.add_shape(type="line", x0=qd, y0=0, x1=qd, y1=floor_price, line=dict(dash="dot", width=1))
        fig.add_shape(type="line", x0=qs, y0=0, x1=qs, y1=floor_price, line=dict(dash="dot", width=1))
        fig.add_annotation(x=qd, y=floor_price, text=f"Qd={qd:.1f}", showarrow=False, yshift=16)
        fig.add_annotation(x=qs, y=floor_price, text=f"Qs={qs:.1f}", showarrow=False, yshift=16)

    st.plotly_chart(fig, use_container_width=True, key="price_floor_chart")

    a, b, c, d = st.columns(4)
    a.metric("Binding?", "Yes" if binding else "No")
    b.metric("Quantity traded", f"{q_traded:.2f}")
    c.metric("Surplus", f"{excess_supply:.2f}")
    d.metric("DWL", f"{dwl:.2f}")

    if show_analysis:
        st.markdown(
            f"""
**Analysis**

Equilibrium is Q = {q_eq:.2f}, P = {p_eq:.2f}. At the floor price, quantity supplied is {qs:.2f} and quantity demanded is {qd:.2f}.

Because a binding floor sits above equilibrium, sellers want to supply more than buyers want to purchase. Actual trade is limited by the short side of the market, so Q traded = {q_traded:.2f}. The lost gains from mutually beneficial trades are the DWL wedge between demand and supply from Q traded to Q equilibrium.
"""
        )
        st.latex(r"P_D(Q)=\alpha_D+\beta_DQ,\quad P_S(Q)=\alpha_S+\beta_SQ")
        st.latex(r"\text{DWL}=\frac{1}{2}\left[P_D(Q_T)-P_S(Q_T)\right]\left(Q^*-Q_T\right)")
