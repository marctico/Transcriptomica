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
col_up1 = 73 #Estudio 1
col_up2 = 0 #Estudio 2
#Consideraciones downregulate
#1- Seleccionar dos datasets
col_down1 = 73
col_down2 = 0

#Upregulate
df28_up = pd.read_excel(r'C:\Users\marcg\OneDrive\Escritorio\Marc\UNI\Nueva carpeta\TFG\python\Experimentos\Parkinson\mRNA-Seq\Output\mRNA seq v3 final.xlsx', sheet_name='upregulate2')
df29_up = pd.read_excel (r'C:\Users\marcg\OneDrive\Escritorio\Marc\UNI\Nueva carpeta\TFG\python\Experimentos\Parkinson\RNA seq de SNc y VTA\Output\RNA seq de VTA original_3_final.xlsx', sheet_name='up')
print (df28_up,df29_up)
df28_nomb_up = df28_up.iloc[:, col_up1] #seleccionar los nombres de los genes 
df28_list_up = df28_nomb_up.tolist()

df29_nomb_up = df29_up.iloc[:, col_up2] #seleccionar los nombres de los genes 
df29_list_up = df29_nomb_up.tolist()

nomb_up = []
for n in df28_list_up:
    m = n[0:15]
    z = m in df29_list_up
    if z is True:
        nomb_up.append (n)
print (nomb_up)
print (len(nomb_up))

#Downregulate
df28_down = pd.read_excel(r'C:\Users\marcg\OneDrive\Escritorio\Marc\UNI\Nueva carpeta\TFG\python\Experimentos\Parkinson\mRNA-Seq\Output\mRNA seq v3 final.xlsx', sheet_name='downregulate2')
df29_down = pd.read_excel (r'C:\Users\marcg\OneDrive\Escritorio\Marc\UNI\Nueva carpeta\TFG\python\Experimentos\Parkinson\RNA seq de SNc y VTA\Output\RNA seq de VTA original_3_final.xlsx', sheet_name='down')
print (df28_down,df29_down)
df28_nomb_down = df28_down.iloc[:, col_down1] #seleccionar los nombres de los genes 
df28_list_down = df28_nomb_down.tolist()

df29_nomb_down = df29_down.iloc[:, col_down2] #seleccionar los nombres de los genes 
df29_list_down = df29_nomb_down.tolist()

nomb_down = []
for l in df28_list_down:
    o = l[0:15]
    s = o in df29_list_down
    if s is True:
        nomb_down.append (l)
print (nomb_down)
print (len(nomb_down))