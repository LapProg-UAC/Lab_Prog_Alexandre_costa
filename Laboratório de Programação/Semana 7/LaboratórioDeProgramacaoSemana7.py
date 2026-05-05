import matplotlib.pyplot as plt
import seaborn as sns
from bokeh.plotting import figure, output_file, show
from bokeh.layouts import column
import plotly.express as px
from math import sin, pi
import numpy as np
import ssl

ssl._create_default_https_context = ssl._create_unverified_context

def co2_emissao(ax):
    try:
        with open('co2_maunaloa.csv', 'r') as wb:
            linhas = wb.readlines()
            ano, co2 = [], []
            for c in linhas[1:]:
                dados = c.strip().split(',')
                ano.append(int(dados[0]))
                co2.append(float(dados[1]))

        ax.plot(ano, co2, color="green")
        ax.set_xlabel("Ano")
        ax.set_ylabel("PPM de CO2")
        ax.set_title("Emissão de CO2")
        ax.grid(True)
        
    except FileNotFoundError:
        ax.set_title("Arquivo CO2 não encontrado")

def pinguins(ax):
    try: 
        with open('pinguins_palmer.csv', 'r') as wb2:
            linhas2 = wb2.readlines()
            massa, barbatana, especie = [], [], []
            colors = {"Adelie": 'skyblue', "Chinstrap": 'lightcoral', "Gentoo": 'lightgreen'}
            for i in linhas2[1:]:
                dados2 = i.strip().split(',')
                massa.append(float(dados2[0]))
                barbatana.append(float(dados2[1]))
                especie.append(dados2[2])
    
        ax.scatter(massa, barbatana, c=[colors.get(esp, 'gray') for esp in especie], alpha=0.5)
        ax.set_xlabel("Massa (g)")
        ax.set_ylabel("Barbatana (mm)")
        ax.set_title("Pinguins: Massa vs Barbatana")
        ax.grid(True)
        
    except FileNotFoundError:
        ax.set_title("Arquivo Pinguins não encontrado")

def veiculos(ax):
    try:
        with open('mpg_epa.csv', 'r') as wb3:
            linhas3 = wb3.readlines()
            mpg = [float(n.strip().split(',')[0]) for n in linhas3[1:]]

        ax.hist(mpg, bins=6, color='red', edgecolor='black')
        ax.set_xlabel("MPG")
        ax.set_ylabel("Frequência")
        ax.set_title("Eficiência MPG")
        ax.grid(True)
        
    except FileNotFoundError:
        ax.set_title("Arquivo MPG não encontrado")

def seabornexemplo(ax):
    tips = sns.load_dataset("tips")
    sns.histplot(tips["total_bill"], bins=20, kde=False, color='purple', ax=ax)
    ax.set_title("Seaborn: Total da Conta")
    ax.set_xlabel("Total")
    ax.grid(True)

def plotlyexemplo():
    df = px.data.iris() 
    fig = px.scatter_matrix(df, dimensions=["sepal_width", "sepal_length", "petal_width", "petal_length"], color="species")
    fig.show()
    
def bokehexemplo():
    x = np.arange(-2*pi, 2*pi, 0.1)
    y = [sin(i) for i in x]
    p = figure(title="Sine Wave Example")
    p.line(x, y)
    show(column(p))
    
def criar_figura_completa():
    plt.style.use('seaborn-v0_8-darkgrid')
    
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    fig.suptitle("Gráficos muito porreiros", fontsize=20, fontweight='bold')
    
    co2_emissao(axes[0, 0])
    pinguins(axes[0, 1])
    veiculos(axes[1, 0])
    seabornexemplo(axes[1, 1])
    
    plt.tight_layout()
    plt.show()

criar_figura_completa()
plotlyexemplo()
bokehexemplo()
    