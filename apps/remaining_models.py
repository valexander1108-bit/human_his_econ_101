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
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
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


def production_function_mp_app():
    st.subheader("Production Function and Marginal Product")
    st.caption("Supports Module 2's production-function and diminishing marginal product worksheet prompt.")

    max_input = st.sidebar.slider("Maximum input units", 4, 20, 10, 1)
    productivity = st.sidebar.slider("Productivity scale", 0.5, 8.0, 3.0, 0.25)
    curvature = st.sidebar.slider("Diminishing-returns strength", 0.20, 0.95, 0.55, 0.05)

    labor = np.arange(0, max_input + 1)
    total_product = productivity * np.power(labor, curvature)
    total_product[0] = 0
    marginal_product = np.r_[np.nan, np.diff(total_product)]
    average_product = np.divide(total_product, labor, out=np.zeros_like(total_product), where=labor > 0)

    table = pd.DataFrame(
        {
            "Input": labor,
            "Total product": np.round(total_product, 2),
            "Marginal product": np.round(marginal_product, 2),
            "Average product": np.round(average_product, 2),
        }
    )
    st.dataframe(table, use_container_width=True, hide_index=True)

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=labor, y=total_product, name="Total product", line=dict(width=3, color=GREEN)))
    fig.add_trace(go.Bar(x=labor[1:], y=marginal_product[1:], name="Marginal product", marker_color=GOLD, yaxis="y2", opacity=0.65))
    fig.update_layout(yaxis=dict(title="Total product"), yaxis2=dict(title="Marginal product", overlaying="y", side="right"))
    fig.update_xaxes(title="Input units")
    st.plotly_chart(styled(fig), use_container_width=True, key="production_function_mp")

    if st.toggle("Full analysis", value=False, key="production_function_mp_analysis"):
        st.markdown(
            "A production function maps inputs into output. Marginal product is the extra output from one more input. "
            "Diminishing marginal product means total product can keep rising while each additional input adds less than the previous one."
        )
        st.latex(r"MP=\Delta TP/\Delta L")


def vmp_derived_demand_app():
    st.subheader("Derived Demand and VMP Hiring Rule")
    st.caption("Matches the Module 5 Florentine cloth merchant problem: VMP = output price x marginal product.")

    output_price = st.sidebar.slider("Price per unit of output", 1.0, 30.0, 8.0, 0.5)
    wage = st.sidebar.slider("Weekly wage", 1.0, 100.0, 24.0, 1.0)
    mp_values = [10, 8, 6, 3, 2]
    workers = np.arange(1, len(mp_values) + 1)
    vmp = output_price * np.array(mp_values)
    hire = vmp >= wage
    optimal_workers = int(workers[hire][-1]) if hire.any() else 0

    table = pd.DataFrame(
        {
            "Workers": workers,
            "MP": mp_values,
            "VMP = P x MP": np.round(vmp, 2),
            "Wage": wage,
            "Hire?": ["Yes" if h else "No" for h in hire],
        }
    )
    st.dataframe(table, use_container_width=True, hide_index=True)

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=workers, y=vmp, name="VMP / labor demand", mode="lines+markers", line=dict(width=3, color=GREEN)))
    fig.add_trace(go.Scatter(x=workers, y=np.full_like(workers, wage, dtype=float), name="Wage", line=dict(width=3, color=GOLD, dash="dash")))
    fig.update_xaxes(title="Workers")
    fig.update_yaxes(title="Florins per week")
    st.plotly_chart(styled(fig), use_container_width=True, key="vmp_derived_demand")

    c1, c2 = st.columns(2)
    c1.metric("Optimal workers", optimal_workers)
    c2.metric("Rule", "Hire while VMP >= W")
    if st.toggle("Full analysis", value=False, key="vmp_derived_demand_analysis"):
        st.markdown(
            "Factor demand is derived from product demand. The firm hires another worker only when the dollar value of that worker's extra output is at least as large as the wage."
        )
        st.latex(r"VMP=P_{output}\times MP,\qquad hire\ while\ VMP\ge W")


def lorenz_gini_app():
    st.subheader("Lorenz Curve and Gini Coefficient")
    st.caption("Uses the Module 7 worksheet quintile shares by default.")

    default_shares = [4.0, 9.0, 15.0, 23.0, 49.0]
    shares = []
    st.sidebar.markdown("**Income shares by quintile**")
    for idx, default in enumerate(default_shares, 1):
        shares.append(st.sidebar.number_input(f"Quintile {idx} share (%)", 0.0, 100.0, default, 0.5))

    total = sum(shares)
    normalized = np.array(shares) / total if total else np.array(default_shares) / 100
    cumulative_income = np.r_[0, np.cumsum(normalized)]
    cumulative_population = np.linspace(0, 1, len(cumulative_income))
    gini = 1 - 2 * np.trapz(cumulative_income, cumulative_population)

    table = pd.DataFrame(
        {
            "Quintile": ["Lowest 20%", "Second 20%", "Third 20%", "Fourth 20%", "Top 20%"],
            "Share of total income (%)": np.round(normalized * 100, 2),
            "Cumulative income share (%)": np.round(cumulative_income[1:] * 100, 2),
            "Perfectly equal (%)": [20, 40, 60, 80, 100],
        }
    )
    st.dataframe(table, use_container_width=True, hide_index=True)

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=cumulative_population, y=cumulative_population, name="Perfect equality", line=dict(width=2, dash="dash", color=SAGE)))
    fig.add_trace(go.Scatter(x=cumulative_population, y=cumulative_income, name="Lorenz curve", fill="tonexty", line=dict(width=3, color=RED)))
    fig.update_xaxes(title="Cumulative population share", tickformat=".0%")
    fig.update_yaxes(title="Cumulative income share", tickformat=".0%")
    st.plotly_chart(styled(fig), use_container_width=True, key="lorenz_gini")

    st.metric("Approximate Gini coefficient", f"{gini:.3f}")
    if st.toggle("Full analysis", value=False, key="lorenz_gini_analysis"):
        st.markdown(
            "The Lorenz curve plots cumulative income against cumulative population. The Gini coefficient is the area between the equality line and the Lorenz curve divided by the total area under equality."
        )


