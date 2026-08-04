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
    st.subheader("Consumer Surplus and Producer Surplus")

    xmax, ymax, demand, supply = market_inputs("surplus")
    q_eq, p_eq = equilibrium(demand, supply)

    c1, c2, c3 = st.columns(3)
    show_cs = c1.toggle("Show consumer surplus", value=True, key="surplus_cs")
    show_ps = c2.toggle("Show producer surplus", value=True, key="surplus_ps")
    use_price = c3.toggle("Set a market price", value=False, key="surplus_price_toggle")

    if use_price:
        price = st.slider("Market price", 0.0, float(ymax), float(p_eq if is_valid_point(q_eq, p_eq) else ymax * 0.45), 1.0)
        qd = max(0.0, quantity_at_price(demand, price))
        qs = max(0.0, quantity_at_price(supply, price))
        q_traded = min(qd, qs)
        binding_gap = abs(qd - qs)
    else:
        price = p_eq
        q_traded = q_eq
        qd = qs = q_eq
        binding_gap = 0.0

    fig = market_figure(xmax, ymax)
    cs, ps = add_surplus_areas(fig, demand, supply, q_traded, price, show_cs=show_cs, show_ps=show_ps)
    dwl = add_dwl(fig, demand, supply, q_traded, q_eq) if use_price and is_valid_point(q_eq, p_eq) else 0.0
    add_market_lines(fig, demand, supply, xmax, ymax)
    if use_price:
        add_price_line(fig, price, xmax, "Market price")
    if is_valid_point(q_eq, p_eq):
        add_guides(fig, q_eq, p_eq, "Equilibrium")

    st.plotly_chart(fig, use_container_width=True, key="surplus_chart")

    a, b, c, d = st.columns(4)
    a.metric("Consumer surplus", f"{cs:.2f}")
    b.metric("Producer surplus", f"{ps:.2f}")
    c.metric("Total surplus", f"{cs + ps:.2f}")
    d.metric("DWL", f"{dwl:.2f}")

    if use_price:
        st.caption(f"At this price, Qd = {qd:.2f}, Qs = {qs:.2f}, and the market gap is {binding_gap:.2f}.")

    if st.toggle("Full analysis", value=False, key="surplus_analysis"):
        st.markdown(
            """
Consumer surplus is the area below demand and above the transaction price. Producer surplus is the area above supply and below the transaction price. At competitive equilibrium, total surplus is maximized because all units whose willingness to pay exceeds marginal cost are traded.
"""
        )
        st.latex(r"CS=\frac{1}{2}(P_{max}-P)Q,\quad PS=\frac{1}{2}(P-P_{min})Q")
        st.latex(r"TS=CS+PS")
