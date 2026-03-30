import plotly.graph_objects as go

nPaired = 114
a = 14
b = 4
c = 81
d = 15

flowLabels = [
    f"Positive → Positive: {a} ({100*a/nPaired:.1f}%)",
    f"Positive → Not positive: {b} ({100*b/nPaired:.1f}%)",
    f"Not positive → Positive: {c} ({100*c/nPaired:.1f}%)",
    f"Not positive → Not positive: {d} ({100*d/nPaired:.1f}%)"
]

fig = go.Figure(data=[go.Sankey(
    node=dict(
        pad=20,
        thickness=25,
        line=dict(width=0.5),
        label=[
            f"Before positive\n{a+b} ({100*(a+b)/nPaired:.1f}%)",
            f"Before not positive\n{c+d} ({100*(c+d)/nPaired:.1f}%)",
            f"After positive\n{a+c} ({100*(a+c)/nPaired:.1f}%)",
            f"After not positive\n{b+d} ({100*(b+d)/nPaired:.1f}%)"
        ]
    ),
    link=dict(
        source=[0, 0, 1, 1],
        target=[2, 3, 2, 3],
        value=[a, b, c, d],
        label=flowLabels
    )
)])

fig.update_layout(
    title_text="Before–After Perception Shift",
    font_size=12
)

fig.show()