def economic_accounting_profit_app():
    st.subheader("Economic vs Accounting Profit")
    st.caption("Supports Module 9's Detroit/Flint profit problems: explicit costs are visible; implicit costs are opportunity costs.")

    revenue = st.sidebar.number_input("Total revenue", 0.0, 10000000.0, 35000.0, 1000.0)
    rent = st.sidebar.number_input("Rent or operating cost", 0.0, 10000000.0, 8000.0, 500.0)
    materials = st.sidebar.number_input("Inventory / materials", 0.0, 10000000.0, 10000.0, 500.0)
    foregone_wage = st.sidebar.number_input("Foregone wage or salary", 0.0, 10000000.0, 12000.0, 500.0)
    savings = st.sidebar.number_input("Capital or savings invested", 0.0, 10000000.0, 20000.0, 1000.0)
    alt_return = st.sidebar.slider("Alternative return on capital", 0.0, 20.0, 5.0, 0.5) / 100

    explicit_costs = rent + materials
    implicit_costs = foregone_wage + savings * alt_return
    accounting_profit = revenue - explicit_costs
    economic_profit = revenue - explicit_costs - implicit_costs

    c1, c2, c3 = st.columns(3)
    c1.metric("Accounting profit", f"{accounting_profit:,.2f}")
    c2.metric("Implicit costs", f"{implicit_costs:,.2f}")
    c3.metric("Economic profit", f"{economic_profit:,.2f}")

    fig = go.Figure()
    fig.add_bar(x=["Revenue"], y=[revenue], name="Revenue", marker_color=GREEN)
    fig.add_bar(x=["Explicit costs", "Implicit costs"], y=[explicit_costs, implicit_costs], name="Costs", marker_color=[GOLD, RED])
    fig.update_yaxes(title="Dollars")
    st.plotly_chart(styled(fig), use_container_width=True, key="economic_accounting_profit")

    if st.toggle("Full analysis", value=False, key="economic_accounting_profit_analysis"):
        st.markdown(
            "Accounting profit subtracts explicit costs only. Economic profit subtracts explicit and implicit costs, so it asks whether the choice beats the next-best alternative."
        )
        st.latex(r"Accounting\ Profit=TR-Explicit\ Costs")
        st.latex(r"Economic\ Profit=TR-Explicit\ Costs-Implicit\ Costs")


def capitalism_climate_app():
    st.subheader("Climate Externality and the Atmosphere Commons")
    demand_intercept = st.sidebar.slider("Willingness-to-pay intercept", 20.0, 200.0, 110.0, 5.0)
    demand_slope = st.sidebar.slider("Demand slope", 0.10, 2.00, 0.55, 0.05)
    private_cost = st.sidebar.slider("Private marginal cost intercept", 0.0, 100.0, 20.0, 2.0)
    cost_slope = st.sidebar.slider("Private marginal cost slope", 0.05, 2.00, 0.35, 0.05)
    emissions_intensity = st.sidebar.slider("Emissions per unit", 0.10, 3.00, 1.00, 0.05)
    climate_damage = st.sidebar.slider("Marginal climate damage per emission unit", 0.0, 50.0, 18.0, 1.0)
    carbon_price = st.sidebar.slider("Carbon price / emissions fee", 0.0, 100.0, 15.0, 1.0)
    stock_factor = st.sidebar.slider("Stock pollutant multiplier", 1.0, 5.0, 2.0, 0.25)

    q = np.linspace(0, 160, 400)
    demand = demand_intercept - demand_slope * q
    mpc = private_cost + cost_slope * q
    external_cost = emissions_intensity * climate_damage * stock_factor
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
    st.caption("The stock multiplier represents the Module 6 claim that CO2 is harder than a normal externality because damages persist and accumulate.")
    if st.toggle("Full analysis", value=False, key="climate_analysis"):
        st.markdown(
            "This is Climate Arc Part 1. The private market prices extraction and production costs, but not the climate damage imposed on third parties. Because the atmosphere is a commons and CO2 is a stock pollutant, market-recorded surplus overstates welfare and the static externality diagram understates the coordination problem."
        )
        st.latex(r"MSC = MPC + \text{marginal climate damage}")
        st.latex(r"\text{efficient quantity: } MB = MSC")


