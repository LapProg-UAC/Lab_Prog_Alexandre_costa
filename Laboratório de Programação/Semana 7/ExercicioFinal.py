import seaborn as sns
import matplotlib.pyplot as plt
from bokeh.plotting import figure, show
from bokeh.layouts import column
import plotly.express as px
import pandas as pd

def criar_figura_completa():
    try:
        df_pinguins = pd.read_csv('pinguins_palmer.csv')
        df_co2 = pd.read_csv('co2_maunaloa.csv')
        
        df_pinguins['ano_estimado'] = ((df_pinguins['barbatana'] - 180) / 14).round() + 2010
        df_merged = pd.merge(df_pinguins, df_co2, left_on='ano_estimado', right_on='ano')

        fig = plt.figure(figsize=(18, 6))
        plt.style.use('seaborn-v0_8-whitegrid')

        # a) Imagem A posta à esquerda/topo é o resultado com plotly
        ax1 = fig.add_subplot(1, 3, 1)
        sns.scatterplot(data=df_pinguins, x="massa", y="barbatana", hue="especie", ax=ax1)
        ax1.legend(title="Espécie", loc='upper left', frameon=True)
        ax1.set_title("A: Massa do Pinguin vs Tamanho da Barbatana (Estilo Plotly)")
        ax1.set_xlabel("Massa do Pinguin (g)")
        ax1.set_ylabel("Tamanho da Barbatana (mm)")
        
        
        # b) Imagem B posta ao centro/meio é o resultado cpom bokeh
        ax2 = fig.add_subplot(1, 3, 2)
        ax2.plot(df_co2['ano'], df_co2['ppm'], color='red', marker='o', markerfacecolor='white', markersize=8)
        ax2.set_title("B: Valores de CO2 ao longo dos anos (Estilo Bokeh)")
        ax2.set_xlabel("Ano")
        ax2.set_ylabel("Nível de CO2 (PPM)")

        # c) Imagem C posta à direita/baixo é esta
        #1- Assumir que as barbatanas crescem 14mm por ano e que o comprimentos no ano 2010 é 180mm
        #2 - Fazer a estimativa da correlação entre "ganho de massa corporal per ano" e respetivo "nível de CO2 para esse ano"
        ax3 = fig.add_subplot(1, 3, 3)
        sns.regplot(data=df_merged, x="ppm", y="massa", ax=ax3, color='purple')
        ax3.set_title("C: Correlação Massa vs Valores de CO2 (Estilo Seaborn)")
        ax3.set_xlabel("Nível de CO2 (PPM)")
        ax3.set_ylabel("Massa Corporal (g)")

        plt.suptitle("Trabalho Final", fontsize=16, fontweight='bold')
        
        # d) Imagems A e B e C devem fazer parte duma única figura que é guardada num único ficheiro jpeg/png
        plt.tight_layout(rect=[0, 0.03, 1, 0.95])
        plt.savefig('ResultadoFinal.png', dpi=300)
        plt.show()
        
        print("Sucesso, a figura foi guardada.")

    except FileNotFoundError as e:
        print("Erro: Certifique-se que os ficheiros CSV estão na pasta.", e)

criar_figura_completa()