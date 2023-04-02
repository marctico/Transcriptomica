import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pingouin as pg
from scipy import stats
from rpy2.robjects.packages import importr
from rpy2.robjects.vectors import FloatVector
import xlsxwriter

#CODIGO PARA COMPARAR GENE ID DE DOS DATASETS DISTINTOS
#Generar dos archivos en el excel, uno para up y otro para down
#Consideraciones upregulate
#1- Seleccionar dos datasets
col_up1 = 209 #Estudio 1
col_up2 = 73 #Estudio 2
col_up3 = 
#Consideraciones downregulate
#1- Seleccionar dos datasets
col_down1 = 209 #Estudio 1
col_down2 = 73 #Estudio 2
col_down3 = 
#IMPORTANTE: 
    #La primera columna del dataframe obtenido del análisis estadístico (columna con indices del 0 a n)
    #debe ser eliminada en el dataframe de up y down
    #Todos los genes de cada dataframe tienen que tener la misma nomenclatura

#Estudio 1 y 2 original
df28_original=pd.read_excel(r'C:\Users\marcg\Documents\UNI\Nueva carpeta\TFG\python\Experimentos\Parkinson\115 RNA-Seq Post\Excel original\Table S1_1.xlsx',sheet_name='Hoja2')
df29_original= pd.read_excel(r'C:\Users\marcg\Documents\UNI\Nueva carpeta\TFG\python\Experimentos\Parkinson\Post mortem BA9 brain\Excel original\post mortem BA9 brain original.xlsx',sheet_name='Hoja2')
df30_original = 
#print (df28_original,df29_original,df30_original)

#Estudio 1 y 2 despues del análisis estadístico
#up
df28_up = pd.read_excel(r'C:\Users\marcg\Documents\UNI\Nueva carpeta\TFG\python\Experimentos\Parkinson\115 RNA-Seq Post\output\115 RNA-Seq Post final v3 final.xlsx', sheet_name='upregulate_name')
df29_up = pd.read_excel (r'C:\Users\marcg\Documents\UNI\Nueva carpeta\TFG\python\Experimentos\Parkinson\Post mortem BA9 brain\output\post mortem BA9 brain original v3 final.xlsx', sheet_name='upregulate')
df30_up = 
#print (df28_up,df29_up,df30_up)
#down
df28_down = pd.read_excel(r'C:\Users\marcg\Documents\UNI\Nueva carpeta\TFG\python\Experimentos\Parkinson\115 RNA-Seq Post\output\115 RNA-Seq Post final v3 final.xlsx', sheet_name='downregulate_name')
df29_down = pd.read_excel (r'C:\Users\marcg\Documents\UNI\Nueva carpeta\TFG\python\Experimentos\Parkinson\Post mortem BA9 brain\output\post mortem BA9 brain original v3 final.xlsx', sheet_name='downregulate')
df30_down = 
#print (df28_down,df29_down,df30_down)

#Estudio 1 y 2 después del análisis estadístico
df28 = pd.read_excel(r'C:\Users\marcg\Documents\UNI\Nueva carpeta\TFG\python\Experimentos\Parkinson\115 RNA-Seq Post\output\115 RNA-Seq Post final v3 final.xlsx', sheet_name='Sheet2') 
df29 = pd.read_excel (r'C:\Users\marcg\Documents\UNI\Nueva carpeta\TFG\python\Experimentos\Parkinson\Post mortem BA9 brain\output\post mortem BA9 brain original v3 final.xlsx', sheet_name='Sheet1')
df30 = 
#print (df28,df29,df30)

#CODIGO PARA COGER SOLO LOS DATOS DE LOS GENES QUE COINCIDEN ENTRE EL OUTPUT DE ENSEMBL Y LA LISTA ORIGINAL 
#Consideraciones:
#El excel debe tener este formato:
    #Dataframe obtenido del análisis estadístico 
    #Lista de genes de ensembl