def capitalism_inequality_app():
    st.subheader("Three Engines and the Great Divergence")
    years = np.arange(1700, 1901, 10)
    t = (years - years[0]) / 10
    britain_tfp = st.sidebar.slider("Britain technology growth", 0.000, 0.060, 0.030, 0.005)
    britain_capital = st.sidebar.slider("Britain capital deepening", 0.000, 0.060, 0.025, 0.005)
    extractive_drag = st.sidebar.slider("Extractive-institution drag", 0.000, 0.050, 0.020, 0.005)
    colonial_shock = st.sidebar.slider("Colonial/deindustrialization shock", 0.0, 0.60, 0.25, 0.05)

    britain = 100 * (1 + britain_tfp + britain_capital) ** t
    china = 105 * (1 + max(britain_tfp * 0.30 - extractive_drag * 0.25, -0.02)) ** t
    india = 100 * (1 + max(britain_tfp * 0.18 - extractive_drag, -0.03)) ** t
    africa = 85 * (1 + max(britain_tfp * 0.15 - extractive_drag * 0.8, -0.03)) ** t
    shock_path = np.linspace(0, colonial_shock, len(years))
    india *= (1 - shock_path)
    africa *= (1 - shock_path * 0.55)

    fig = go.Figure()
    for series, name, color in [
        (britain, "Britain: technology + capital deepening", GREEN),
        (china, "China: constrained accumulation", GOLD),
        (india, "India/Bengal: deindustrialization shock", RED),
        (africa, "Sub-Saharan Africa: extraction drag", BLUE),
    ]:
        fig.add_trace(go.Scatter(x=years, y=series, name=name, line=dict(width=3, color=color)))
    fig.update_xaxes(title="Year")
    fig.update_yaxes(title="Income per person index")
    st.plotly_chart(styled(fig), use_container_width=True, key="great_divergence")
    c1, c2, c3 = st.columns(3)
    c1.metric("Britain 1900 index", f"{britain[-1]:.0f}")
    c2.metric("India/Bengal 1900 index", f"{india[-1]:.0f}")
    c3.metric("Britain vs India ratio", f"{britain[-1] / max(india[-1], 1):.1f}x")
    if st.toggle("Full analysis", value=False, key="ineq_analysis"):
        st.markdown(
            "This model maps to Module 6 Parts 3 and 4. The hockey stick begins when technology becomes continuous and capital deepening raises labor productivity. The Great Divergence asks why those engines activated unevenly: institutions, geography, colonial extraction, and technological accidents are competing explanations, not mutually exclusive sliders."
        )
        st.latex(r"Y=A\cdot K^{\alpha}\cdot L^{1-\alpha}")


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
    params = st.session_state.get("selected_model_params", {})
    if params.get("worksheet_note"):
        st.info(params["worksheet_note"])
    if params.get("mc_schedule"):
        schedule = pd.DataFrame(params["mc_schedule"], columns=["Q", "MC"])
        price = st.sidebar.slider("Market price", 0.1, 200.0, float(params.get("price", 70.0)), 0.1, key="pc_p_schedule")
        atc_at_q = float(params.get("atc_at_q", 0.0))
        avc_at_q = float(params.get("avc_at_q", 0.0))
        q_star = float(schedule.iloc[(schedule["MC"] - price).abs().idxmin()]["Q"])
        mc_star = float(schedule.iloc[(schedule["Q"] - q_star).abs().idxmin()]["MC"])
        profit = (price - atc_at_q) * q_star if atc_at_q else 0.0
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=schedule["Q"], y=schedule["MC"], mode="lines+markers", name="MC", line=dict(width=3, color=GREEN)))
        fig.add_trace(go.Scatter(x=schedule["Q"], y=np.full(len(schedule), price), name="MR = P", line=dict(width=3, color=GOLD)))
        if atc_at_q:
            fig.add_trace(go.Scatter(x=[q_star], y=[atc_at_q], mode="markers+text", name="ATC at Q*", text=["ATC"], textposition="bottom center", marker=dict(size=11, color=RED)))
        if avc_at_q:
            fig.add_trace(go.Scatter(x=[q_star], y=[avc_at_q], mode="markers+text", name="AVC at Q*", text=["AVC"], textposition="bottom center", marker=dict(size=11, color=BLUE)))
        fig.add_trace(go.Scatter(x=[q_star], y=[mc_star], mode="markers+text", name="MR = MC", text=["MR=MC"], textposition="top center", marker=dict(size=12, color=POINT)))
        fig.update_xaxes(title="Output Q")
        fig.update_yaxes(title="Dollars per unit")
        st.plotly_chart(styled(fig), use_container_width=True, key="pc_profit_schedule")
        c1, c2, c3 = st.columns(3)
        c1.metric("Profit-max Q", f"{q_star:.0f}")
        c2.metric("Economic profit", f"{profit:.2f}")
        c3.metric("Produce?", "Yes" if not avc_at_q or price >= avc_at_q else "Shut down")
        return

    max_fc = max(500.0, float(params.get("fixed_cost", 120.0)))
    fc = st.sidebar.slider("Fixed cost", 0.0, max_fc, float(params.get("fixed_cost", 120.0)), 10.0, key="pc_fc")
    price = st.sidebar.slider("Market price", 1.0, 200.0, float(params.get("price", 70.0)), 1.0, key="pc_p")
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


def game_theory_preview_app():
    st.subheader("Game Theory Preview: Players, Strategies, and Payoffs")
    scenario = st.sidebar.selectbox(
        "Preview scenario",
        ["Marcus and coworkers ask for a raise", "Two food carts choose price posture"],
    )
    if scenario.startswith("Marcus"):
        matrix = pd.DataFrame(
            {
                "Coworker asks": ["4, 4", "1, 5"],
                "Coworker stays silent": ["5, 1", "2, 2"],
            },
            index=["Marcus asks", "Marcus stays silent"],
        )
        lesson = (
            "This preview focuses on the structure: each worker's payoff depends on the "
            "other worker's action. The collectively stronger outcome may be individually risky."
        )
    else:
        matrix = pd.DataFrame(
            {
                "Ray keeps price high": ["3, 3", "5, 1"],
                "Ray cuts price": ["1, 5", "2, 2"],
            },
            index=["Marcus keeps price high", "Marcus cuts price"],
        )
        lesson = (
            "The point is strategic interdependence: Marcus's best move cannot be judged "
            "without Ray's possible move. Formal Nash equilibrium comes later in Module 11."
        )
    st.dataframe(matrix, use_container_width=True)
    st.info(lesson)
    if st.toggle("Full analysis", value=False, key="game_preview_analysis"):
        st.markdown(
            "Module 7 should name players, strategies, and payoffs, and should let students see the prisoner's-dilemma structure. It should not require formal Nash-equilibrium analysis yet."
        )


