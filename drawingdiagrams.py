
import pandas as pd
from graphviz import Digraph
import matplotlib.pyplot as plt

df = pd.read_csv("ranking.csv")

df.head()

f = Digraph('finite_state_machine', filename='MapMinddiagram.gv', format='png')

#f.attr('node', shape='doublecircle',fixedsize='true')

#f.attr(rankdir='LR', size='6,6')

for index, row in df.head(20).iterrows():
#    f.attr('node', shape='doublecircle',scale=str(row['Ocorrence']))
#    f.attr(rankdir='LR', )
#    f.attr('node', width='1', height='1')#str(row['Ocorrence']))
    f.attr('node', width=str(int(row['Ocorrence']*20/3154)), height=str(int(row['Ocorrence']*20/3154)))
    f.node(row['Palavras'])


dfm = pd.read_csv("matriz.csv")
fim=1
for index, row in dfm.iterrows():
    for i in range(0,fim-1,1):
        print(row.Palavras," ",dfm['Palavras'].iloc[i]," ",dfm[row.Palavras].iloc[i])
        if(dfm[row.Palavras].iloc[i] >40):
            f.edge(str(row.Palavras), str(dfm['Palavras'].iloc[i]),str(dfm[row.Palavras].iloc[i]))
    fim+=1
    



    
f.view()


def TopCitedPapers():

    data = pd.read_csv('Top20papers.data')
    dataT = data.T
    
    fig, ax = plt.subplots()
    
    for row in dataT[3:20]:
        ax.plot(dataT[3:20].iloc[::-1].index, dataT[row][3:20].iloc[::-1], label=str(data['Unnamed: 0'][row]))
        
    legend = ax.legend(loc='upper left')# shadow=True, fontsize='x-large')
    
    # Put a nicer background color on the legend.
    #legend.get_frame().set_facecolor('C0')
    plt.show()
