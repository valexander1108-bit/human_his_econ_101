import numpy as np
import streamlit as st
import plotly.graph_objects as go

def app():
    st.subheader("Comparative Advantage — Linear PPCs for Two Producers")

    with st.sidebar.expander("Producer A ", False):
        Ax = st.number_input("A: Max X (a_x)", 10.0, 10_000.0, 100.0, 5.0)
        Ay = st.number_input("A: Max Y (a_y)", 10.0, 10_000.0, 100.0, 5.0)

    with st.sidebar.expander("Producer B ", False):
        Bx = st.number_input("B: Max X (b_x)", 10.0, 10_000.0, 60.0, 5.0)
        By = st.number_input("B: Max Y (b_y)", 10.0, 10_000.0, 140.0, 5.0)

    with st.sidebar.expander("Analyze Trade & World Price", False):
        px_over_py = st.number_input("World relative price Px/Py (slope = -Px/Py)", 0.01, 100.0, 0.8, 0.05)
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
    ca_X = "A" if OCx_A < OCx_B else "B"
    ca_Y = "B" if ca_X == "A" else "A"

    # Specialization sliders (0..1 of the CA good)
    st.markdown("### Specialization Level:")
    col1, col2 = st.columns(2)
    with col1:
        sA = st.slider("Producer A", 0.0, 1.0, 1.0, 0.05)
    with col2:
        sB = st.slider("Producer B", 0.0, 1.0, 1.0, 0.05)
        

    # Production points (on intercept of the CA good)
    if ca_X == "A":
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
    fig.add_trace(go.Scatter(x=xsA, y=ysA, mode="lines", name="A: PPC"))
    fig.add_trace(go.Scatter(x=xsB, y=ysB, mode="lines", name="B: PPC"))
    fig.add_trace(go.Scatter(x=[A_prod[0]], y=[A_prod[1]], mode="markers+text", text=["A prod"], textposition="top center"))
    fig.add_trace(go.Scatter(x=[B_prod[0]], y=[B_prod[1]], mode="markers+text", text=["B prod"], textposition="top center"))
    if show_trade:
        xs, ys = trade_line_through(A_prod, Xmax_all, Ymax_all, px_over_py)
        fig.add_trace(go.Scatter(x=xs, y=ys, mode="lines", name="A trade line", line=dict(dash="dot")))
        xs, ys = trade_line_through(B_prod, Xmax_all, Ymax_all, px_over_py)
        fig.add_trace(go.Scatter(x=xs, y=ys, mode="lines", name="B trade line", line=dict(dash="dot")))

    fig.update_layout(
        xaxis_title="Good X", yaxis_title="Good Y",
        xaxis=dict(range=[0, Xmax_all], zeroline=False),
        yaxis=dict(range=[0, Ymax_all], zeroline=False),
        height=520, margin=dict(l=40, r=20, t=20, b=40)
    )
    st.plotly_chart(fig, use_container_width=True,key="ca_chart")

    st.markdown(
        f"""
**Opportunity costs (Y per 1 X):** A = {OCx_A:.2f}, B = {OCx_B:.2f}  
**Comparative advantage:** {('A in X, B in Y' if ca_X=='A' else 'B in X, A in Y')}  
**Trade-line slope:** \(-P_x/P_y = -{px_over_py:.2f}\)  (a steeper line means X is relatively pricier).
        """
    )

    show_adv = st.toggle("Advanced (show equations)", key="comp_ad_adv")
    if show_adv:
        st.latex(r" \text{PPC}_A: \; y = a_y - \frac{a_y}{a_x} x \quad;\quad \text{PPC}_B: \; y = b_y - \frac{b_y}{b_x} x ")
        st.latex(r" \text{OC}_X^A = \frac{a_y}{a_x}, \quad \text{OC}_X^B = \frac{b_y}{b_x} \;\;\Rightarrow\;\; \text{CA in X} = \arg\min \text{OC}_X ")