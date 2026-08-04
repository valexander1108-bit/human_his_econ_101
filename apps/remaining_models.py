import math

import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from apps.common import apply_grid


GREEN = "#1d511e"
GOLD = "#C49A6C"
SAGE = "#6C7A61"
BROWN = "#563b19"
POINT = "#B38210"
BLUE = "#33658A"
RED = "#B23F35"


def styled(fig, height=540):
    fig.update_layout(
        height=height,
        margin=dict(l=40, r=20, t=30, b=40),
        legend=dict(orientation="h", y=1.08, x=0),
        plot_bgcolor="white",
        paper_bgcolor="white",
    )
    apply_grid(fig)
    return fig


def cost_values(q, fc, vc_base, vc_slope, vc_curve):
    q = np.asarray(q)
    vc = vc_base * q + vc_slope * q**2 + vc_curve * q**3
    tc = fc + vc
    afc = fc / np.maximum(q, 1e-9)
    avc = vc / np.maximum(q, 1e-9)
    atc = tc / np.maximum(q, 1e-9)
    mc = vc_base + 2 * vc_slope * q + 3 * vc_curve * q**2
    return vc, tc, afc, avc, atc, mc


def capitalism_climate_app():
    st.subheader("Capitalism and Climate Change: A Micro Externality Model")
    demand_intercept = st.sidebar.slider("Willingness-to-pay intercept", 20.0, 200.0, 110.0, 5.0)
    demand_slope = st.sidebar.slider("Demand slope", 0.10, 2.00, 0.55, 0.05)
    private_cost = st.sidebar.slider("Private marginal cost intercept", 0.0, 100.0, 20.0, 2.0)
    cost_slope = st.sidebar.slider("Private marginal cost slope", 0.05, 2.00, 0.35, 0.05)
    emissions_intensity = st.sidebar.slider("Emissions per unit", 0.10, 3.00, 1.00, 0.05)
    climate_damage = st.sidebar.slider("Marginal climate damage per emission unit", 0.0, 50.0, 18.0, 1.0)
    carbon_price = st.sidebar.slider("Carbon price / emissions fee", 0.0, 100.0, 15.0, 1.0)

    q = np.linspace(0, 160, 400)
    demand = demand_intercept - demand_slope * q
    mpc = private_cost + cost_slope * q
    external_cost = emissions_intensity * climate_damage
    msc = mpc + external_cost
    taxed_mpc = mpc + carbon_price * emissions_intensity

    q_private = (demand_intercept - private_cost) / (demand_slope + cost_slope)
    q_social = (demand_intercept - private_cost - external_cost) / (demand_slope + cost_slope)
    q_policy = (demand_intercept - private_cost - carbon_price * emissions_intensity) / (demand_slope + cost_slope)
    q_private = max(q_private, 0)
    q_social = max(q_social, 0)
    q_policy = max(q_policy, 0)
    dwl = 0.5 * max(q_private - q_social, 0) * external_cost

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=q[demand >= 0], y=demand[demand >= 0], name="Demand / marginal benefit", line=dict(width=3, color=GREEN)))
    fig.add_trace(go.Scatter(x=q, y=mpc, name="MPC", line=dict(width=3, color=GOLD)))
    fig.add_trace(go.Scatter(x=q, y=msc, name="MSC = MPC + climate damage", line=dict(width=3, color=RED, dash="dash")))
    fig.add_trace(go.Scatter(x=q, y=taxed_mpc, name="Private cost with carbon price", line=dict(width=3, color=BLUE, dash="dot")))
    for x0, label, color in [(q_private, "private", POINT), (q_social, "efficient", RED), (q_policy, "policy", BLUE)]:
        y0 = demand_intercept - demand_slope * x0
        fig.add_trace(go.Scatter(x=[x0], y=[y0], mode="markers+text", text=[label], textposition="top center", marker=dict(size=12, color=color), name=label.title()))
    fig.update_xaxes(title="Carbon-intensive output")
    fig.update_yaxes(title="Marginal benefit / cost")
    st.plotly_chart(styled(fig), use_container_width=True, key="capitalism_climate")

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Private Q", f"{q_private:.1f}")
    c2.metric("Efficient Q", f"{q_social:.1f}")
    c3.metric("Policy Q", f"{q_policy:.1f}")
    c4.metric("DWL without policy", f"{dwl:.1f}")
    if st.toggle("Full analysis", value=False, key="climate_analysis"):
        st.markdown(
            "This is the microeconomics of climate change: the private market ignores damages imposed on others, so the private outcome overproduces carbon-intensive output. A carbon price works by moving the private marginal cost closer to the social marginal cost."
        )
        st.latex(r"MSC = MPC + \text{marginal climate damage}")
        st.latex(r"\text{efficient quantity: } MB = MSC")


