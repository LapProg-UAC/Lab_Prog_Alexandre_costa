import seaborn as sns
import matplotlib.pyplot as plt
from bokeh.plotting import figure, show
from bokeh.layouts import column
import plotly.express as px
import pandas as pd
import numpy as np

def seabornexemplo():
    try:
        x = []
        with open('mpg_epa.csv', 'r') as wb:
            linhas = wb.readlines()
            for c in linhas[1:]:
                val = c.strip()
                if val:
                    x.append(float(val))
        
        fig, ax = plt.subplots(figsize=(8, 4))
        sns.histplot(x, kde=True, color='purple', ax=ax)
        ax.set_title("Seaborn: MPG Distribution (mpg_epa.csv)")
        ax.set_xlabel("Miles Per Gallon")
        ax.grid(True)
        plt.show()
        
    except FileNotFoundError:
        print("Error: mpg_epa.csv not found.")
    except Exception as e:
        print(f"An error occurred in Seaborn: {e}")

def plotlyexemplo():
    try:
        df = pd.read_csv('pinguins_palmer.csv')
        
        fig = px.scatter(df, 
                         x="massa", 
                         y="barbatana", 
                         color="especie",
                         title="Plotly: Penguin Mass vs Fin Length",
                         labels={"massa": "Body Mass (g)", "barbatana": "Flipper Length (mm)"})
        fig.show()
        
    except FileNotFoundError:
        print("Error: pinguins_palmer.csv not found.")
    except Exception as e:
        print(f"An error occurred in Plotly: {e}")
        
def bokehexemplo():
    try:
        df = pd.read_csv('co2_maunaloa.csv')
        
        p = figure(title="CO2 Levels Over Time (co2_maunaloa.csv)", 
                   x_axis_label='Year', 
                   y_axis_label='PPM')
        
        p.line(df['ano'], df['ppm'], line_width=2, color="red", legend_label="CO2 PPM")
        p.circle(df['ano'], df['ppm'], fill_color="white", size=8)
        
        show(column(p))
        
    except FileNotFoundError:
        print("Error: co2_maunaloa.csv not found.")
    except Exception as e:
        print(f"An error occurred in Bokeh: {e}")

seabornexemplo()
plotlyexemplo()
bokehexemplo()