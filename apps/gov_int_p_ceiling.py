import streamlit as st

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
    st.subheader("Government Intervention: Price Ceiling")

    xmax, ymax, demand, supply = market_inputs("ceiling")
    q_eq, p_eq = equilibrium(demand, supply)
    default_ceiling = max(p_eq - 8.0, 0.0) if is_valid_point(q_eq, p_eq) else 25.0
    ceiling_price = st.sidebar.slider("Price ceiling", 0.0, float(ymax), float(min(default_ceiling, ymax)), 1.0)

    c1, c2, c3 = st.columns(3)
    show_surplus = c1.toggle("Show CS and PS", value=True, key="ceiling_surplus")
    show_dwl = c2.toggle("Show DWL", value=True, key="ceiling_dwl")
    show_analysis = c3.toggle("Full analysis", value=False, key="ceiling_analysis")

    qs = max(0.0, quantity_at_price(supply, ceiling_price))
    qd = max(0.0, quantity_at_price(demand, ceiling_price))
    binding = is_valid_point(q_eq, p_eq) and ceiling_price < p_eq
    q_traded = min(qs, qd) if binding else q_eq
    market_price = ceiling_price if binding else p_eq
    shortage = max(qd - qs, 0.0) if binding else 0.0

    fig = market_figure(xmax, ymax)
    if show_surplus:
        add_surplus_areas(fig, demand, supply, q_traded, market_price)
    dwl = add_dwl(fig, demand, supply, q_traded, q_eq) if show_dwl and binding else 0.0
    add_market_lines(fig, demand, supply, xmax, ymax)
    add_price_line(fig, ceiling_price, xmax, "Ceiling")
    if is_valid_point(q_eq, p_eq):
        add_guides(fig, q_eq, p_eq, "Equilibrium")
    if binding:
        fig.add_shape(type="line", x0=qs, y0=0, x1=qs, y1=ceiling_price, line=dict(dash="dot", width=1))
        fig.add_shape(type="line", x0=qd, y0=0, x1=qd, y1=ceiling_price, line=dict(dash="dot", width=1))
        fig.add_annotation(x=qs, y=ceiling_price, text=f"Qs={qs:.1f}", showarrow=False, yshift=16)
        fig.add_annotation(x=qd, y=ceiling_price, text=f"Qd={qd:.1f}", showarrow=False, yshift=16)

    st.plotly_chart(fig, use_container_width=True, key="price_ceiling_chart")

    a, b, c, d = st.columns(4)
    a.metric("Binding?", "Yes" if binding else "No")
    b.metric("Quantity traded", f"{q_traded:.2f}")
    c.metric("Shortage", f"{shortage:.2f}")
    d.metric("DWL", f"{dwl:.2f}")

    if show_analysis:
        st.markdown(
            f"""
**Analysis**

Equilibrium is Q = {q_eq:.2f}, P = {p_eq:.2f}. At the ceiling price, quantity supplied is {qs:.2f} and quantity demanded is {qd:.2f}.

Because a binding ceiling sits below equilibrium, buyers want more than sellers provide. Actual trade is limited by the short side of the market, so Q traded = {q_traded:.2f}. The DWL wedge measures the value of trades that would have happened at equilibrium but are blocked by the ceiling.
"""
        )
        st.latex(r"P_D(Q)=\alpha_D+\beta_DQ,\quad P_S(Q)=\alpha_S+\beta_SQ")
        st.latex(r"\text{DWL}=\frac{1}{2}\left[P_D(Q_T)-P_S(Q_T)\right]\left(Q^*-Q_T\right)")
