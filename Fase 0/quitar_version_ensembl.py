import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pingouin as pg
from scipy import stats
from rpy2.robjects.packages import importr
from rpy2.robjects.vectors import FloatVector
import csv

df= pd.read_excel(r'C:\Users\marcg\Documents\UNI\Nueva carpeta\TFG\python\Experimentos\Parkinson\PKRN_hermanos\Excel original\PRKN_hermanos original.xlsx', sheet_name='11d')
print (df)

#Consideraciones
#1- Los datos deben de estar en: 
    #Vertical: Genes Ensembl ID + version
    #Ubicar los Gene ID en la columna A con un índice encima como 'Ensembl ID'
    #Horizontal: Réplicas
    #Los datos se pueden coger del propio excel original

#input del Dataframe(se tiene que poner una lista en la columna A)
#Ensembl ID
gene_start=0
gene_end=57785
ensembl_id= 0

#Celdas
a = df.iloc[gene_start:gene_end, ensembl_id]
ensembl_version = list (a)

#Quitar las versiones
ensembl = []
for n in ensembl_version:
    m = n[0:15]
    ensembl.append (m)

ensembl_df = pd.DataFrame (ensembl)
print (ensembl_df)
ensembl_df.to_excel(r'C:\Users\marcg\Documents\UNI\Nueva carpeta\TFG\python\Output\ttt.xlsx')
