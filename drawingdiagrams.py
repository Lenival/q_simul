
import pandas as pd
from graphviz import Digraph

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
<<<<<<< HEAD
        if(dfm[row.Palavras].iloc[i] > 40):
=======
        if(dfm[row.Palavras].iloc[i] > 60):
>>>>>>> 81be3a64a0adc92a9100ffb49a9e2f393528f42c
            f.edge(str(row.Palavras), str(dfm['Palavras'].iloc[i]),str(dfm[row.Palavras].iloc[i]))
    fim+=1
    



    
f.view()
