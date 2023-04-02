import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pingouin as pg
from scipy import stats
from rpy2.robjects.packages import importr
from rpy2.robjects.vectors import FloatVector

df= pd.read_excel(r'C:\Users\marcg\Documents\UNI\Nueva carpeta\TFG\python\Experimentos\Parkinson\PKRN_hermanos\Excel original\PRKN_hermanos original.xlsx', sheet_name='25d')
df = df.transpose()
print (df)

#Consideraciones
#1- El excel tiene que estar en este formato:
    #Horizontal: Réplicas
    #Vertical: Genes (codigo Ensembl ID)
#2- IMPORTANTE:
    #En cada fila de genes no pueden ser todos los datos NaN, sino el pvalue no funciona
    #La celda A1 no debe estar vacía

#input del Dataframe
#Control 
row_cd_start=1 #posición de inicio de las réplicas control
row_cd_end=5 #posición final de las réplicas control
col_cd_start=0 #posición de inicio de los genes
col_cd_end =57784 #posición final de los genes 
#Tratado
row_trat_start=5 #posición de inicio de las réplicas tratado
row_trat_end=9 #posición final de las réplicas tratado
col_trat_start=0
col_trat_end =57784
#Missing Value, indicar el limite de 0 permitidos para validar los datos de ese gen
repet_cd = (row_cd_end-row_cd_start)/2
repet_trat =(row_trat_end-row_trat_start)/2


#Aquí empieza el código 
#Celdas Control
celdas_ct=df.iloc[row_cd_start:row_cd_end]
#Celdas Tratado
celdas_trat= df.iloc[row_trat_start:row_trat_end]


# Promedio Control 
promedio_ct= celdas_ct.mean(axis=0)
df_1_ct= pd.DataFrame(promedio_ct)
df2_ct= df_1_ct.transpose()
df3= pd.concat([df,df2_ct], ignore_index=True)

#Promedio Tratado
promedio_trat= celdas_trat.mean(axis=0)
df_1_trat= pd.DataFrame(promedio_trat)
df2_trat= df_1_trat.transpose()
df4= pd.concat([df3,df2_trat], ignore_index=True)

#Desv Est Control
desvest_ct= celdas_ct.std(axis=0)
df_2_ct= pd.DataFrame(desvest_ct)
df3_ct= df_2_ct.transpose()
df5= pd.concat([df4,df3_ct], ignore_index=True)

#Desv Est Tratado
desvest_trat= celdas_trat.std(axis=0)
df_2_trat= pd.DataFrame(desvest_trat)
df3_trat= df_2_trat.transpose()
df6= pd.concat([df5,df3_trat], ignore_index=True)

#Límite Positivo Control
limit_pos_ct1= promedio_ct + (2*desvest_ct)
df_3_ct= pd.DataFrame(limit_pos_ct1)
df4_ct= df_3_ct.transpose()
df7= pd.concat([df6,df4_ct], ignore_index=True)

#Límite Negativo Control 
limit_neg_ct1= promedio_ct - (2*desvest_ct)
df_4_ct= pd.DataFrame(limit_neg_ct1)
df5_ct= df_4_ct.transpose()
df8= pd.concat([df7,df5_ct], ignore_index=True)

#Límite Positivo Tratado
limit_pos_trat1= promedio_trat + (2*desvest_trat)
df_3_trat= pd.DataFrame(limit_pos_trat1)
df4_trat= df_3_trat.transpose()
df9= pd.concat([df8,df4_trat], ignore_index=True)

#Límite Negativo Tratado
limit_neg_trat1= promedio_trat - (2*desvest_trat)
df_4_trat= pd.DataFrame(limit_neg_trat1)
df5_trat= df_4_trat.transpose()
df10= pd.concat([df9,df5_trat], ignore_index=True)


############################################################################################
#Límite Control positivo y negativo
#Pasar un data frame a lista
lista_2 = []
for x in limit_pos_ct1:
    lista_2.append(x)

lista_3 = []
for x in limit_neg_ct1:
    lista_3.append(x)

#Transponer el dataframe
df10_1= df10.transpose()

#Transformar el dataframe (listas de columnas dentro de una lista)
df10_1 = df10_1.iloc[col_cd_start:col_cd_end, row_cd_start:row_cd_end]
df10_3 = df10_1

