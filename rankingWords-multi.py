
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
#    for line in islice(f, 100):
    for line in f: 
        linhas.append(line) 

 

def montandoDicionario(line,dicionario,numPalavras, lock):
    for lines in line:
        for word in lines.split():
            if (len(word) > 3):
                with open('Dic-delete-words.text','r') as f: 
                    for lineRem in f: 
                        for key in lineRem.split():
                            if (key == word.lower() or key in word.lower()):
                                word = word.lower()
                                word = word.replace(key," ")
                with lock:
                    Tem = 0
                    for k in dicionario.items():
                        if (word.lower() in str(k[1])):
                            Tem = 1
                    if (" " in word):
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
#                for word in line.split():
#                    if (len(word) > 3):
                if ( wordDic in line.lower()):
                    pal_count += 1
        with lock:
            ocorrencias[index] = pal_count
                            

def montantoMatrixOcorrenciasCruzadas(palavrasTop):
    cruzados = np.zeros((20,20))
    for indexA, wordDicA  in enumerate(palavrasTop.Palavras):
        for indexB, wordDicB in enumerate(palavrasTop.Palavras):
            pal_count=0
            with open('quantum-Comput-titles.text','r') as f:
                for line in f:
                    if ( wordDicA in line.lower() and wordDicB in line.lower()):
                        pal_count += 1
            cruzados[indexA][indexB]=pal_count

if __name__ == '__main__': 
    jobs = [] 

    with open('Dic-compound-words.text','r') as f: 
        for line in f: 
            dicionario[numPalavras.value] = (line.lower().rstrip())
            numPalavras.value += 1
 
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

    end = timeit.timeit()
    print(end-start)

#    print(dicionario)

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
    df.to_csv('ranking-test.csv') 

    palavrasTop = df.head(20) 

    cruzados = np.zeros((20,20)) 
    for indexA, wordDicA  in enumerate(palavrasTop.Palavras): 
        for indexB, wordDicB in enumerate(palavrasTop.Palavras): 
            pal_count=0 
            with open('quantum-Comput-titles.text','r') as f: 
                for line in f: 
                    if ( wordDicA in line.lower() and wordDicB in line.lower()): 
                        pal_count += 1 
            cruzados[indexA][indexB]=pal_count 
  
    DFcruzados = pd.DataFrame(cruzados)  
    DFcruzados.columns=[i for i in palavrasTop.Palavras] 
    DFcruzados["Palavras"] = [i for i in palavrasTop.Palavras] 
    cols = DFcruzados.columns.tolist()
    cols = cols[-1:] + cols[:-1]                                                                                                                                                                
    DFcruzados = DFcruzados[cols] 

    print(DFcruzados)
    DFcruzados.to_csv('matriz-test.csv') 