def capitalism_inequality_app():
    st.subheader("Capitalism and Global Inequality")
    n = 100
    capital_share = st.sidebar.slider("Capital income share", 0.10, 0.60, 0.35, 0.05)
    skill_premium = st.sidebar.slider("Skill premium", 1.0, 5.0, 2.2, 0.1)
    globalization = st.sidebar.slider("Global integration", 0.0, 1.0, 0.55, 0.05)
    redistribution = st.sidebar.slider("Redistribution strength", 0.0, 0.6, 0.20, 0.05)

    people = np.linspace(0.01, 1, n)
    market_income = (people ** (1.9 + globalization)) * (1 + capital_share * 3) + (people > 0.75) * skill_premium
    market_income = market_income / market_income.sum()
    equal_share = np.ones(n) / n
    post_income = (1 - redistribution) * market_income + redistribution * equal_share
    lorenz_market = np.r_[0, np.cumsum(np.sort(market_income))]
    lorenz_post = np.r_[0, np.cumsum(np.sort(post_income))]
    pop = np.linspace(0, 1, n + 1)
    gini_market = 1 - 2 * np.trapz(lorenz_market, pop)
    gini_post = 1 - 2 * np.trapz(lorenz_post, pop)

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=pop, y=pop, name="Perfect equality", line=dict(dash="dash", color=SAGE)))
    fig.add_trace(go.Scatter(x=pop, y=lorenz_market, name="Market income", line=dict(width=3, color=RED)))
    fig.add_trace(go.Scatter(x=pop, y=lorenz_post, name="After redistribution", line=dict(width=3, color=GREEN)))
    fig.update_xaxes(title="Cumulative population")
    fig.update_yaxes(title="Cumulative income")
    st.plotly_chart(styled(fig), use_container_width=True, key="capitalism_inequality")
    c1, c2 = st.columns(2)
    c1.metric("Market Gini", f"{gini_market:.2f}")
    c2.metric("Post-policy Gini", f"{gini_post:.2f}")
    if st.toggle("Full analysis", value=False, key="ineq_analysis"):
        st.markdown("The Lorenz curve shows how income is distributed across the population. Capital ownership, skill premia, and global integration can pull income toward the top; redistribution and public investment can partially offset that pattern.")


