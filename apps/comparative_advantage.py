import numpy as np
import streamlit as st
import plotly.graph_objects as go
from apps.common import apply_grid

def app(scenario=None, **params):
    st.subheader("Comparative Advantage — Linear PPCs for Two Producers")
    params = {**st.session_state.get("selected_model_params", {}), **params}
    note = params.get("worksheet_note")
    producer_a = params.get("producer_a", "A")
    producer_b = params.get("producer_b", "B")
    x_label = params.get("x_label", "Good X")
    y_label = params.get("y_label", "Good Y")
    if note:
        st.info(note)

    with st.sidebar.expander(f"Producer {producer_a} ", False):
        Ax = st.number_input(f"{producer_a}: Max {x_label} (a_x)", 1.0, 10_000.0, float(params.get("a_x", 100.0)), 5.0)
        Ay = st.number_input(f"{producer_a}: Max {y_label} (a_y)", 1.0, 10_000.0, float(params.get("a_y", 100.0)), 5.0)

    with st.sidebar.expander(f"Producer {producer_b} ", False):
        Bx = st.number_input(f"{producer_b}: Max {x_label} (b_x)", 1.0, 10_000.0, float(params.get("b_x", 60.0)), 5.0)
        By = st.number_input(f"{producer_b}: Max {y_label} (b_y)", 1.0, 10_000.0, float(params.get("b_y", 140.0)), 5.0)

    with st.sidebar.expander("Analyze Trade & World Price", False):
        px_over_py = st.number_input("World relative price Px/Py (slope = -Px/Py)", 0.01, 100.0, float(params.get("relative_price", 0.8)), 0.05)
        show_trade = st.checkbox("Show trade lines through production points", value=False)

    # Linear PPCs:  y = Ymax - (Ymax/Xmax) * x
    def ppc_line(Xmax, Ymax, x):
        return Ymax - (Ymax/Xmax)*x

    xsA = np.linspace(0, Ax, 200)
    ysA = ppc_line(Ax, Ay, xsA)
    xsB = np.linspace(0, Bx, 200)
    ysB = ppc_line(Bx, By, xsB)

    # Opportunity costs (constant on linear PPC)
    OCx_A = Ay / Ax     # Y per X in A
    OCx_B = By / Bx     # Y per X in B

    # Who has CA in X? (lower OCx)
    ca_X = producer_a if OCx_A < OCx_B else producer_b
    ca_Y = producer_b if ca_X == producer_a else producer_a

    # Specialization sliders (0..1 of the CA good)
    st.markdown("### Specialization Level:")
    col1, col2 = st.columns(2)
    with col1:
        sA = st.slider(f"Producer {producer_a}", 0.0, 1.0, 1.0, 0.05)
    with col2:
        sB = st.slider(f"Producer {producer_b}", 0.0, 1.0, 1.0, 0.05)
        

    # Production points (on intercept of the CA good)
    if ca_X == producer_a:
        A_prod = (sA*Ax, 0.0)
        B_prod = (0.0, sB*By)
    else:
        A_prod = (0.0, sA*Ay)
        B_prod = (sB*Bx, 0.0)

    # Trade line helpers: line with slope -Px/Py through production point
    def trade_line_through(point, x_max, y_max, slope):
        x0, y0 = point
        xs = np.linspace(0, x_max, 2)
        ys = y0 + (-slope)*(xs - x0)  # slope = -Px/Py on (X horizontal, Y vertical)
        return xs, ys

    Xmax_all = max(Ax, Bx) * 1.1
    Ymax_all = max(Ay, By) * 1.1

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=xsA, y=ysA, mode="lines", name=f"{producer_a}: PPC"))
    fig.add_trace(go.Scatter(x=xsB, y=ysB, mode="lines", name=f"{producer_b}: PPC"))
    fig.add_trace(go.Scatter(x=[A_prod[0]], y=[A_prod[1]], mode="markers+text", text=[f"{producer_a} prod"], textposition="top center"))
    fig.add_trace(go.Scatter(x=[B_prod[0]], y=[B_prod[1]], mode="markers+text", text=[f"{producer_b} prod"], textposition="top center"))
    if show_trade:
        xs, ys = trade_line_through(A_prod, Xmax_all, Ymax_all, px_over_py)
        fig.add_trace(go.Scatter(x=xs, y=ys, mode="lines", name="A trade line", line=dict(dash="dot")))
        xs, ys = trade_line_through(B_prod, Xmax_all, Ymax_all, px_over_py)
        fig.add_trace(go.Scatter(x=xs, y=ys, mode="lines", name="B trade line", line=dict(dash="dot")))

    fig.update_layout(
        xaxis_title=x_label, yaxis_title=y_label,
        xaxis=dict(range=[0, Xmax_all], zeroline=False),
        yaxis=dict(range=[0, Ymax_all], zeroline=False),
        height=520, margin=dict(l=40, r=20, t=20, b=40)
    )
    apply_grid(fig)
    st.plotly_chart(fig, use_container_width=True,key="ca_chart")

    st.markdown(
        f"""
**Opportunity costs (Y per 1 X):** A = {OCx_A:.2f}, B = {OCx_B:.2f}  
**Comparative advantage:** {ca_X} in {x_label}, {ca_Y} in {y_label}  
**Trade-line slope:** \(-P_x/P_y = -{px_over_py:.2f}\)  (a steeper line means X is relatively pricier).
        """
    )

    show_adv = st.toggle("Advanced (show equations)", key="comp_ad_adv")
    if show_adv:
        st.latex(r" \text{PPC}_A: \; y = a_y - \frac{a_y}{a_x} x \quad;\quad \text{PPC}_B: \; y = b_y - \frac{b_y}{b_x} x ")
        st.latex(r" \text{OC}_X^A = \frac{a_y}{a_x}, \quad \text{OC}_X^B = \frac{b_y}{b_x} \;\;\Rightarrow\;\; \text{CA in X} = \arg\min \text{OC}_X ")
