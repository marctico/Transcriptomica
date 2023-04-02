import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pingouin as pg
from scipy import stats
from rpy2.robjects.packages import importr
from rpy2.robjects.vectors import FloatVector
import math

df_counts = pd.read_excel(r'C:\Users\marcg\Documents\UNI\Nueva carpeta\TFG\python\Experimentos\Parkinson\115 RNA-Seq Post\output\115 RNA-Seq Post final.xlsx', sheet_name='Hoja1')
df_longene = pd.read_excel (r'C:\Users\marcg\Documents\UNI\Nueva carpeta\TFG\python\Experimentos\Parkinson\115 RNA-Seq Post\Excel original\Table S1_1.xlsx', sheet_name='LGen')
df_counts = df_counts.transpose()
print(df_counts)
print (df_longene)

#Consideraciones
#1- El excel debe seguir este formato:
    #df_counts: 
        #Vertical: Genes (codigo Ensembl ID)
        #Horizontal: Réplicas
        #La celda A1 no puede estar vacía
    #df_longene:
        #Vertical: Valores de longitud de genes
        #Ubicar los datos en la columna 'B', con un índice en la fila 1
        
#Input dataframe 
rep_counts_start = 1
rep_counts_end = 210
gene_counts_start = 0
gene_counts_end = 14004
denominador= 100000

#Celdas 
#Hay que crear una lista de listas para que se haga la división más adelante. 
#Se crea una lista general con un número igual al nombre de genes analizados. Las listas internas tienen un número igual al número de réplicas del estudio. 
#Esto va así porque la función más abajo, coge cada lista interna, y por cada valor lo divide por el elemento complementario de la lista divi.
#Por tanto, en cada bucle que se da a cabo, se utiliza todos los números de divi. 
counts2 = df_counts.iloc[rep_counts_start:rep_counts_end, gene_counts_start:gene_counts_end]
counts = counts2.transpose()
counts_list = np.array (counts)
counts_list2 = list (counts_list)
counts_list3 =[]
for a in counts_list2:
    b= list(a)
    counts_list3.append(b)

#Suma transcritos
#Hay que crear otra lista de listas, ya que para la suma se necesita una lista que contenga otras listas que correspondan a todos los counts por réplica. 
#asi que la lista general tendrá el número de réplicas del experimento, y las listas internas tendrán el número correspondiente al número de genes secuenciados.
counts2_list= np.array(counts2)
counts2_list2= list(counts2_list)
counts2_list3 =[]
for a in counts2_list2:#Transformar las listas internas en verdaderas listas
    b= list(a)
    counts2_list3.append(b)

suma= []
for a in counts2_list3:
    c = sum(x for x in a if not math.isnan(x))
    suma.append (c)

#Denominador de la división para cada réplica
divi = []
for d in suma:
    e= d/denominador
    divi.append (e)

#División 1 de la suma de transcritos
output_rpkm1_1 =[]
for i in range(len(counts_list3)): #Este bucle itera sobre cada lista anidada. Es decir, en el primer bucle se tendrá en cuenta [5, 20, 40]
    output_inter = [] #Aquí creo una lista vacía para luego almacenar las listas anidadas "output"
    for j in range(len(counts_list3[i])): #Aquí se itera sobre cada elemento de la lista anidada que estamos iterando. Es decirm primero 5, luego 20, y luego 40
         a = counts_list3[i][j] / divi[j] # Aquí se calcula la divisón de cada elemento que se está iterando, por el elemento correspondiente a la misma longitud de la longitud de los genes.
         output_inter.append(a) #Aquí se apendea la variable a cada lista que se aninará posteriormete.
    output_rpkm1_1.append(output_inter)#Aquí se anida la lista

#Pasar la matriz de lista a dataframe 
outputrpkm1 = pd.DataFrame(output_rpkm1_1)
outputrpkm1=outputrpkm1.transpose()
#Pasar el Dataframe a lista de listas
output_rpkm1= np.array (outputrpkm1)
output_rpkm1_3 = list (output_rpkm1)
output_rpkm1_2 =[]
for a in output_rpkm1_3:
    b= list(a)
    output_rpkm1_2.append(b)

#Lon Gen 
longene = df_longene.iloc[:, 1]
list_longene= list(longene)

#División 2 de la longitud de genes
output_rpkm2 =[]
for i in range(len(output_rpkm1_2)): #Este bucle itera sobre cada lista anidada. Es decir, en el primer bucle se tendrá en cuenta [5, 20, 40]
    output_inter2 = [] #Aquí creo una lista vacía para luego almacenar las listas anidadas "output"
    for j in range(len(output_rpkm1_2[i])): #Aquí se itera sobre cada elemento de la lista anidada que estamos iterando. Es decirm primero 5, luego 20, y luego 40
         a = output_rpkm1_2[i][j] / list_longene[j] # Aquí se calcula la divisón de cada elemento que se está iterando, por el elemento correspondiente a la misma longitud de la longitud de los genes.
         output_inter2.append(a) #Aquí se apendea la variable a cada lista que se aninará posteriormete.
    output_rpkm2.append(output_inter2)#Aquí se anida la lista

output_rpkm3 =pd.DataFrame(output_rpkm2)
output_rpkm4 = output_rpkm3
df3= output_rpkm4.transpose()
print(df3)
df3.to_excel (r'C:\Users\marcg\Documents\UNI\Nueva carpeta\TFG\python\Output\tttt.xlsx')



