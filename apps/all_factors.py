import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from apps.common import apply_grid


def production(a, labor, capital, alpha):
    return a * (capital ** alpha) * (labor ** (1 - alpha))


def app():
    st.subheader("Factors of Production: Production, MP, AP, and Derived Demand")

    horizon = st.sidebar.radio("Time horizon", ["Short run: capital fixed", "Long run: labor and capital vary"])
    a = st.sidebar.slider("Technology", 0.50, 5.00, 1.40, 0.05)
    alpha = st.sidebar.slider("Capital share", 0.10, 0.80, 0.35, 0.05)
    fixed_capital = st.sidebar.slider("Capital stock", 1.0, 200.0, 50.0, 1.0)
    output_price = st.sidebar.slider("Output price", 1.0, 30.0, 8.0, 0.5)
    wage = st.sidebar.slider("Wage", 1.0, 100.0, 30.0, 1.0)

    labor = np.linspace(1, 160, 320)
    if horizon.startswith("Short"):
        capital = np.full_like(labor, fixed_capital)
    else:
        capital = fixed_capital * (labor / 50) ** 0.45

    total_product = production(a, labor, capital, alpha)
    average_product = total_product / labor
    marginal_product = np.gradient(total_product, labor)
    mrp_labor = output_price * marginal_product
    hire_idx = np.argmin(np.abs(mrp_labor - wage))
    hire_labor = labor[hire_idx]

    tab1, tab2 = st.tabs(["Production", "Derived demand"])
    with tab1:
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=labor, y=total_product, name="Total product", line=dict(width=4, color="#1d511e")))
        fig.add_trace(go.Scatter(x=labor, y=average_product, name="Average product", yaxis="y2", line=dict(width=3, color="#33658A")))
        fig.add_trace(go.Scatter(x=labor, y=marginal_product, name="Marginal product", yaxis="y2", line=dict(width=3, color="#C49A6C")))
        fig.update_layout(
            height=540,
            yaxis=dict(title="Total product"),
            yaxis2=dict(title="AP and MP", overlaying="y", side="right"),
            legend=dict(orientation="h", y=1.08, x=0),
            plot_bgcolor="white",
            paper_bgcolor="white",
        )
        fig.update_xaxes(title="Labor")
        apply_grid(fig)
        st.plotly_chart(fig, use_container_width=True, key="factors_production_chart")

    with tab2:
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=labor, y=mrp_labor, name="MRP of labor", line=dict(width=4, color="#1d511e")))
        fig.add_trace(go.Scatter(x=labor, y=np.full_like(labor, wage), name="Wage", line=dict(width=3, color="#B38210", dash="dash")))
        fig.add_trace(go.Scatter(x=[hire_labor], y=[wage], mode="markers+text", text=["hire until MRP=w"], textposition="top center", marker=dict(size=12, color="#B38210"), name="Hiring rule"))
        fig.update_xaxes(title="Labor")
        fig.update_yaxes(title="Dollars")
        fig.update_layout(height=540, legend=dict(orientation="h", y=1.08, x=0), plot_bgcolor="white", paper_bgcolor="white")
        apply_grid(fig)
        st.plotly_chart(fig, use_container_width=True, key="factors_mrp_chart")

    current = pd.DataFrame(
        {
            "Measure": ["Labor hired", "Output", "AP at hiring point", "MP at hiring point", "MRP at hiring point"],
            "Value": [
                hire_labor,
                total_product[hire_idx],
                average_product[hire_idx],
                marginal_product[hire_idx],
                mrp_labor[hire_idx],
            ],
        }
    )
    st.dataframe(current.round(3), hide_index=True, use_container_width=True)

    if st.toggle("Full analysis", value=False, key="factors_core_analysis"):
        st.markdown(
            "This page treats production as a micro decision by the firm. In the short run, capital is fixed and labor is variable. The firm compares the value of the marginal product of labor to the wage. In the long run, more inputs can adjust, so complementarities between capital and labor shift productivity."
        )
        st.latex(r"Q=A K^\alpha L^{1-\alpha}")
        st.latex(r"AP_L=Q/L,\quad MP_L=\Delta Q/\Delta L,\quad MRP_L=P\times MP_L")
