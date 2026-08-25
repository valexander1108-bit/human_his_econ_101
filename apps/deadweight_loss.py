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
    st.subheader("Deadweight Loss")
    params = st.session_state.get("selected_model_params", {})
    if params.get("worksheet_note"):
        st.info(params["worksheet_note"])

    xmax, ymax, demand, supply = market_inputs("dwl")
    q_eq, p_eq = equilibrium(demand, supply)
    policies = ["Per-unit tax", "Quantity restriction", "Price floor", "Price ceiling"]
    default_policy = params.get("policy", "Per-unit tax")
    policy = st.sidebar.selectbox("Policy source", policies, index=policies.index(default_policy) if default_policy in policies else 0)

    if policy == "Per-unit tax":
        tax = st.sidebar.slider("Tax per unit", 0.0, float(ymax), float(params.get("tax", 10.0)), 1.0)
        taxed_supply = type(supply)(supply.a + tax, supply.b)
        q_policy, buyer_price = equilibrium(demand, taxed_supply)
        seller_price = buyer_price - tax
        q_traded = max(0.0, q_policy)
        policy_price = buyer_price
    elif policy == "Quantity restriction":
        max_q = q_eq if is_valid_point(q_eq, p_eq) else xmax * 0.6
        q_traded = st.sidebar.slider("Allowed quantity", 0.0, float(xmax), float(params.get("quantity_restriction", max_q * 0.7)), 1.0)
        buyer_price = line_y(demand, q_traded)
        seller_price = line_y(supply, q_traded)
        policy_price = buyer_price
    elif policy == "Price floor":
        floor = st.sidebar.slider("Price floor", 0.0, float(ymax), float(min(params.get("price_floor", (p_eq if is_valid_point(q_eq, p_eq) else 35) + 8), ymax)), 1.0)
        q_traded = min(max(0.0, quantity_at_price(demand, floor)), max(0.0, quantity_at_price(supply, floor))) if floor > p_eq else q_eq
        buyer_price = seller_price = policy_price = floor if floor > p_eq else p_eq
    else:
        ceiling = st.sidebar.slider("Price ceiling", 0.0, float(ymax), float(max(params.get("price_ceiling", (p_eq if is_valid_point(q_eq, p_eq) else 35) - 8), 0)), 1.0)
        q_traded = min(max(0.0, quantity_at_price(demand, ceiling)), max(0.0, quantity_at_price(supply, ceiling))) if ceiling < p_eq else q_eq
        buyer_price = seller_price = policy_price = ceiling if ceiling < p_eq else p_eq

    c1, c2, c3 = st.columns(3)
    show_surplus = c1.toggle("Show realized CS and PS", value=False, key="dwl_surplus")
    show_wedge = c2.toggle("Show DWL wedge", value=True, key="dwl_wedge")
    show_analysis = c3.toggle("Full analysis", value=False, key="dwl_analysis")

    fig = market_figure(xmax, ymax)
    if show_surplus:
        add_surplus_areas(fig, demand, supply, q_traded, seller_price)
    dwl = add_dwl(fig, demand, supply, q_traded, q_eq) if show_wedge and is_valid_point(q_eq, p_eq) else 0.0
    add_market_lines(fig, demand, supply, xmax, ymax)
    if policy in ("Price floor", "Price ceiling"):
        add_price_line(fig, policy_price, xmax, policy)
    if policy == "Per-unit tax":
        fig.add_shape(type="line", x0=q_traded, y0=seller_price, x1=q_traded, y1=buyer_price, line=dict(width=3, color="#B38210"))
        fig.add_annotation(x=q_traded, y=(buyer_price + seller_price) / 2, text=f"tax={buyer_price - seller_price:.2f}", showarrow=False, xshift=42)
    if is_valid_point(q_eq, p_eq):
        add_guides(fig, q_eq, p_eq, "Equilibrium")
    if q_traded >= 0:
        fig.add_shape(type="line", x0=q_traded, y0=0, x1=q_traded, y1=max(buyer_price, seller_price), line=dict(dash="dot", width=1, color="#B38210"))
        fig.add_annotation(x=q_traded, y=0, text=f"Q_T={q_traded:.1f}", showarrow=False, yshift=-12)

    st.plotly_chart(fig, use_container_width=True, key="dwl_chart")

    a, b, c, d = st.columns(4)
    a.metric("Efficient Q", f"{q_eq:.2f}")
    b.metric("Traded Q", f"{q_traded:.2f}")
    c.metric("Buyer price", f"{buyer_price:.2f}")
    d.metric("DWL", f"{dwl:.2f}")

    if show_analysis:
        st.markdown(
            f"""
**Analysis**

Deadweight loss appears when the policy moves trade from the efficient quantity {q_eq:.2f} to {q_traded:.2f}. The vertical gap between demand and supply at the restricted quantity is the surplus still available from the next unit. The triangle aggregates those lost gains until the original equilibrium.
"""
        )
        st.latex(r"\text{DWL}=\frac{1}{2}\left[P_D(Q_T)-P_S(Q_T)\right]\left(Q^*-Q_T\right)")