def cost_production_app():
    st.subheader("Cost of Production: Average vs Marginal Rates")
    fc = st.sidebar.slider("Fixed cost", 0.0, 500.0, 120.0, 10.0)
    vc_base = st.sidebar.slider("Base variable cost", 0.0, 30.0, 8.0, 0.5)
    vc_slope = st.sidebar.slider("Rising VC slope", 0.0, 3.0, 0.55, 0.05)
    vc_curve = st.sidebar.slider("Capacity pressure", 0.000, 0.080, 0.010, 0.002)
    price = st.sidebar.slider("Market price / MR", 1.0, 200.0, 65.0, 1.0)
    q = np.linspace(1, 100, 300)
    vc, tc, afc, avc, atc, mc = cost_values(q, fc, vc_base, vc_slope, vc_curve)
    tr = price * q
    mr = np.full_like(q, price)
    atr = tr / q

    tab1, tab2 = st.tabs(["Totals", "Average and marginal"])
    with tab1:
        fig = go.Figure()
        for y, name, color in [(tr, "TR", GREEN), (tc, "TC", RED), (np.full_like(q, fc), "FC", BROWN), (vc, "VC", BLUE)]:
            fig.add_trace(go.Scatter(x=q, y=y, name=name, line=dict(width=3, color=color)))
        fig.update_xaxes(title="Output Q")
        fig.update_yaxes(title="Dollars")
        st.plotly_chart(styled(fig), use_container_width=True, key="cost_totals")
    with tab2:
        fig = go.Figure()
        for y, name, color in [(afc, "AFC", BROWN), (avc, "AVC", BLUE), (atc, "ATC", RED), (atr, "ATR", SAGE), (mr, "MR", GOLD), (mc, "MC as supply", GREEN)]:
            fig.add_trace(go.Scatter(x=q, y=y, name=name, line=dict(width=3, color=color)))
        fig.update_xaxes(title="Output Q")
        fig.update_yaxes(title="Dollars per unit")
        st.plotly_chart(styled(fig), use_container_width=True, key="cost_rates")
    if st.toggle("Full analysis", value=False, key="cost_analysis"):
        st.markdown("Average rates divide a total by output: AFC, AVC, and ATC. Marginal rates measure the extra amount from one more unit: MR and MC. In perfect competition, the firm's supply curve is the MC curve above minimum AVC.")
        st.latex(r"ATC=TC/Q,\quad AVC=VC/Q,\quad AFC=FC/Q,\quad MC=\Delta TC/\Delta Q")


def pc_profit_app():
    st.subheader("Perfect Competition: Profit Maximization")
    fc = st.sidebar.slider("Fixed cost", 0.0, 500.0, 120.0, 10.0, key="pc_fc")
    price = st.sidebar.slider("Market price", 1.0, 200.0, 70.0, 1.0, key="pc_p")
    q = np.linspace(1, 100, 500)
    vc, tc, afc, avc, atc, mc = cost_values(q, fc, 8.0, 0.55, 0.010)
    q_star = q[np.argmin(np.abs(mc - price))]
    atc_star = np.interp(q_star, q, atc)
    profit = (price - atc_star) * q_star
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=q, y=mc, name="MC", line=dict(width=3, color=GREEN)))
    fig.add_trace(go.Scatter(x=q, y=atc, name="ATC", line=dict(width=3, color=RED)))
    fig.add_trace(go.Scatter(x=q, y=np.full_like(q, price), name="MR = P", line=dict(width=3, color=GOLD)))
    fig.add_trace(go.Scatter(x=[q_star], y=[price], mode="markers+text", name="MR = MC", text=["MR=MC"], textposition="top center", marker=dict(size=12, color=POINT)))
    fig.update_xaxes(title="Output Q")
    fig.update_yaxes(title="Dollars per unit")
    st.plotly_chart(styled(fig), use_container_width=True, key="pc_profit")
    c1, c2, c3 = st.columns(3)
    c1.metric("Profit-max Q", f"{q_star:.2f}")
    c2.metric("Profit", f"{profit:.2f}")
    c3.metric("ATC at Q*", f"{atc_star:.2f}")
    if st.toggle("Full analysis", value=False, key="pc_analysis"):
        st.markdown("A perfectly competitive firm takes price as given, so price equals marginal revenue. The profit-maximizing rule is produce the quantity where MR = MC, provided price is high enough to avoid shutdown.")


def shutdown_app():
    st.subheader("Perfect Competition: Shutdown Point")
    price = st.sidebar.slider("Market price", 1.0, 120.0, 35.0, 1.0, key="sd_p")
    q = np.linspace(1, 100, 500)
    vc, tc, afc, avc, atc, mc = cost_values(q, 120.0, 8.0, 0.55, 0.010)
    min_avc = float(avc.min())
    produce = price >= min_avc
    q_star = q[np.argmin(np.abs(mc - price))] if produce else 0
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=q, y=avc, name="AVC", line=dict(width=3, color=BLUE)))
    fig.add_trace(go.Scatter(x=q, y=atc, name="ATC", line=dict(width=3, color=RED)))
    fig.add_trace(go.Scatter(x=q, y=mc, name="MC", line=dict(width=3, color=GREEN)))
    fig.add_trace(go.Scatter(x=q, y=np.full_like(q, price), name="P = MR", line=dict(width=3, color=GOLD)))
    fig.update_xaxes(title="Output Q")
    fig.update_yaxes(title="Dollars per unit")
    st.plotly_chart(styled(fig), use_container_width=True, key="shutdown")
    st.metric("Decision", "Produce" if produce else "Shut down", f"min AVC = {min_avc:.2f}")
    st.metric("Output", f"{q_star:.2f}")
    if st.toggle("Full analysis", value=False, key="shutdown_analysis"):
        st.markdown("In the short run, fixed costs are sunk. The firm produces if price covers average variable cost. If price is below minimum AVC, every unit adds to losses beyond fixed cost, so the firm shuts down.")