def credit_exclusion_labor_power_app():
    st.subheader("Credit Exclusion and Labor Power")
    monthly_income = st.sidebar.slider("Monthly income", 800.0, 6000.0, 2000.0, 100.0)
    repair_need = st.sidebar.slider("Emergency expense", 100.0, 3000.0, 500.0, 50.0)
    low_apr = st.sidebar.slider("Credit-union APR", 0.0, 36.0, 6.0, 0.5)
    high_apr = st.sidebar.slider("Payday APR", 40.0, 500.0, 300.0, 10.0)
    months = st.sidebar.slider("Repayment horizon (months)", 1, 24, 6, 1)
    ray_wage = st.sidebar.slider("Ray warehouse wage", 8.0, 40.0, 15.0, 0.5)
    vmp = st.sidebar.slider("Marcus VMP", 8.0, 60.0, 24.0, 0.5)

    def payoff(apr):
        monthly_rate = apr / 100 / 12
        if monthly_rate == 0:
            return repair_need / months
        return repair_need * monthly_rate / (1 - (1 + monthly_rate) ** (-months))

    low_payment = payoff(low_apr)
    high_payment = payoff(high_apr)
    wage_gap = max(vmp - ray_wage, 0)
    hours_needed_low = low_payment / max(ray_wage, 1e-9)
    hours_needed_high = high_payment / max(ray_wage, 1e-9)

    fig = go.Figure()
    fig.add_bar(x=["Credit union", "Payday lender"], y=[low_payment, high_payment], name="Monthly payment", marker_color=[GREEN, RED])
    fig.add_bar(x=["Ray wage", "Marcus VMP"], y=[ray_wage, vmp], name="Hourly value", marker_color=[GOLD, BLUE], yaxis="y2")
    fig.update_layout(
        yaxis=dict(title="Monthly loan payment"),
        yaxis2=dict(title="Dollars per hour", overlaying="y", side="right"),
    )
    st.plotly_chart(styled(fig), use_container_width=True, key="credit_exclusion_labor_power")
    c1, c2, c3 = st.columns(3)
    c1.metric("Extra monthly credit burden", f"{high_payment - low_payment:.2f}")
    c2.metric("Extra work hours/month", f"{hours_needed_high - hours_needed_low:.1f}")
    c3.metric("VMP-wage gap", f"{wage_gap:.2f}/hr")
    if st.toggle("Full analysis", value=False, key="credit_exclusion_analysis"):
        st.markdown(
            "Credit exclusion compresses the feasible set even when income is unchanged. Labor power matters at the same time: if Marcus is paid below VMP, he has less monthly income available to absorb shocks or finance exit from Ray's warehouse."
        )
        st.latex(r"\text{monthly loan payment}=\frac{Lr}{1-(1+r)^{-n}}")


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


def technology_ai_climate_inequality_app():
    st.subheader("Technology, AI Bias, and Climate Inequality")
    years = np.arange(0, 21)
    high_access_speed = st.sidebar.slider("High-income adoption speed", 0.10, 1.00, 0.45, 0.05)
    low_access_speed = st.sidebar.slider("Low-income adoption speed", 0.05, 0.80, 0.22, 0.05)
    skill_complement = st.sidebar.slider("Skill-complement payoff", 0.0, 2.0, 0.75, 0.05)
    proxy_bias = st.sidebar.slider("AI proxy bias", 0.0, 0.6, 0.22, 0.02)
    climate_exposure = st.sidebar.slider("Climate exposure gap", 0.0, 0.6, 0.25, 0.02)

    high_adopt = 1 / (1 + np.exp(-high_access_speed * (years - 8)))
    low_adopt = 1 / (1 + np.exp(-low_access_speed * (years - 11)))
    high_mrp = 20 + 18 * high_adopt * (1 + skill_complement)
    low_mrp = 20 + 18 * low_adopt * (1 + skill_complement) * (1 - proxy_bias) * (1 - climate_exposure)

    tab1, tab2 = st.tabs(["Diffusion", "MRP gap"])
    with tab1:
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=years, y=high_adopt, name="High-access group", line=dict(width=4, color=GREEN)))
        fig.add_trace(go.Scatter(x=years, y=low_adopt, name="Low-access group", line=dict(width=4, color=RED)))
        fig.update_xaxes(title="Years after new technology")
        fig.update_yaxes(title="Adoption share", range=[0, 1])
        st.plotly_chart(styled(fig), use_container_width=True, key="tech_diffusion")
    with tab2:
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=years, y=high_mrp, name="High-access MRP", line=dict(width=4, color=GREEN)))
        fig.add_trace(go.Scatter(x=years, y=low_mrp, name="Low-access MRP after bias/exposure", line=dict(width=4, color=RED)))
        fig.update_xaxes(title="Years after new technology")
        fig.update_yaxes(title="Estimated MRP")
        st.plotly_chart(styled(fig), use_container_width=True, key="tech_mrp_gap")
    st.metric("Final MRP gap", f"{high_mrp[-1] - low_mrp[-1]:.2f}")
    if st.toggle("Full analysis", value=False, key="tech_ai_climate_analysis"):
        st.markdown(
            "The S-curve shows technology diffusion. Access gaps create early MRP gaps; skill complementarity can amplify them. Proxy bias and climate exposure can then make the final labor-market outcome even more unequal."
        )


