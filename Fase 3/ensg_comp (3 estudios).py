import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pingouin as pg
from scipy import stats
from rpy2.robjects.packages import importr
from rpy2.robjects.vectors import FloatVector

#CODIGO PARA COMPARAR GENE ID DE DOS DATASETS DISTINTOS
#Generar dos archivos en el excel, uno para up y otro para down
#Consideraciones upregulate
#1- Seleccionar dos datasets
col_up1 = 209 #Estudio 1
col_up2 = 73 #Estudio 2
col_up3 = 73 #Estudio 3
#Consideraciones downregulate
#1- Seleccionar dos datasets
col_down1 = 209
col_down2 = 73
col_down3 = 73

#Upregulate
df28_up = pd.read_excel(r'C:\Users\marcg\Documents\UNI\Nueva carpeta\TFG\python\Experimentos\Parkinson\115 RNA-Seq Post\output\115 RNA-Seq Post final v3 final.xlsx', sheet_name='upregulate')
df29_up = pd.read_excel (r'C:\Users\marcg\Documents\UNI\Nueva carpeta\TFG\python\Experimentos\Parkinson\Post mortem BA9 brain\output\post mortem BA9 brain original v3 final.xlsx', sheet_name='upregulate')
df30_up = pd.read_excel (r'C:\Users\marcg\Documents\UNI\Nueva carpeta\TFG\python\Experimentos\Parkinson\mRNA-Seq\Output\mRNA seq v3 final.xlsx', sheet_name='upregulate2')
print (df28_up,df29_up,df30_up)
df28_nomb_up = df28_up.iloc[:, col_up1] #seleccionar los nombres de los genes 
df28_list_up = df28_nomb_up.tolist()

df29_nomb_up = df29_up.iloc[:, col_up2] #seleccionar los nombres de los genes 
df29_list_up = df29_nomb_up.tolist()

df30_nomb_up = df30_up.iloc[:, col_up3] #seleccionar los nombres de los genes 
df30_list_up = df30_nomb_up.tolist()
print (df28_nomb_up)
print (df29_nomb_up)
print (df30_nomb_up)
nomb_up = []
for n in df28_list_up:
    m = n[0:15]
    z = m in df29_list_up
    if z is True:
        nomb_up.append (n)

nomb_up2=[]
for n in nomb_up:
    m = n[0:15]
    z = m in df30_list_up
    if z is True:
        nomb_up2.append (n)

print (nomb_up2)
print (len(nomb_up2))

#Downregulate
df28_down = pd.read_excel(r'C:\Users\marcg\Documents\UNI\Nueva carpeta\TFG\python\Experimentos\Parkinson\115 RNA-Seq Post\output\115 RNA-Seq Post final v3 final.xlsx', sheet_name='downregulate')
df29_down = pd.read_excel (r'C:\Users\marcg\Documents\UNI\Nueva carpeta\TFG\python\Experimentos\Parkinson\Post mortem BA9 brain\output\post mortem BA9 brain original v3 final.xlsx', sheet_name='downregulate')
df30_down = pd.read_excel (r'C:\Users\marcg\Documents\UNI\Nueva carpeta\TFG\python\Experimentos\Parkinson\mRNA-Seq\Output\mRNA seq v3 final.xlsx', sheet_name='downregulate2')
print (df28_down,df29_down,df30_down)
df28_nomb_down = df28_down.iloc[:, col_down1] #seleccionar los nombres de los genes 
df28_list_down = df28_nomb_down.tolist()

df29_nomb_down = df29_down.iloc[:, col_down2] #seleccionar los nombres de los genes 
df29_list_down = df29_nomb_down.tolist()

df30_nomb_down = df30_down.iloc[:, col_down3] #seleccionar los nombres de los genes 
df30_list_down = df30_nomb_down.tolist()

nomb_down = []
for l in df28_list_down:
    o = l[0:15]
    s = o in df29_list_down
    if s is True:
        nomb_down.append (l)

nomb_down2 = []
for l in nomb_down:
    o = l[0:15]
    s = o in df30_list_down
    if s is True:
        nomb_down2.append (l)

print (nomb_down2)
print (len(nomb_down2))