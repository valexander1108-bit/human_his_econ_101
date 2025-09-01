# apps/common.py
from dataclasses import dataclass
import plotly.graph_objects as go

@dataclass
class Line:     # P = a + bQ
    a: float
    b: float

def line_y(line: Line, q):
    return line.a + line.b*q

def intersect(d, s):
    den = (s.b - d.b)
    if abs(den) < 1e-9:
        return float("nan"), float("nan")
    q_star = (d.a - s.a) / den
    p_star = line_y(d, q_star)
    return float(q_star), float(p_star)

def base_fig(xmax=100, ymax=100, x_title="Quantity (Q)", y_title="Price (P)"):
    fig = go.Figure()
    fig.update_layout(
        margin=dict(l=40, r=20, t=20, b=40),
        xaxis_title=x_title, yaxis_title=y_title,
        xaxis=dict(range=[0, xmax], zeroline=False),
        yaxis=dict(range=[0, ymax], zeroline=False),
        height=520,
    )
    return fig

def add_line(fig, line: Line, name, q0=0, q1=100, dash=None):
    fig.add_trace(go.Scatter(
        x=[q0, q1],
        y=[line_y(line, q0), line_y(line, q1)],
        mode="lines", name=name,
        line=dict(dash=dash) if dash else None
    ))
    return fig

def add_point(fig, q, p, label):
    fig.add_trace(go.Scatter(x=[q], y=[p], mode="markers+text",
                             text=[label], textposition="top center"))