def climate_distributional_injustice_app():
    st.subheader("Climate as Distributional Injustice")
    rich_emissions = st.sidebar.slider("High-income emissions responsibility", 0.10, 0.90, 0.70, 0.05)
    low_emissions = 1 - rich_emissions
    rich_exposure = st.sidebar.slider("High-income climate exposure", 0.05, 0.70, 0.25, 0.05)
    low_exposure = 1 - rich_exposure
    adaptation = st.sidebar.slider("Adaptation capacity gap", 0.0, 0.80, 0.45, 0.05)
    land_mp = st.sidebar.slider("Baseline MP of exposed land/labor", 10.0, 100.0, 50.0, 1.0)

    rich_damage = rich_exposure * (1 - adaptation) * land_mp
    low_damage = low_exposure * (1 + adaptation) * land_mp
    fig = go.Figure()
    fig.add_bar(x=["High-income group", "Low-income group"], y=[rich_emissions, low_emissions], name="Emissions share", marker_color=BLUE)
    fig.add_bar(x=["High-income group", "Low-income group"], y=[rich_exposure, low_exposure], name="Exposure share", marker_color=GOLD)
    fig.add_bar(x=["High-income group", "Low-income group"], y=[rich_damage / land_mp, low_damage / land_mp], name="Productivity damage index", marker_color=RED)
    fig.update_yaxes(title="Share / index")
    st.plotly_chart(styled(fig), use_container_width=True, key="climate_distribution")
    c1, c2 = st.columns(2)
    c1.metric("High-income MP loss", f"{rich_damage:.1f}")
    c2.metric("Low-income MP loss", f"{low_damage:.1f}")
    if st.toggle("Full analysis", value=False, key="climate_distribution_analysis"):
        st.markdown(
            "The distributional injustice is the mismatch between responsibility and exposure. Climate shocks also operate through factor markets by lowering the marginal product of land and labor in exposed communities."
        )


def labor_leisure_app():
    st.subheader("Labor-Leisure Choice")
    hours = np.linspace(0, 16, 250)
    wage = st.sidebar.slider("Wage", 1.0, 80.0, 18.0, 1.0)
    nonlabor_income = st.sidebar.slider("Non-labor income", 0.0, 300.0, 40.0, 5.0)
    preference_leisure = st.sidebar.slider("Preference for leisure", 0.10, 0.90, 0.45, 0.05)
    total_time = st.sidebar.slider("Available hours", 8.0, 24.0, 16.0, 1.0)
    leisure = total_time - hours
    consumption = nonlabor_income + wage * hours
    utility = (np.maximum(leisure, 0.01) ** preference_leisure) * (consumption ** (1 - preference_leisure))
    i = int(np.argmax(utility))
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=leisure, y=consumption, name="Feasible frontier", line=dict(width=3, color=GREEN)))
    fig.add_trace(go.Scatter(x=[leisure[i]], y=[consumption[i]], mode="markers+text", text=["Choice"], textposition="top center", marker=dict(size=12, color=POINT), name="Best bundle"))
    fig.update_xaxes(title="Leisure hours")
    fig.update_yaxes(title="Consumption")
    st.plotly_chart(styled(fig), use_container_width=True, key="labor_leisure")
    c1, c2, c3 = st.columns(3)
    c1.metric("Work hours", f"{hours[i]:.1f}")
    c2.metric("Leisure hours", f"{leisure[i]:.1f}")
    c3.metric("Consumption", f"{consumption[i]:.2f}")
    if st.toggle("Full analysis", value=False, key="labor_leisure_analysis"):
        st.markdown("The wage is the opportunity cost of leisure. A higher wage rotates the feasible frontier and creates both substitution and income effects.")


def malthus_growth_app():
    st.subheader("Malthusian Trap and Demographic Transition")
    years = np.arange(0, 201)
    tech_growth = st.sidebar.slider("Technology growth", 0.000, 0.040, 0.010, 0.002)
    population_response = st.sidebar.slider("Baseline population response", 0.000, 0.050, 0.018, 0.002)
    transition_strength = st.sidebar.slider("Demographic transition strength", 0.0, 1.0, 0.45, 0.05)
    transition_year = st.sidebar.slider("Transition begins", 20, 180, 95, 5)
    shock_year = st.sidebar.slider("Shock year", 20, 180, 70, 5)
    shock_size = st.sidebar.slider("Population shock", 0.0, 0.8, 0.35, 0.05)
    technology = (1 + tech_growth) ** years
    transition = 1 / (1 + np.exp(-(years - transition_year) / 12))
    effective_pop_response = population_response * (1 - transition_strength * transition)
    population = np.cumprod(1 + effective_pop_response)
    population = population * np.where(years >= shock_year, 1 - shock_size, 1)
    income_pc = 100 * technology / np.maximum(population ** 0.55, 1e-9)
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=years, y=income_pc, name="Income per person", line=dict(width=4, color=GREEN)))
    fig.add_trace(go.Scatter(x=years, y=100 * technology, name="Technology", line=dict(width=3, color=BLUE)))
    fig.add_trace(go.Scatter(x=years, y=100 * population / population[0], name="Population", line=dict(width=3, color=RED)))
    fig.update_xaxes(title="Years")
    fig.update_yaxes(title="Index")
    st.plotly_chart(styled(fig), use_container_width=True, key="malthus_growth")
    c1, c2, c3 = st.columns(3)
    c1.metric("Final income per person", f"{income_pc[-1]:.1f}")
    c2.metric("Final technology index", f"{100 * technology[-1]:.1f}")
    c3.metric("Final population index", f"{100 * population[-1] / population[0]:.1f}")
    if st.toggle("Full analysis", value=False, key="malthus_analysis"):
        st.markdown(
            "Malthusian pressure appears when population growth absorbs productivity gains and returns living standards toward subsistence. Escape requires continuous productivity growth plus the demographic transition: as child mortality falls, schooling expands, and women's opportunity cost rises, higher income can lead to fewer, more-invested-in children."
        )


