import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

import plotly.graph_objects as go
from bokeh.plotting import figure, show

t = np.linspace(0, 10, 400)
y1 = np.sin(t)
y2 = np.cos(t)

df = pd.DataFrame({
    "y1": y1,
    "y2": y2
})


corr = df.corr()
print(corr)

# Matriz da correlação
plt.figure()
sns.heatmap(corr, annot=True, cmap="coolwarm")
plt.title("Matriz de Correlação")
plt.show()


# Gráfico com plotly
fig = go.Figure()

fig.add_trace(go.Scatter(x=t, y=y1, mode='lines', name='sin(t)'))
fig.add_trace(go.Scatter(x=t, y=y2, mode='lines', name='cos(t)'))

fig.update_layout(title="Sinais (Plotly)",
                  xaxis_title="t",
                  yaxis_title="Amplitude")

fig.show()

# Gráfico com bokeh
p = figure(title="Sinais (Bokeh)",
           x_axis_label='t',
           y_axis_label='Amplitude')

p.line(t, y1, legend_label="sin(t)")
p.line(t, y2, legend_label="cos(t)")

show(p)