#Estudio 1 (up/down)
#input Dataframe
rep_counts_start = 0
rep_counts_end = df28.shape[1]
gene_counts_start = 0
gene_counts_end = df28.shape[0]
ubi_col_gene = col_up1 + 1

#Estudio 2 (up/down)
#input Dataframe
rep_counts_start2 = 0
rep_counts_end2 = df29.shape[1]
gene_counts_start2 = 0
gene_counts_end2 = df29.shape[0]
ubi_col_gene2 = col_up2 + 1

#Estudio 3 (up/down)
#input Dataframe
rep_counts_start3 = 0
rep_counts_end3 = df30.shape[1]
gene_counts_start3 = 0
gene_counts_end3 = df30.shape[0]
ubi_col_gene3 = col_up3 + 1
################################################################################################################
#Upregulate
df28_nomb_up = df28_up.iloc[:, col_up1] #seleccionar los nombres de los genes 
df28_list_up = df28_nomb_up.tolist()

df29_nomb_up = df29_up.iloc[:, col_up2] #seleccionar los nombres de los genes 
df29_list_up = df29_nomb_up.tolist()

df30_nomb_up = df30_up.iloc[:, col_up3] #seleccionar los nombres de los genes 
df30_list_up = df30_nomb_up.tolist()

#obtener lista de gene id sin versión (ENSG00)
nomb_up = []
for n in df29_list_up:
    m = n[0:15]
    z = m in df28_list_up
    if z is True:
        nomb_up.append (m)
#print (nomb_up)
nomb_up_df = pd.DataFrame (nomb_up)

nomb_up2=[]
for n in nomb_up:
    m = n[0:15]
    z = m in df30_list_up
    if z is True:
        nomb_up2.append (n)

#obtener lista de gene id con versión (ENSG000.1)
nomb_up_version = []
for n in df29_list_up:
    m = n[0:15]
    z = m in df28_list_up
    if z is True:
        nomb_up_version.append (n)

#Seleccionar datos de los DEG
#Estudio 1
#DataFrame original
df1_1 = df28.iloc [gene_counts_start:gene_counts_end, rep_counts_start:rep_counts_end]
df1_2= np.array(df1_1)
df1_3 = list (df1_2)
df1_4 = []
for a in df1_3:
    b = list(a)
    df1_4.append(b)

#Filtrar la lista de DEG en el dataframe
output_est1_up=[]
for a in df1_4:
    b= a[ubi_col_gene]
    c = b in nomb_up2
    if c is True:
        output_est1_up.append (a)

output1_up = pd.DataFrame (output_est1_up)

#Estudio 2
#DataFrame original
df1_5 = df29.iloc [gene_counts_start2:gene_counts_end2, rep_counts_start2:rep_counts_end2]
df1_6= np.array(df1_5)
df1_7 = list (df1_6)
df1_8 = []
for a in df1_7:
    b = list(a)
    df1_8.append(b)

#Filtrar la lista de DEG en el dataframe
output_est2_up=[]
for a in df1_8:
    b= a[ubi_col_gene2]
    c = b in nomb_up2
    if c is True:
        output_est2_up.append (a)

output2_up = pd.DataFrame (output_est2_up)

#Estudio 3
#DataFrame original
df1_9 = df30.iloc [gene_counts_start3:gene_counts_end3, rep_counts_start3:rep_counts_end3]
df1_10= np.array(df1_9)
df1_11 = list (df1_10)
df1_12 = []
for a in df1_11:
    b = list(a)
    df1_12.append(b)

#Filtrar la lista de DEG en el dataframe
output_est3_up=[]
for a in df1_12:
    b= a[ubi_col_gene3]
    c = b in nomb_up2
    if c is True:
        output_est3_up.append (a)

output3_up = pd.DataFrame (output_est3_up)
#############################################################################################################
#Downregulate
df28_nomb_down = df28_down.iloc[:, col_down1] #seleccionar los nombres de los genes 
df28_list_down = df28_nomb_down.tolist()

