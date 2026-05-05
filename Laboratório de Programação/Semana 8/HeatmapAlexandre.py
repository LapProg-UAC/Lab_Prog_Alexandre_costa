import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from bokeh.plotting import figure
import panel as pn #Biblioteca Adicional

pn.extension('plotly')

eixo_tempo = np.linspace(0, 10, 500)
onda_seno = np.sin(eixo_tempo)
onda_cosseno = np.cos(eixo_tempo)

dados_sinais = pd.DataFrame({
    "Seno": onda_seno,
    "Cosseno": onda_cosseno
})

fig_sns, ax = plt.subplots(figsize=(5, 4))
sns.heatmap(dados_sinais.corr(), annot=True, cmap="coolwarm", ax=ax)
ax.set_title("Correlação dos Sinais")
plt.close(fig_sns)

fig_plotly = go.Figure()
fig_plotly.add_trace(go.Scatter(x=eixo_tempo, y=onda_seno, name='Seno (V)', line=dict(color='firebrick')))
fig_plotly.add_trace(go.Scatter(x=eixo_tempo, y=onda_cosseno, name='Cosseno (I)', line=dict(color='royalblue')))
fig_plotly.update_layout(title="Análise Plotly", height=350, margin=dict(l=10, r=10, t=40, b=10))

fig_bokeh = figure(title="Análise Bokeh", height=350, x_axis_label='Tempo', y_axis_label='Amplitude')
fig_bokeh.line(eixo_tempo, onda_seno, legend_label="Seno", color="green", line_width=2)
fig_bokeh.line(eixo_tempo, onda_cosseno, legend_label="Cosseno", color="purple", line_width=2)
fig_bokeh.legend.click_policy = "hide"

layout_final = pn.Column(
    "## Todos os gráficos pedidos",
    pn.Row(
        pn.Column("### Heatmap (Seaborn)", fig_sns),
        pn.Column("### Interativo (Plotly)", fig_plotly),
        pn.Column("### Interativo (Bokeh)", fig_bokeh)
    )
)

layout_final.show()