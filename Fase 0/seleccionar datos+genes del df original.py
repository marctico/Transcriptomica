import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pingouin as pg
from scipy import stats
from rpy2.robjects.packages import importr
from rpy2.robjects.vectors import FloatVector
#CODIGO PARA COGER SOLO LOS DATOS DE LOS GENES QUE COINCIDEN ENTRE EL OUTPUT DE ENSEMBL Y LA LISTA ORIGINAL 
#Consideraciones:
#El excel debe tener este formato:
    #Dataframe original
    #Lista de genes de ensembl

#input Dataframe
rep_counts_start = 0
rep_counts_end = 11
gene_counts_start = 0
gene_counts_end = 55618
#input lista de genes
rep_gene_start = 0
gene_start = 0
gene_end = 54623


df= pd.read_excel(r'C:\Users\marcg\Documents\UNI\Nueva carpeta\TFG\python\Experimentos\Parkinson\Transcriptomic profiling\Excel original\Transcriptomic profiling original.xlsx', sheet_name='longene') 
df1 = pd.read_excel(r'C:\Users\marcg\Documents\UNI\Nueva carpeta\TFG\python\Experimentos\Parkinson\Transcriptomic profiling\Excel original\Transcriptomic profiling original putamen.xlsx', sheet_name='counts')
print (df)
print (df1)

#celdas
#original
df1_1 = df1.iloc [gene_counts_start:gene_counts_end, rep_counts_start:rep_counts_end]
df1_2= np.array(df1_1)
df1_3 = list (df1_2)
df1_4 = []
for a in df1_3:
    b = list(a)
    df1_4.append(b)
print(df1_1)
#lista de los genes que faltan
df_1 = df.iloc[gene_start:gene_end, rep_gene_start]
df_2 = list (df_1)
print (df_1)
output=[]

for a in df1_4:
    b= a[0]
    c = b in df_2
    if c is True:
        output.append (a)

output1 = pd.DataFrame (output)
print(output1)
df5 = output1.to_excel (r'C:\Users\marcg\Documents\UNI\Nueva carpeta\TFG\python\Output\Archivo final.xlsx')