def long_run_exit_app():
    st.subheader("Long-Run Equilibrium and Firm Exit")
    demand = st.sidebar.slider("Market demand index", 50.0, 200.0, 110.0, 5.0)
    firms = st.sidebar.slider("Number of firms", 1, 100, 35, 1)
    min_atc = st.sidebar.slider("Minimum ATC", 10.0, 100.0, 42.0, 1.0)
    price = demand / math.sqrt(firms)
    profit_signal = price - min_atc
    entry_exit = "Entry pressure" if profit_signal > 3 else ("Exit pressure" if profit_signal < -3 else "Long-run equilibrium")
    fig = go.Figure()
    firm_counts = np.arange(1, 101)
    prices = demand / np.sqrt(firm_counts)
    fig.add_trace(go.Scatter(x=firm_counts, y=prices, name="Market price as firms enter", line=dict(width=3, color=GREEN)))
    fig.add_trace(go.Scatter(x=firm_counts, y=np.full_like(firm_counts, min_atc), name="min ATC", line=dict(width=3, color=RED)))
    fig.add_trace(go.Scatter(x=[firms], y=[price], mode="markers+text", text=[entry_exit], textposition="top center", marker=dict(size=12, color=POINT), name="Current"))
    fig.update_xaxes(title="Number of firms")
    fig.update_yaxes(title="Price")
    st.plotly_chart(styled(fig), use_container_width=True, key="long_run")
    st.metric("Current price", f"{price:.2f}", entry_exit)
    if st.toggle("Full analysis", value=False, key="lr_analysis"):
        st.markdown("In long-run perfect competition, economic profit attracts entry and losses cause exit. The process stops when price equals minimum ATC, so representative firms earn zero economic profit.")


def economies_scale_app():
    st.subheader("Economies of Scale")
    fixed = st.sidebar.slider("Fixed setup cost", 0.0, 1000.0, 350.0, 25.0)
    coordination = st.sidebar.slider("Coordination cost", 0.000, 0.200, 0.035, 0.005)
    learning = st.sidebar.slider("Learning-by-doing strength", 0.0, 20.0, 8.0, 0.5)
    q = np.linspace(1, 200, 500)
    lratc = fixed / q + 18 - learning * np.log(q) / np.log(200) + coordination * q
    mes_q = q[np.argmin(lratc)]
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=q, y=lratc, name="LRATC", line=dict(width=4, color=GREEN)))
    fig.add_trace(go.Scatter(x=[mes_q], y=[lratc.min()], mode="markers+text", text=["MES"], textposition="top center", marker=dict(size=12, color=POINT), name="Minimum efficient scale"))
    fig.update_xaxes(title="Scale of output")
    fig.update_yaxes(title="Long-run average total cost")
    st.plotly_chart(styled(fig), use_container_width=True, key="scale")
    st.metric("Minimum efficient scale", f"{mes_q:.1f}")
    if st.toggle("Full analysis", value=False, key="scale_analysis"):
        st.markdown("Economies of scale occur where LRATC falls as output expands. Diseconomies occur where coordination, complexity, or capacity costs make LRATC rise. Minimum efficient scale is the lowest-cost scale of production.")