df29_nomb_down = df29_down.iloc[:, col_down2] #seleccionar los nombres de los genes 
df29_list_down = df29_nomb_down.tolist()

df30_nomb_down = df30_down.iloc[:, col_down3] #seleccionar los nombres de los genes 
df30_list_down = df30_nomb_down.tolist()

#obtener lista de gene id sin versión (ENSG00)
nomb_down = []
for l in df29_list_down:
    o = l[0:15]
    s = o in df28_list_down
    if s is True:
        nomb_down.append (o)
#print (nomb_down)
nomb_down_df = pd.DataFrame (nomb_down)

nomb_down2 = []
for l in nomb_down:
    o = l[0:15]
    s = o in df30_list_down
    if s is True:
        nomb_down2.append (l)


#Seleccionar datos de los DEG
#Estudio 1
#Filtrar la lista de DEG en el dataframe
output_est1_down=[]
for a in df1_4:
    b= a[ubi_col_gene]
    c = b in nomb_down2
    if c is True:
        output_est1_down.append (a)

output1_down = pd.DataFrame (output_est1_down)

#Estudio 2
#DataFrame original
#Filtrar la lista de DEG en el dataframe
output_est2_down=[]
for a in df1_8:
    b= a[ubi_col_gene2]
    c = b in nomb_down2
    if c is True:
        output_est2_down.append (a)

output2_down = pd.DataFrame (output_est2_down)

#Estudio 3
#DataFrame original
#Filtrar la lista de DEG en el dataframe
output_est3_down=[]
for a in df1_12:
    b= a[ubi_col_gene3]
    c = b in nomb_down2
    if c is True:
        output_est3_down.append (a)

output3_down = pd.DataFrame (output_est3_down)

#################################################################################################################
#Añadir títulos a las columnas

lista =['Ensembl','pvalue','pvalue adjust','Promedio control','Promedio tratado','Desv.est control','Desv.est tratado','FC']

    #Estudio 1
tit_est1_1 = df28_original.columns.values
tit_est1_2 = list (tit_est1_1)
tit_est1 = tit_est1_2 [0:]
tit_est1_list = list(tit_est1)
for a in lista:
    tit_est1_list.append (a)
tit_est1_df = pd.DataFrame (tit_est1_list)
tit_est1_df2 = tit_est1_df.transpose()
up1= pd.concat([tit_est1_df2,output1_up],ignore_index=True)
down1= pd.concat([tit_est1_df2,output1_down],ignore_index=True)

    #Estudio 2
tit_est2_1 = df29_original.columns.values
tit_est2_2 = list (tit_est2_1)
tit_est2 = tit_est2_2 [0:]
tit_est2_list = list(tit_est2)
for a in lista:
    tit_est2_list.append (a)
tit_est2_df = pd.DataFrame (tit_est2_list)
tit_est2_df2= tit_est2_df.transpose()
up2= pd.concat([tit_est2_df2,output2_up],ignore_index=True)
down2= pd.concat([tit_est2_df2,output2_down],ignore_index=True)

#Estudio 3
tit_est3_1 = df30_original.columns.values
tit_est3_2 = list (tit_est3_1)
tit_est3 = tit_est3_2 [0:]
tit_est3_list = list(tit_est3)
for a in lista:
    tit_est3_list.append (a)
tit_est3_df = pd.DataFrame (tit_est3_list)
tit_est3_df2= tit_est3_df.transpose()
up3= pd.concat([tit_est3_df2,output3_up],ignore_index=True)
down3= pd.concat([tit_est3_df2,output3_down],ignore_index=True)

with pd.ExcelWriter('GenDEG.xlsx', engine='xlsxwriter') as writer:
    up1.to_excel(writer, sheet_name='est1_up')
    up2.to_excel(writer, sheet_name='est2_up')
    up3.to_excel(writer, sheet_name='est3_up')
    down1.to_excel(writer, sheet_name='est1_down')
    down2.to_excel(writer, sheet_name='est2_down')
    down3.to_excel(writer, sheet_name='est3_down')
