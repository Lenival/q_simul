
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

f.view()
