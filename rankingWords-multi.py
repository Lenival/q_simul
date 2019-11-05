
import timeit
import pandas as pd
import numpy as np
import multiprocessing 
from multiprocessing import Process, Manager, Value, Array, Lock
from ctypes import c_char_p
from itertools import islice

manager = Manager()

linhas = list() 
dicionario  = manager.dict()#Array(c_char_p, 80)
ocorrencias = manager.dict()#Array(c_char_p, 80)
numPalavras = manager.Value('i', 0)

with open('quantum-Comput-titles.text','r') as f: 
#    for line in islice(f, 1000):
    for line in f: 
        linhas.append(line) 

 

def montandoDicionario(line,dicionario,numPalavras, lock):
    my_replacement_dict = {"[": " ", "+":" ", "using": " ", "with": " ", "based": " ", "from": " ", "between":" "} 
#    print(dicionairio[:])
    for lines in line:
        for word in lines.split():
            if (len(word) > 3):
                for key, value in my_replacement_dict.items():
#                    print(".",key,".",word, ".") 
                    if (key == word.lower()):
#                        print("IGUAL!!!!!!!!!")
                        word = word.lower()
                        word = word.replace(key,value) 
#                        print("REMOVEU ?", word,".")
                with lock:
                    Tem = 0
                    for k in dicionario.items():
                        if   (word.lower() in str(k[1])):
                            Tem = 1
                    if (word == " "):
                        Tem = 1
                        
                    if (not Tem):
                        dicionario[numPalavras.value] = (word.lower())
#                       print("ADD.", dicionario[numPalavras.value], ".")
                        numPalavras.value += 1

                        
def procurandoOcorrencias(dicionario, ocorrencias,lock):
    for index, wordDic in dicionario:
        pal_count=0
        with open('quantum-Comput-titles.text','r') as f:
#            for line in islice(f, 200):
            for line in f:
                for word in line.split():
                    if (len(word) > 3):
                        if ( wordDic == word.lower()):
                            pal_count += 1
        with lock:
            ocorrencias[index] = pal_count
                            
  
if __name__ == '__main__': 
    jobs = [] 
 
    numcpus = 20

    final = int(np.size(linhas) - np.size(linhas)%numcpus)

    passos = int((np.size(linhas)-np.size(linhas)%numcpus)/numcpus)

    quebrados=0

    lock = Lock()
    
    start = timeit.timeit()
    for i in range(0,final,passos):
        p = multiprocessing.Process(target=montandoDicionario, args=(linhas[i:i+passos+quebrados],dicionario,numPalavras,lock)) 
        if (i == final-passos):
            quebrados = int(np.size(linhas)%numcpus)
        p.start()
        p.join()
#    print(dicionario)

    end = timeit.timeit()
    print(end-start)

    start = timeit.timeit()

    tamanhoDic = np.size(dicionario)

    final = int(tamanhoDic - tamanhoDic%numcpus)

    passos = int((tamanhoDic-tamanhoDic%numcpus)/numcpus)

    quebrados=0

    for i in range(0,final,passos):
        p = multiprocessing.Process(target=procurandoOcorrencias, args=(dicionario.items()[i:i+passos+quebrados],ocorrencias,lock)) 
        if (i == final-passos):
            quebrados = int(tamanhoDic%numcpus)
        p.start()
        p.join()

    end = timeit.timeit()
    print(end-start)
        

    df = pd.DataFrame([[row[1] for row in ocorrencias.items()], [row[1] for row in dicionario.items()[0:np.size(ocorrencias)]]])
    df = np.transpose(df)
    df.columns =['Ocorrence','Palavras']

    pd.set_option('display.max_rows', None)
                    
    df = df.sort_values(by='Ocorrence', ascending=False, na_position='first')

    df = df.reset_index()   

    print(df[0:200])
    df.to_csv('ranking.csv') 

        

#    for 
#    procs = [multiprocessing.Process(target=montandoDicionario, args=(linhas[i:i+5],numPalavras,lock))     
#



#def montandoDicionarioAUX(num,numPalavras,df): 
#    """thread worker function""" 
#    print('Worker:', num) 
#    return 


#        jobs.append(p) 
#        p.start()
#        p.join()
#        print(dicionario[:])
#                
#
#

#
#
#with open('quantum-Comput-titles.text','r') as f:
#    for line in f:
#        for word in line.split():
#            if (len(word) > 3):
#                if ( not np.size(df[df['Palavras'].str.contains(word)]) > 0 ):
#                    df.loc[i] = [word.lower(),0]
#                    i+=1
#dicionario = df
#
#df = pd.DataFrame([["Quantum Information", 0]], columns=['Palavras','Ocorrence'])
#prosseguindo=1
#i=1
#start = timeit.timeit()
#for index, wordDic in dicionario.iterrows():
#    pal_count=0
#    with open('quantum-Comput-titles.text','r') as f:
#        for line in f:
#            for word in line.split():
#                if (len(word) > 3):
#                    if ( wordDic.Palavras == word.lower()):
#                        pal_count += 1
#                        dicionario.Ocorrence[index] = pal_count
#                    
#end = timeit.timeit()
#print(end-start)
#df = dicionario.sort_values(by='Ocorrence', ascending=False, na_position='first')
#
#df.to_csv('ranking.csv') 
