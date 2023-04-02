# **Fase 1: Transformar valores count a RPKM**
## RPKM
---
Muchos estudios publican sus resultados de RNAseq en un formato de 'counts', el número de veces que se encuentra un transcrito en una muestra. Estos datos no estan normalizados, ni por el número de counts que se encuentra en cada muestra, ni por la longitud total del gen analizado. Por tanto, la normalización con RPKM se puede obtener unos datos más óptimos para ser interpretados.

**CONSIDERACIONES:** 
1. 1- El excel debe seguir este formato:
    - df_counts: 
        - Vertical: Genes (codigo Ensembl ID)
        - Horizontal: Réplicas
        - La celda A1 no puede estar vacía
    - df_longene:
        - Vertical: Valores de longitud de genes
        - Ubicar los datos en la columna 'B', con un índice en la fila 1

Una vez explicado esto, empecemos con el código:
> Importar las librerías
``` python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pingouin as pg
from scipy import stats
from rpy2.robjects.packages import importr
from rpy2.robjects.vectors import FloatVector
import math
```

> Directorio de nuestra lista de genes: 

``` python
df_counts= pd.read_excel (r'C', sheet_name= '') 
df_longene= pd.read_excel (r'C', sheet_name= '')
df_counts = df_counts.transpose()
```
Se transpone el DataFrame para poder generar una lista de listas, ya que cuando se pasa un DataFrame a lista, se genera una lista empezando per las filas del Excel y no por las columnas. Dentro de esta lista general clasificada por las filas 'x' del Excel, se generan listas internas que son los datos por fila por cada gen. 
> Input de nuestro dataframe original (counts)

``` python
rep_counts_start = 1
rep_counts_end = 210
gene_counts_start = 0
gene_counts_end = 14004
denominador= 100000
```
> Transformar el DataFrame original a lista
```python
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
```
> Suma de transcritos por cada réplica
```python
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
```
> Denominador de la división para cada réplica
```python
divi = []
for d in suma:
    e= d/denominador
    divi.append (e)
```
> División 1 de la suma de transcritos
```python
output_rpkm1_1 =[]
for i in range(len(counts_list3)): #Este bucle itera sobre cada lista anidada. Es decir, en el primer bucle se tendrá en cuenta [5, 20, 40]
    output_inter = [] #Aquí creo una lista vacía para luego almacenar las listas anidadas "output"
    for j in range(len(counts_list3[i])): #Aquí se itera sobre cada elemento de la lista anidada que estamos iterando. Es decirm primero 5, luego 20, y luego 40
         a = counts_list3[i][j] / divi[j] # Aquí se calcula la divisón de cada elemento que se está iterando, por el elemento correspondiente a la misma longitud de la longitud de los genes.
         output_inter.append(a) #Aquí se apendea la variable a cada lista que se aninará posteriormete.
    output_rpkm1_1.append(output_inter)#Aquí se anida la lista
```
> Pasar la lista de listas a dataframe
```python
outputrpkm1 = pd.DataFrame(output_rpkm1_1)
outputrpkm1=outputrpkm1.transpose() 
``` 
Se transpone para ubicar los genes en horizontal y las réplicas en vertical, así se genera una lista general en base a las réplicas (ubicadas en las filas del Excel). Este paso se realiza porque queremos dividir en base a la longitud de los genes y no a la suma de los transcritos. 
> Pasar el Dataframe a lista de listas
```python
output_rpkm1= np.array (outputrpkm1)
output_rpkm1_3 = list (output_rpkm1)
output_rpkm1_2 =[]
for a in output_rpkm1_3:
    b= list(a)
    output_rpkm1_2.append(b)
```
> Seleccionar la lista de longitud de genes
```python
longene = df_longene.iloc[:, 1]
list_longene= list(longene)
``` 
> División 2 de la longitud de genes
```python
output_rpkm2 =[]
for i in range(len(output_rpkm1_2)): #Este bucle itera sobre cada lista anidada. Es decir, en el primer bucle se tendrá en cuenta [5, 20, 40]
    output_inter2 = [] #Aquí creo una lista vacía para luego almacenar las listas anidadas "output"
    for j in range(len(output_rpkm1_2[i])): #Aquí se itera sobre cada elemento de la lista anidada que estamos iterando. Es decirm primero 5, luego 20, y luego 40
         a = output_rpkm1_2[i][j] / list_longene[j] # Aquí se calcula la divisón de cada elemento que se está iterando, por el elemento correspondiente a la misma longitud de la longitud de los genes.
         output_inter2.append(a) #Aquí se apendea la variable a cada lista que se aninará posteriormete.
    output_rpkm2.append(output_inter2)#Aquí se anida la lista

```
> Transformar la lista en DataFrame
``` python
output_rpkm3 =pd.DataFrame(output_rpkm2)
output_rpkm4 = output_rpkm3
df3= output_rpkm4.transpose() #Recolocamos otra vez el DataFrame, réplicas en horizontal y genes en vertical
``` 
> Exportar la lista a un Excel 
```python
ensembl_df.to_excel(r'C:\ .xlsx')
``` 