def imperfect_competition_app():
    st.subheader("Monopoly and Monopolistic Competition: Profit Maximization")
    market = st.sidebar.radio("Market structure", ["Monopoly", "Monopolistic competition"], horizontal=True)
    a = st.sidebar.slider("Demand intercept", 20.0, 200.0, 120.0, 5.0)
    b = st.sidebar.slider("Demand slope", 0.2, 3.0, 1.0, 0.1)
    mc_base = st.sidebar.slider("MC intercept", 0.0, 80.0, 20.0, 1.0)
    mc_slope = st.sidebar.slider("MC slope", 0.0, 2.0, 0.45, 0.05)
    fixed = st.sidebar.slider("Fixed cost", 0.0, 600.0, 180.0, 10.0)
    q = np.linspace(1, min(120, a / b), 500)
    demand = a - b * q
    mr = a - 2 * b * q
    mc = mc_base + mc_slope * q
    atc = fixed / q + mc_base + 0.5 * mc_slope * q
    q_star = q[np.argmin(np.abs(mr - mc))]
    p_star = a - b * q_star
    atc_star = np.interp(q_star, q, atc)
    profit = (p_star - atc_star) * q_star
    if market == "Monopolistic competition":
        profit *= st.sidebar.slider("Product differentiation power", 0.0, 1.0, 0.55, 0.05)
    fig = go.Figure()
    for y, name, color in [(demand, "Demand", GREEN), (mr, "MR", GOLD), (mc, "MC", RED), (atc, "ATC", BLUE)]:
        fig.add_trace(go.Scatter(x=q, y=y, name=name, line=dict(width=3, color=color)))
    fig.add_trace(go.Scatter(x=[q_star], y=[p_star], mode="markers+text", text=["Profit max"], textposition="top center", marker=dict(size=12, color=POINT), name="Choice"))
    fig.update_xaxes(title="Output Q")
    fig.update_yaxes(title="Price / cost")
    st.plotly_chart(styled(fig), use_container_width=True, key="imperfect")
    st.metric("Profit-max rule", "MR = MC")
    st.metric("Estimated profit", f"{profit:.2f}")
    if st.toggle("Full analysis", value=False, key="imperfect_analysis"):
        st.markdown("Imperfect competitors face downward-sloping demand, so marginal revenue lies below demand. They choose Q where MR = MC, then charge the highest price consumers will pay on the demand curve.")


def game_theory_app():
    st.subheader("Game Theory: Types of Games")
    game = st.sidebar.selectbox("Game type", ["Prisoner's dilemma", "Coordination", "Chicken"])
    if game == "Prisoner's dilemma":
        matrix = pd.DataFrame({"Other Cooperates": ["3, 3", "5, 0"], "Other Defects": ["0, 5", "1, 1"]}, index=["Cooperate", "Defect"])
        lesson = "Dominant strategies can produce a collectively worse outcome."
    elif game == "Coordination":
        matrix = pd.DataFrame({"Left": ["4, 4", "0, 0"], "Right": ["0, 0", "3, 3"]}, index=["Left", "Right"])
        lesson = "Multiple equilibria can exist when players mainly need to coordinate."
    else:
        matrix = pd.DataFrame({"Swerve": ["2, 2", "1, 4"], "Straight": ["4, 1", "0, 0"]}, index=["Swerve", "Straight"])
        lesson = "Commitment and threats matter when each player wants the other to yield."
    st.dataframe(matrix, use_container_width=True)
    st.info(lesson)
    if st.toggle("Full analysis", value=False, key="game_analysis"):
        st.markdown("A Nash equilibrium occurs when each player is choosing a best response to the other player's strategy. Different games emphasize dominance, coordination, credibility, and repeated interaction.")