df10_4 = np.array(df10_3)
df10_5 = list(df10_4)

df10_2 = df10_5

#Sustituir un valor por ''
def sustituir (df10_2, lista_2):
    if len(df10_2) != len(lista_2) or len(df10_2) != len(lista_3):
        raise ValueError('La longitud de lst y limite_sup deben de ser iguales')
    for i in range(len(df10_2)):
        df10_2[i] = ['' if x > lista_2[i] or x < lista_3[i] else x for x in df10_2[i]]
    return df10_2
df10_2 = sustituir(df10_2, lista_2)

#Crear un dataframe nuevo con los valores sustituidos
df11= pd.DataFrame(df10_2)
#transponer el dataframe 
df12 = df11.transpose()

############################################################################################
#Límite Tratado positivo y negativo
#Pasar un data frame a lista
lista_4 = []
for x in limit_pos_trat1:
    lista_4.append(x)

lista_5 = []
for x in limit_neg_trat1:
    lista_5.append(x) 

#Transponer el dataframe
df13= df10.transpose()

#Transformar el dataframe (listas de columnas dentro de una lista)
df13_3 = df13.iloc[col_trat_start:col_trat_end, row_trat_start:row_trat_end]
df13_4 = np.array(df13_3)
df13_5 = list(df13_4)
df13_2 = df13_5

#Sustituir un valor por ''
def sustituir (df13_2, lista_4):
    if len(df13_2) != len(lista_4):
        raise ValueError('La longitud de lst y limite_sup deben de ser iguales')
    for i in range(len(df13_2)):
        df13_2[i] = ['' if x > lista_4[i] or x < lista_5[i] else x for x in df13_2[i]]
    return df13_2
df13_2 = sustituir(df13_2, lista_4)

#Crear un dataframe nuevo con los valores sustituidos
df14= pd.DataFrame(df13_2)

#transponer el dataframe 
df15 = df14.transpose()

df16= pd.concat([df12,df15], ignore_index=True)

#Crear una lista de los genes/metabolitos 
df_index = df.iloc[0] #selecciono la columna
df_index_list = list (df_index) #lo convierto a lista
df_index_df = pd.DataFrame (df_index_list) #lo paso a un dataframe 
df_index_df = df_index_df.transpose () #lo transpongo para que el dataframe pase de vertical a horizontal 

#Unir el nombre de los genes con los valores sin outlayers
df16_1 = pd.concat([df16,df_index_df], ignore_index=True)
df16_2 = df16_1.transpose() #lo hago para que el python no me de error, ya que hay un límite de matriz para colocar en el excel (row=100.000, column=16.000)

df16_2.to_excel(r'C:\Users\marcg\Documents\UNI\Nueva carpeta\TFG\python\Output\PRKN_hermanos v2.xlsx')

df17 = pd.read_excel(r'C:\Users\marcg\Documents\UNI\Nueva carpeta\TFG\python\Output\PRKN_hermanos v2.xlsx')
#########################################################################################################################
 
#Transponer el dataframe
df18= df17

#Nuevo Dataframe
#Control
new_row_cd_start = 0
new_row_cd_end = row_cd_end-row_cd_start
#Tratado
new_row_trat_start = new_row_cd_end
new_row_trat_end =row_trat_end-row_cd_start


#Missing Values
#Transformar el dataframe (listas de columnas dentro de una lista) Juntas
row_cd_end2 = row_trat_end + 1 
df13_12 = df18.iloc[col_cd_start:col_cd_end, row_cd_start:row_cd_end2] #Incluir los nombres de los genes en la matriz
df13_13 = np.array(df13_12)
df13_14 = list(df13_13)

test_list = []
for a in df13_13:
    control = a[new_row_cd_start:new_row_cd_end]
    tratado = a[new_row_trat_start:new_row_trat_end] #excluir los nombres de los genes 
    c = list(control)
    repet = c.count(0)
    e = list(tratado)
    repet2 = e.count (0)
    if repet < repet_cd and repet2 < repet_trat:
        test_list.append (a)
    
df18 = pd.DataFrame (test_list)