def gdp_wellbeing_app():
    st.subheader("Poverty, GDP, and the Kuznets Curve")
    gdp = st.sidebar.slider("GDP per person index", 20.0, 200.0, 100.0, 5.0)
    inequality = st.sidebar.slider("Inequality", 0.0, 1.0, 0.35, 0.05)
    redistribution = st.sidebar.slider("Redistribution / public investment", 0.0, 1.0, 0.30, 0.05)
    unpaid_work = st.sidebar.slider("Unpaid work / care value", 0.0, 80.0, 20.0, 2.0)
    pollution = st.sidebar.slider("Pollution damage", 0.0, 80.0, 25.0, 2.0)
    leisure = st.sidebar.slider("Leisure and health value", 0.0, 80.0, 25.0, 2.0)
    adjusted = gdp * (1 - 0.35 * inequality) + unpaid_work + leisure - pollution
    income = np.linspace(20, 200, 200)
    kuznets = 0.18 + 0.45 * np.exp(-((income - 95) / 45) ** 2)
    policy_path = kuznets * (1 - redistribution * 0.55)
    absolute_poverty = max(0.0, 100 - gdp) * (1 - redistribution * 0.45)
    relative_poverty = max(0.0, inequality * 100 - redistribution * 25)

    tab1, tab2 = st.tabs(["GDP limits", "Kuznets and poverty"])
    with tab1:
        fig = go.Figure(go.Bar(
            x=["GDP/person", "Inequality penalty", "Unpaid work", "Leisure/health", "Pollution cost", "Adjusted wellbeing"],
            y=[gdp, -gdp * 0.35 * inequality, unpaid_work, leisure, -pollution, adjusted],
            marker_color=[GREEN, RED, BLUE, SAGE, RED, POINT],
        ))
        fig.update_yaxes(title="Index contribution")
        st.plotly_chart(styled(fig), use_container_width=True, key="gdp_wellbeing")
    with tab2:
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=income, y=kuznets, name="Kuznets hypothesis", line=dict(width=3, color=RED)))
        fig.add_trace(go.Scatter(x=income, y=policy_path, name="With redistribution/public investment", line=dict(width=3, color=GREEN)))
        fig.add_trace(go.Scatter(x=[gdp], y=[inequality], mode="markers+text", text=["Current"], textposition="top center", marker=dict(size=12, color=POINT), name="Current economy"))
        fig.update_xaxes(title="GDP per person index")
        fig.update_yaxes(title="Inequality index", range=[0, 0.75])
        st.plotly_chart(styled(fig), use_container_width=True, key="kuznets_poverty")
    c1, c2, c3 = st.columns(3)
    c1.metric("Adjusted wellbeing", f"{adjusted:.1f}", f"{adjusted - gdp:.1f} vs GDP")
    c2.metric("Absolute poverty pressure", f"{absolute_poverty:.1f}")
    c3.metric("Relative poverty pressure", f"{relative_poverty:.1f}")
    if st.toggle("Full analysis", value=False, key="gdp_analysis"):
        st.markdown(
            "This model maps to Module 6 Part 5. GDP per person helps measure absolute poverty, but it does not tell us how income is distributed or whether people have real capabilities. The Kuznets hypothesis says inequality may first rise and then fall with development; the policy question is whether 'grow first, redistribute later' treats avoidable deprivation as temporary."
        )


def price_discrimination_app():
    st.subheader("Price Discrimination")
    demand_intercept = st.sidebar.slider("Demand intercept", 50.0, 200.0, 120.0, 5.0)
    demand_slope = st.sidebar.slider("Demand slope", 0.2, 3.0, 1.0, 0.1)
    mc = st.sidebar.slider("Marginal cost", 0.0, 100.0, 25.0, 1.0)
    degree = st.sidebar.selectbox("Type", ["Single monopoly price", "First-degree", "Third-degree"])
    q = np.linspace(0, demand_intercept / demand_slope, 300)
    demand = demand_intercept - demand_slope * q
    mr = demand_intercept - 2 * demand_slope * q
    if degree == "First-degree":
        q_star = max((demand_intercept - mc) / demand_slope, 0)
        profit = 0.5 * (demand_intercept - mc) * q_star
    else:
        q_star = max((demand_intercept - mc) / (2 * demand_slope), 0)
        p_star = demand_intercept - demand_slope * q_star
        profit = (p_star - mc) * q_star
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=q, y=demand, name="Demand", line=dict(width=3, color=GREEN)))
    fig.add_trace(go.Scatter(x=q, y=mr, name="MR", line=dict(width=3, color=GOLD)))
    fig.add_trace(go.Scatter(x=q, y=np.full_like(q, mc), name="MC", line=dict(width=3, color=RED)))
    fig.add_trace(go.Scatter(x=[q_star], y=[mc if degree == "First-degree" else demand_intercept - demand_slope * q_star], mode="markers+text", text=[degree], textposition="top center", marker=dict(size=12, color=POINT), name="Output"))
    fig.update_xaxes(title="Quantity")
    fig.update_yaxes(title="Price")
    st.plotly_chart(styled(fig), use_container_width=True, key="price_discrimination")
    st.metric("Output", f"{q_star:.1f}")
    st.metric("Producer surplus/profit area", f"{profit:.1f}")
    if st.toggle("Full analysis", value=False, key="pd_analysis"):
        st.markdown("Price discrimination changes who captures surplus. First-degree discrimination converts consumer surplus into producer surplus; third-degree discrimination charges different groups different prices based on elasticities.")


