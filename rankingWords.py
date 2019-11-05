
import timeit
import pandas as pd
import numpy as np

df = pd.DataFrame([["Quantum Information", 0]], columns=['Palavras','Ocorrence'])
i=1

my_replacement_dict = {"[": "", "+":""} 

with open('quantum-Comput-titles.text','r') as f:
    for line in f:
        for word in line.split():
            if (len(word) > 3):
                for key, value in my_replacement_dict.items(): 
                    word = word.replace(key,value) 
                if ( not np.size(df[df['Palavras'].str.contains(word)]) > 0 ):
                    df.loc[i] = [word.lower(),0]
                    i+=1
dicionario = df

df = pd.DataFrame([["Quantum Information", 0]], columns=['Palavras','Ocorrence'])
prosseguindo=1
i=1
start = timeit.timeit()
for index, wordDic in dicionario.iterrows():
    pal_count=0
    with open('quantum-Comput-titles.text','r') as f:
        for line in f:
            for word in line.split():
                if (len(word) > 3):
                    if ( wordDic.Palavras == word.lower()):
                        pal_count += 1
                        dicionario.Ocorrence[index] = pal_count
                    
end = timeit.timeit()
print(end-start)
df = dicionario.sort_values(by='Ocorrence', ascending=False, na_position='first')

df.to_csv('ranking.csv') 