####################################################
#Nuevo Dataframe
#Control
new_row_cd_start = 0
new_row_cd_end = row_cd_end-row_cd_start
new_col_cd_start = 0
new_col_cd_end =df18.shape[0]
new_col_cd_end2=new_col_cd_end+1
#Tratado
new_row_trat_start = new_row_cd_end
new_row_trat_end =row_trat_end-row_cd_start
new_col_trat_start = 0
new_col_trat_end =df18.shape[0]
new_col_trat_end2=new_col_trat_end+1
######################################################

#Calcular el Pvalor ajustado
#Transformar el dataframe (listas de columnas dentro de una lista) Control
df13_6 = df18.iloc[0:new_col_cd_end2, new_row_cd_start:new_row_cd_end]
df13_7 = np.array(df13_6)
df13_8 = list(df13_7)

#Transformar el dataframe (listas de columnas dentro de una lista) Tratado
df13_9 = df18.iloc[0:new_col_trat_end2, new_row_trat_start:new_row_trat_end]
df13_10 = np.array(df13_9)
df13_11 = list(df13_10)

#P valor  
pvalor_lista = []
for gen in range(len(df18.iloc[0:new_col_trat_end2, 1])):#len cuenta los valores dentro de una lista, range itera dentro del rango indicado con len
    a = df13_8[gen].tolist()
    b = df13_11[gen].tolist()
    t_test = pg.ttest(a, b, correction=False)
    p_valor = f"{t_test.iloc[0,3]}"
    pvalor_lista.append(p_valor)

#Convertir los string de pvalores a float()
n = []
for a in pvalor_lista:
    n.append(float(a))

#Añadir el dataframe a otro
pvalor_lista_df2= pd.DataFrame(n)
pvalor_lista_off= pvalor_lista_df2.transpose()
df19 = df18.transpose()
df20= pd.concat([df19,pvalor_lista_off], ignore_index=True)

#Pvalor ajustado
stats = importr('stats')

p_adjust = stats.p_adjust(FloatVector(n), method = 'BH')
p_adjust_off = list(p_adjust)
p_adjust_off2 = pd.DataFrame (p_adjust_off)
p_adjust_off2 = p_adjust_off2.transpose()
df21= pd.concat([df20,p_adjust_off2], ignore_index=True)

######################################################################################
#Promedio Sin Outlayers 
#Celdas Control
celdas_ct_2= df21.iloc[0:new_row_cd_end, 0:new_col_cd_end2]
#Celdas Tratado
celdas_trat_2= df21.iloc[new_row_trat_start:new_row_trat_end, 0:new_col_trat_end2]

# Promedio Control 
promedio_ctnew= celdas_ct_2.mean(axis=0)
df_1_ctnew= pd.DataFrame(promedio_ctnew)
df2_ctnew= df_1_ctnew.transpose()
df22= pd.concat([df21,df2_ctnew], ignore_index=True)

#Promedio Tratado
promedio_tratnew= celdas_trat_2.mean(axis=0)
df_1_tratnew= pd.DataFrame(promedio_tratnew)
df2_tratnew= df_1_tratnew.transpose()
df23= pd.concat([df22,df2_tratnew], ignore_index=True)

#Desv.est Sin Outlayers
#Desv Est Control
desvest_ctnew= celdas_ct_2.std(axis=0)
df_2_ctnew= pd.DataFrame(desvest_ctnew)
df3_ctnew= df_2_ctnew.transpose()
df24= pd.concat([df23,df3_ctnew], ignore_index=True)

#Desv Est Tratado
desvest_tratnew= celdas_trat_2.std(axis=0)
df_2_tratnew= pd.DataFrame(desvest_tratnew)
df3_tratnew= df_2_tratnew.transpose()
df25= pd.concat([df24,df3_tratnew], ignore_index=True)

#Fold Change
fc = promedio_tratnew / promedio_ctnew
fc_df = pd.DataFrame (fc)
fc_df2 = fc_df.transpose()
df26 = pd.concat([df25,fc_df2], ignore_index=True)
df27 = df26.transpose()
print (df27)
df27.to_excel(r'C:\Users\marcg\Documents\UNI\Nueva carpeta\TFG\python\Output\PRKN_hermanos v3.xlsx')