def hhi_antitrust_app():
    st.subheader("Antitrust: HHI and Merger Analysis")
    base = {
        "American": 17, "Delta": 17, "United": 15, "Southwest": 17,
        "Spirit": 5, "Alaska": 5, "JetBlue": 5, "Frontier": 3, "Other": 16,
    }
    acquirer = st.sidebar.selectbox("Acquirer", list(base), index=3)
    target = st.sidebar.selectbox("Target", [k for k in base if k != acquirer], index=3)
    shares = base.copy()
    hhi_before = sum(v * v for v in shares.values())
    shares[acquirer] += shares[target]
    shares.pop(target)
    hhi_after = sum(v * v for v in shares.values())
    delta = hhi_after - hhi_before
    fig = go.Figure()
    fig.add_bar(x=list(base), y=list(base.values()), name="Before", marker_color=BLUE)
    fig.add_bar(x=list(shares), y=list(shares.values()), name="After", marker_color=GOLD)
    fig.update_yaxes(title="Market share (%)")
    st.plotly_chart(styled(fig), use_container_width=True, key="hhi_antitrust")
    c1, c2, c3 = st.columns(3)
    c1.metric("HHI before", f"{hhi_before:.0f}")
    c2.metric("HHI after", f"{hhi_after:.0f}")
    c3.metric("ΔHHI", f"{delta:.0f}")
    st.info("DOJ/FTC screen: markets above 1,800 HHI are highly concentrated; a large positive ΔHHI raises concern.")
    if st.toggle("Full analysis", value=False, key="hhi_analysis"):
        st.latex(r"HHI=\sum_i s_i^2")
        st.markdown("HHI is sensitive to mergers because combining two firms removes rivalry between them and squares the combined market share.")


def tax_incidence_app():
    st.subheader("Tax Incidence")
    params = st.session_state.get("selected_model_params", {})
    if params.get("worksheet_note"):
        st.info(params["worksheet_note"])

    st.sidebar.markdown("**Starting market**")
    q0 = st.sidebar.slider("Pre-tax equilibrium quantity", 20.0, 200.0, float(params.get("q0", 100.0)), 5.0)
    p0 = st.sidebar.slider("Pre-tax equilibrium price", 5.0, 100.0, float(params.get("p0", 40.0)), 1.0)
    tax = st.sidebar.slider("Supply-side tax per unit", 0.0, 80.0, float(params.get("tax", 12.0)), 1.0)

    st.sidebar.markdown("**Elasticity at the pre-tax equilibrium**")
    demand_elasticity = st.sidebar.slider("|Demand elasticity|", 0.10, 5.00, abs(float(params.get("demand_elasticity", 0.60))), 0.05)
    supply_elasticity = st.sidebar.slider("Supply elasticity", 0.10, 5.00, float(params.get("supply_elasticity", 1.20)), 0.05)
    show_pre_tax_surplus = st.sidebar.toggle("Show pre-tax surplus", value=False, key="tax_show_pre_surplus")

    demand_slope = p0 / (demand_elasticity * q0)
    supply_slope = p0 / (supply_elasticity * q0)
    demand_intercept = p0 + demand_slope * q0
    supply_intercept = p0 - supply_slope * q0

    q_tax = max(0.0, (demand_intercept - supply_intercept - tax) / (demand_slope + supply_slope))
    pc = demand_intercept - demand_slope * q_tax
    pp = pc - tax

    consumer_burden = max(0.0, pc - p0)
    producer_burden = max(0.0, p0 - pp)
    consumer_share = consumer_burden / tax if tax else 0.0
    producer_share = producer_burden / tax if tax else 0.0

    pre_cs = max(0.0, 0.5 * (demand_intercept - p0) * q0)
    pre_ps = max(0.0, 0.5 * (p0 - supply_intercept) * q0)
    post_cs = max(0.0, 0.5 * (demand_intercept - pc) * q_tax)
    post_ps = max(0.0, 0.5 * (pp - supply_intercept) * q_tax)
    tax_revenue = tax * q_tax
    deadweight_loss = max(0.0, 0.5 * tax * (q0 - q_tax))

    xmax = max(q0 * 1.35, q_tax * 1.35, 50)
    ymax = max(demand_intercept, pc + tax * 0.35, p0 + tax * 1.2, 20) * 1.08
    q = np.linspace(0, xmax, 300)
    demand = demand_intercept - demand_slope * q
    supply = supply_intercept + supply_slope * q
    supply_tax = supply + tax

    fig = go.Figure()
    if show_pre_tax_surplus:
        fig.add_trace(go.Scatter(
            x=[0, q0, 0],
            y=[p0, p0, demand_intercept],
            mode="lines",
            fill="toself",
            name="Pre-tax consumer surplus",
            line=dict(width=0),
            fillcolor="rgba(51,101,138,0.16)",
            hoverinfo="skip",
        ))
        fig.add_trace(go.Scatter(
            x=[0, q0, 0],
            y=[supply_intercept, p0, p0],
            mode="lines",
            fill="toself",
            name="Pre-tax producer surplus",
            line=dict(width=0),
            fillcolor="rgba(196,154,108,0.18)",
            hoverinfo="skip",
        ))

    if q_tax > 0:
        fig.add_trace(go.Scatter(
            x=[0, q_tax, 0],
            y=[pc, pc, demand_intercept],
            mode="lines",
            fill="toself",
            name="Consumer surplus after tax",
            line=dict(width=0),
            fillcolor="rgba(51,101,138,0.24)",
            hoverinfo="skip",
        ))
        fig.add_trace(go.Scatter(
            x=[0, q_tax, 0],
            y=[supply_intercept, pp, pp],
            mode="lines",
            fill="toself",
            name="Producer surplus after tax",
            line=dict(width=0),
            fillcolor="rgba(196,154,108,0.30)",
            hoverinfo="skip",
        ))
        fig.add_trace(go.Scatter(
            x=[0, q_tax, q_tax, 0],
            y=[pp, pp, pc, pc],
            mode="lines",
            fill="toself",
            name="Tax revenue",
            line=dict(width=0),
            fillcolor="rgba(179,130,16,0.30)",
            hoverinfo="skip",
        ))
    if deadweight_loss > 0:
        fig.add_trace(go.Scatter(
            x=[q_tax, q0, q_tax],
            y=[pp, p0, pc],
            mode="lines",
            fill="toself",
            name="Deadweight loss",
            line=dict(width=0),
            fillcolor="rgba(178,63,53,0.26)",
            hoverinfo="skip",
        ))

    visible = demand >= 0
    fig.add_trace(go.Scatter(x=q[visible], y=demand[visible], name="Demand", line=dict(width=3, color=GREEN)))
    fig.add_trace(go.Scatter(x=q, y=supply, name="Supply before tax", line=dict(width=3, color=SAGE, dash="dash")))
    fig.add_trace(go.Scatter(x=q, y=supply_tax, name="Supply plus tax", line=dict(width=3, color=GOLD)))
    fig.add_trace(go.Scatter(x=[q0], y=[p0], mode="markers+text", text=["Pre-tax"], textposition="top center", marker=dict(size=11, color=BLUE), name="Pre-tax equilibrium"))
    fig.add_trace(go.Scatter(x=[q_tax], y=[pc], mode="markers+text", text=["Consumer price"], textposition="top center", marker=dict(size=12, color=POINT), name="Price paid by buyers"))
    fig.add_trace(go.Scatter(x=[q_tax], y=[pp], mode="markers+text", text=["Producer price"], textposition="bottom center", marker=dict(size=12, color=RED), name="Price received by sellers"))
    fig.add_shape(type="line", x0=q_tax, x1=q_tax, y0=pp, y1=pc, line=dict(width=4, color=POINT))
    fig.add_shape(type="line", x0=0, x1=q_tax, y0=pc, y1=pc, line=dict(width=1, dash="dot", color=POINT))
    fig.add_shape(type="line", x0=0, x1=q_tax, y0=pp, y1=pp, line=dict(width=1, dash="dot", color=RED))
    fig.update_xaxes(title="Quantity", range=[0, xmax])
    fig.update_yaxes(title="Price", range=[max(0, min(supply_intercept, pp) * 0.95), ymax])
    fig.update_layout(legend=dict(orientation="h", y=1.16, x=0))
    st.plotly_chart(styled(fig), use_container_width=True, key="tax_incidence")

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Consumer burden", f"{consumer_burden:.2f}", f"{consumer_share:.0%}" if tax else "0%")
    c2.metric("Producer burden", f"{producer_burden:.2f}", f"{producer_share:.0%}" if tax else "0%")
    c3.metric("Quantity change", f"{q_tax - q0:.1f}")
    c4.metric("Tax revenue", f"{tax_revenue:.1f}")

    c5, c6, c7, c8 = st.columns(4)
    c5.metric("Consumer surplus", f"{post_cs:.1f}", f"{post_cs - pre_cs:.1f}")
    c6.metric("Producer surplus", f"{post_ps:.1f}", f"{post_ps - pre_ps:.1f}")
    c7.metric("Deadweight loss", f"{deadweight_loss:.1f}")
    c8.metric("Total surplus after tax", f"{post_cs + post_ps + tax_revenue:.1f}")

    if st.toggle("Full analysis", value=False, key="incidence_analysis"):
        st.markdown(
            "The supply-side tax shifts the supply curve up by the tax amount, creating a wedge between the price buyers pay and the price sellers receive. The less elastic side bears more of that wedge because it changes quantity less in response to price. When demand is relatively inelastic, buyers absorb more of the tax through a higher consumer price. When supply is relatively inelastic, sellers absorb more through a lower producer price."
        )


