import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

df = pd.read_csv("superstore.csv")
df = df.dropna()

cfg = {'displayModeBar': False}

pie_df = df.groupby('Region')['Sales'].sum().reset_index()
fig_pie = px.pie(pie_df, values='Sales', names='Region', title='Pie Chart - Ventas por Region')
fig_pie.write_html('pie.html', config=cfg)

sunburst_df = df.groupby(['Region', 'Category', 'Sub-Category'])['Sales'].sum().reset_index()
fig_sunburst = px.sunburst(sunburst_df, path=['Region', 'Category', 'Sub-Category'], values='Sales', title='Sunburst Chart')
fig_sunburst.write_html('sunburst.html', config=cfg)

df_mekko = df.groupby(['Segment', 'Category'])['Sales'].sum().unstack(fill_value=0)
segment_totals = df_mekko.sum(axis=1)
widths = segment_totals / segment_totals.sum()
df_pct = df_mekko.div(segment_totals, axis=0) * 100

x_edges = np.cumsum([0] + list(widths[:-1]))
x_centers = x_edges + widths / 2

fig_mekko = go.Figure()
bottoms = np.zeros(len(df_pct))

for cat in df_pct.columns:
    values = df_pct[cat].values
    fig_mekko.add_trace(go.Bar(
        name=cat,
        x=x_centers,
        y=values,
        width=widths,
        base=bottoms
    ))
    bottoms += values

fig_mekko.update_layout(
    title='Marimekko Chart',
    barmode='stack',
    xaxis=dict(
        tickvals=list(x_centers),
        ticktext=list(df_pct.index),
        title='Segmento'
    ),
    yaxis=dict(title='Porcentaje'),
    legend_title='Categoria'
)
fig_mekko.write_html('marimekko.html', config=cfg)