def types_goods_app():
    st.subheader("Types of Goods")
    rivalry = st.sidebar.slider("Rivalry", 0.0, 1.0, 0.50, 0.05)
    excludability = st.sidebar.slider("Excludability", 0.0, 1.0, 0.50, 0.05)
    if rivalry >= 0.5 and excludability >= 0.5:
        good = "Private good"
    elif rivalry < 0.5 and excludability >= 0.5:
        good = "Club good"
    elif rivalry >= 0.5 and excludability < 0.5:
        good = "Common resource"
    else:
        good = "Public good"
    fig = go.Figure()
    fig.add_shape(type="rect", x0=0, x1=.5, y0=0, y1=.5, fillcolor="rgba(51,101,138,.18)", line=dict(width=0))
    fig.add_shape(type="rect", x0=.5, x1=1, y0=0, y1=.5, fillcolor="rgba(108,122,97,.18)", line=dict(width=0))
    fig.add_shape(type="rect", x0=0, x1=.5, y0=.5, y1=1, fillcolor="rgba(196,154,108,.18)", line=dict(width=0))
    fig.add_shape(type="rect", x0=.5, x1=1, y0=.5, y1=1, fillcolor="rgba(178,63,53,.18)", line=dict(width=0))
    fig.add_trace(go.Scatter(x=[excludability], y=[rivalry], mode="markers+text", text=[good], textposition="top center", marker=dict(size=14, color=POINT), name="Good"))
    fig.update_xaxes(title="Excludability", range=[0, 1])
    fig.update_yaxes(title="Rivalry", range=[0, 1])
    st.plotly_chart(styled(fig), use_container_width=True, key="goods")
    st.metric("Classification", good)
    if st.toggle("Full analysis", value=False, key="goods_analysis"):
        st.markdown("Private goods are rival and excludable. Public goods are nonrival and nonexcludable. Common resources are rival but hard to exclude. Club goods are excludable but mostly nonrival until congestion.")


def externalities_combined_app():
    st.subheader("Externalities: Positive and Negative")
    kind = st.sidebar.radio("Externality type", ["Negative externality", "Positive externality"], horizontal=True)
    external_value = st.sidebar.slider("External value per unit", 0.0, 50.0, 15.0, 1.0)
    q = np.linspace(0, 120, 300)
    demand = 90 - 0.5 * q
    supply = 15 + 0.35 * q
    if kind == "Negative externality":
        social = supply + external_value
        label = "MSC"
    else:
        social = demand + external_value
        label = "SMB"
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=q, y=demand, name="PMB / Demand", line=dict(width=3, color=GREEN)))
    fig.add_trace(go.Scatter(x=q, y=supply, name="PMC / Supply", line=dict(width=3, color=GOLD)))
    fig.add_trace(go.Scatter(x=q, y=social, name=label, line=dict(width=3, dash="dash", color=RED if kind.startswith("Negative") else BLUE)))
    fig.update_xaxes(title="Quantity")
    fig.update_yaxes(title="Price / marginal value")
    st.plotly_chart(styled(fig), use_container_width=True, key="externalities_combined")
    st.info("Negative externalities create overproduction without policy. Positive externalities create underproduction without policy.")
    if st.toggle("Full analysis", value=False, key="externalities_combined_analysis"):
        st.markdown("Efficient policy aligns private incentives with social marginal costs or benefits: taxes for negative externalities, subsidies or public provision for positive externalities.")


def competition_fairness_app():
    st.subheader("Competition and Fairness")
    concentration = st.sidebar.slider("Market concentration", 0.0, 1.0, 0.45, 0.05)
    entry_barriers = st.sidebar.slider("Entry barriers", 0.0, 1.0, 0.35, 0.05)
    info_asymmetry = st.sidebar.slider("Information asymmetry", 0.0, 1.0, 0.30, 0.05)
    labor_power_gap = st.sidebar.slider("Labor bargaining gap", 0.0, 1.0, 0.40, 0.05)
    fairness_risk = 0.30 * concentration + 0.25 * entry_barriers + 0.20 * info_asymmetry + 0.25 * labor_power_gap
    categories = ["Concentration", "Entry barriers", "Information gaps", "Bargaining gap"]
    values = [concentration, entry_barriers, info_asymmetry, labor_power_gap]
    fig = go.Figure(go.Bar(x=categories, y=values, marker_color=[GREEN, GOLD, BLUE, RED]))
    fig.update_yaxes(range=[0, 1], title="Risk index")
    st.plotly_chart(styled(fig), use_container_width=True, key="fairness")
    st.metric("Fairness risk", f"{fairness_risk:.2f}", "higher means weaker competitive discipline")
    if st.toggle("Full analysis", value=False, key="fairness_analysis"):
        st.markdown("Competition can promote fairness by limiting market power, but outcomes can still be unfair when entry is blocked, information is unequal, or bargaining power is imbalanced. Policy choices define which forms of competition society treats as legitimate.")