def behavioral_policy_app():
    st.subheader("Behavioral Policy: Biases and Fixes")
    bias = st.sidebar.selectbox("Behavioral failure", ["Present bias", "Loss aversion", "Framing effect", "Overconfidence"])
    stakes = st.sidebar.slider("Stakes", 1.0, 100.0, 50.0, 1.0)
    bias_strength = st.sidebar.slider("Bias strength", 0.0, 1.0, 0.45, 0.05)
    policy_strength = st.sidebar.slider("Policy design strength", 0.0, 1.0, 0.50, 0.05)
    rational_choice = stakes
    biased_choice = stakes * (1 - bias_strength)
    policy_choice = biased_choice + (rational_choice - biased_choice) * policy_strength
    fig = go.Figure(go.Bar(x=["Rational benchmark", "Biased choice", "With policy design"], y=[rational_choice, biased_choice, policy_choice], marker_color=[GREEN, RED, BLUE]))
    fig.update_yaxes(title="Effective decision value")
    st.plotly_chart(styled(fig), use_container_width=True, key="behavioral_policy")
    st.metric("Policy recovery", f"{policy_choice - biased_choice:.1f}")
    if st.toggle("Full analysis", value=False, key="behavioral_policy_analysis"):
        fixes = {
            "Present bias": "defaults, commitment devices, automatic enrollment",
            "Loss aversion": "insurance framing, gradual transitions, loss-offset rebates",
            "Framing effect": "standardized disclosure and plain-language comparison",
            "Overconfidence": "stress tests, independent audits, and delayed compensation",
        }
        st.markdown(f"Policy response: {fixes[bias]}. Behavioral policy changes the choice architecture without assuming people optimize perfectly.")
