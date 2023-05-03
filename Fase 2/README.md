# **Fase 2: Análisis estadístico**
## DataFrame Original
---
Una vez ya se tiene los datos normalizados, se procede a realizar el análisis estadístico.

En primer lugar, se utiliza el DataFrame original donde se selecciona la matriz de datos. Sobre este dataset se realiza un tratamiento o limpieza de datos para evitar datos que han sido mal interpretados o leídos por la maquinaria del laboratorio. 
- Outlayers:

Sobre estos datos se calcula el promedio y la desviación estándar por cada gen. Con estos valores se calcula los límites positivo y negativo por gen.

Límite positivo : Promedio + 2*(Desv. est.)

Límite negativo : Promedio - 2*(Desv. est.)

Todos los datos dentro de cada gen que no esten en la zona permitida, son transformados a Nan/celda vacía.

Nota: esta eliminación de los outlayers por gen, se realiza en dos partes. Por tanto, por cada gen hay 4 límites, dos para control y dos para tratado/condición problema. 

- Missing Values

Hay veces que la lectura del gen no es correcta y los datos de ese gen (tanto de control como condición problema son 0). Para evitar estos datos se ha desarrollado un sistema para eliminar estos genes. 

Control: si tienes 'x' muestras, si la mitad de esas muestras por ese gen tienen un valor de 0, se elimina toda la fila del gen (tanto control como condición problema).

Condición problema: si tienes 'x' muestras, si la mitad de esas muestras por ese gen tienen un valor de 0, se elimina toda la fila del gen (tanto control como condición problema).

Por tanto, si se encuentra esta premisa en cualquiera de los dos condiciones, ese gen se elimina para evitar errores en los resultados. 


**CONSIDERACIONES:** 
1. El excel tiene que estar en este formato:
    - Horizontal: Réplicas
    - Vertical: Genes (codigo Ensembl ID)
2. IMPORTANTE:
    - En cada fila de genes no pueden ser todos los datos NaN, sino el pvalue no funciona
    - La celda A1 no debe estar vacía

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
```

> Directorio de nuestra lista de genes: 

``` python
df= pd.read_excel (r'C', sheet_name= '') 
df = df.transpose()
```
Se transpone el DataFrame para poder generar una lista de listas, ya que cuando se pasa un DataFrame a lista, se genera una lista empezando per las filas del Excel y no por las columnas. Dentro de esta lista general clasificada por las filas 'x' del Excel, se generan listas internas que son los datos por fila por cada gen. 
> Input de nuestro dataframe original (counts)

``` python
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
```
> Missing Value, indicar el limite de 0 permitidos para validar los datos de ese gen
```python
repet_cd = (row_cd_end-row_cd_start)/2
repet_trat =(row_trat_end-row_trat_start)/2
```
> Seleccionar las celdas
```python
#Celdas Control
celdas_ct=df.iloc[row_cd_start:row_cd_end]
#Celdas Tratado
celdas_trat= df.iloc[row_trat_start:row_trat_end]
```
> Promedio
```python
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
```
> Desviación estándar
```python
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
```
> Límites
```python
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
```
## **Outlayers**

**Sustituir datos de genes a partir de los límites control**
> Transformar los datos de límites (+/-) a lista
```python
lista_2 = []
for x in limit_pos_ct1:
    lista_2.append(x)

lista_3 = []
for x in limit_neg_ct1:
    lista_3.append(x)
```
> Transformar el DataFrame original a lista
```python
#Transponer el dataframe
df10_1= df10.transpose()

#Transformar el dataframe (listas de columnas dentro de una lista)
df10_1 = df10_1.iloc[col_cd_start:col_cd_end, row_cd_start:row_cd_end]
df10_3 = df10_1

df10_4 = np.array(df10_3)
df10_5 = list(df10_4)

df10_2 = df10_5
```
> Sustituir un valor por ''
```python
def sustituir (df10_2, lista_2):
    if len(df10_2) != len(lista_2) or len(df10_2) != len(lista_3):
        raise ValueError('La longitud de lst y limite_sup deben de ser iguales') 
        #Si el número de elementos entre una lista interna de la lista general del DataFrame no es igual al núm. de elementos en las dos listas de límites (+/-), marca un error al ejecutar. 
    for i in range(len(df10_2)):
        df10_2[i] = ['' if x > lista_2[i] or x < lista_3[i] else x for x in df10_2[i]]
        #Dos condicionales, si uno de los dos se cumple, se sustituye el elemento por un NaN.
    return df10_2
df10_2 = sustituir(df10_2, lista_2)

#Crear un dataframe nuevo con los valores sustituidos
df11= pd.DataFrame(df10_2)
#transponer el dataframe 
df12 = df11.transpose()
```
Realizamos lo mismo con los datos en la condición problema

**Sustituir datos de genes a partir de los límites tratado**
```python
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

#Unir los dos DataFrame modificados, uno donde estan las muestras control y otro el de las muestras tratado
df16= pd.concat([df12,df15], ignore_index=True)
```
Ahora solo tenemos los datos en sí, se ha obviado la lista de genes con el código. Por tanto, se debe volver a colocar esta lista en el DataFrame.
```python
#Crear una lista de los genes/metabolitos 
df_index = df.iloc[0] #selecciono la columna
df_index_list = list (df_index) #lo convierto a lista
df_index_df = pd.DataFrame (df_index_list) #lo paso a un dataframe 
df_index_df = df_index_df.transpose () #lo transpongo para que el dataframe pase de vertical a horizontal 

#Unir el nombre de los genes con los valores sin outlayers
df16_1 = pd.concat([df16,df_index_df], ignore_index=True)
df16_2 = df16_1.transpose() #lo hago para que el python no me de error, ya que hay un límite de matriz para colocar en el excel (row=100.000, column=16.000)
```
Exportamos los datos a un Excel, para tener un archivo de control dentro del propio código, por si ocurre algún error inesperado, saber más o menos donde está y solucionarlo. 
```python
df16_2.to_excel(r'C:.xlsx')
```
Importamos de nuevo el archivo para seguir trabajando en el análisis
```python
df17 = pd.read_excel(r'C:.xlsx')
```
> Input del nuevo DataFrame
```python
df18= df17
#Control
new_row_cd_start = 0
new_row_cd_end = row_cd_end-row_cd_start
#Tratado
new_row_trat_start = new_row_cd_end
new_row_trat_end =row_trat_end-row_cd_start
```
## **Missing Values**
```python
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
```
---
## DataFrame Nuevo


### **Normalidad y Homocedasticidad**
Para poder comprobar que los datos siguen una distribución paramétrica, es necesario realizar pruebas de normalidad y de homocedasticidad.

**CONSIDERACIONES:** 
1. El excel debe tener el siguiente formato:
    - Columnas: Muestras (control/tratado)
    - Filas (variables/metabolitos/genes)
    - La celda 'A1' se debe escribir algo
2. Output: 4 columnas en un Excel
    - Columnas: nombre variables, normalidad control (Shaphiro-Wilk), normalidad tratado (Shaphiro-Wilk), homocedasticidad (Bartlett)
    

Una vez explicado esto, empecemos con el código:
> Importar las librerías
``` python
# Tratamiento de datos
import pandas as pd
import numpy as np

# Gráficos
import matplotlib.pyplot as plt
from matplotlib import style
import seaborn as sns

# Preprocesado y análisis
import statsmodels.api as sm
from scipy import stats

# Configuración matplotlib
plt.style.use('ggplot')

# Configuración warnings
import warnings
warnings.filterwarnings('ignore')
```

> Directorio de nuestra lista de genes: 

``` df= pd.read_excel (r'C', sheet_name= '') ```

> Generar lista de metabolitos
```python 
df_metb = d1.iloc[:,0]
df_list_metb = np.array(df_metb)
df_list_metb2 = list (df_list_metb)
```
> Input de nuestro dataframe 
```python 
#Control
start_ct= 1 #Número de columna inicio 
end_ct= 12 #Número de columna final 
#Tratado
start_trat = 12
end_trat =18
#Todos
start= 1
end= 18 
```
> Creación de listas por condiciones separadas
```python 
#Lista de control
df_ct= d1.iloc[:, start_ct:end_ct]
df_list_ct = np.array(df_ct)
df_list_ct2 = list(df_list_ct)

#Lista de tratado
df_trat= d1.iloc[:, start_trat:end_trat]
df_list_trat = np.array(df_trat)
df_list_trat2 = list(df_list_trat)
```
Se genera dos listas. En cada lista, contiene varias listas con datos de cada metabolito en particular.

---
### Normalidad
---
Generación de bucles para cada condición. La función del bucle es coger una lista de listas e ir pasando el código por cada lista interna, obteniendo un pvalor para cada metabolito. 
Finalmente, se obtienen dos listas de pvalores, una para la condición control y otra para la condición tratado 
```python 
#Bucle Control Normalidad
pvalue_ct2=[]
for j in range(len(df_list_ct2)): 
    metb_ct = df_list_ct2[j]
    metb_ct2=[]
    for h in metb_ct: 
        k= str (h)
        metb_ct2. append(k)
    pess2_ct= []
    for x in metb_ct2: 
        y= str(x)
        l= y.isalpha()
        if l is False:
            a= float(y)
            pess2_ct.append (a)
    peso_ct = pd.DataFrame (pess2_ct)
    shapiro_ct =stats.shapiro(peso_ct)
    pvalue_ct_float = shapiro_ct[1]
    pvalue_ct2.append(pvalue_ct_float)
    
#Bucle Tratado Normalidad
pvalue_trat2=[]
for j in range(len(df_list_trat2)): 
    metb_trat = df_list_trat2[j]
    metb_trat2=[]
    for h in metb_trat: 
        k= str (h)
        metb_trat2. append(k)
    pess2_trat= []
    for x in metb_trat2: 
        y= str(x)
        l= y.isalpha()
        if l is False:
            a= float(y)
            pess2_trat.append (a)
    peso_trat = pd.DataFrame (pess2_trat)
    shapiro_trat =stats.shapiro(peso_trat)
    pvalue_trat_float = shapiro_trat[1]
    pvalue_trat2.append(pvalue_trat_float)

```
---
### Homocedasticidad
---
Generación de un bucle, donde se va pasando lista por lista, tanto de la condición control como tratado. 

```python 
#Bucle Todos
bartlett2 =[]
for j in range(len(df_list_ct2)): 
    met_ct = df_list_ct2[j]
    met_ct2 =[]
    for x in met_ct:
        k = float(x)
        met_ct2.append (k)
    met_ct_df = pd.DataFrame(met_ct2)
    met_ctt= met_ct_df.iloc [:,0]
    met_trat = df_list_trat2[j]
    met_trat2= []
    for x in met_trat: 
        k=float(x)
        met_trat2.append(k)
    met_trat_df = pd.DataFrame(met_trat2)
    met_tratt = met_trat_df[0]
    bartlett_test=stats.bartlett(met_ctt, met_tratt)
    pvalue_bar_float = bartlett_test[1]
    bartlett2.append(pvalue_bar_float)
```
---
### Exportación de las tres listas a un Excel
---
```python 
#Convertir las listas a DataFrame
df1 = pd.DataFrame (df_list_metb2).T
pvalue_ct2_df = pd.DataFrame (pvalue_ct2).T
pvalue_trat2_df = pd.DataFrame(pvalue_trat2).T
bartlett2_df= pd.DataFrame (bartlett2).T
#Concatenar los diversos DataFrame
df2 = pd.concat([df1,pvalue_ct2_df], ignore_index=True)
df3 = pd.concat([df2,pvalue_trat2_df], ignore_index=True)
df4 = pd.concat([df3,bartlett2_df], ignore_index=True).T
```
```python 
df4.to_excel(r'C:.xlsx')
```

### **Test paramétrico**
En segundo lugar, cuando se tienen los datos ya tratados y siguen una distribución normal, se puede comenzar a realizar el análisis estadístico. 

Se calcula tanto el pvalue como el pvalue ajustado y, también, los nuevos promedios y desviaciones estándar de control y condición control. Por último, se calcula el Fold Change, que es un valor importante para poder seleccionar genes DEG. 

> Input del nuevo DataFrame
```python
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
```
Se debe seleccionar por separado los datos de las dos condiciones y transformar las dos matrices de datos en listas.
``` python
#Transformar el dataframe (listas de columnas dentro de una lista) Control
df13_6 = df18.iloc[0:new_col_cd_end2, new_row_cd_start:new_row_cd_end]
df13_7 = np.array(df13_6)
df13_8 = list(df13_7)

#Transformar el dataframe (listas de columnas dentro de una lista) Tratado
df13_9 = df18.iloc[0:new_col_trat_end2, new_row_trat_start:new_row_trat_end]
df13_10 = np.array(df13_9)
df13_11 = list(df13_10)
```
> Calcular el pvalue
```python 
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
```
La lista de pvalues por cada gen se añade al DataFrame
```python 
pvalor_lista_df2= pd.DataFrame(n)
pvalor_lista_off= pvalor_lista_df2.transpose()
df19 = df18.transpose()
df20= pd.concat([df19,pvalor_lista_off], ignore_index=True)
```
Seguidamente, se calcula el pvalue ajustado en base a el pvalue obtenido anteriormente
```python 
stats = importr('stats')

p_adjust = stats.p_adjust(FloatVector(n), method = 'BH')
p_adjust_off = list(p_adjust)
p_adjust_off2 = pd.DataFrame (p_adjust_off)
p_adjust_off2 = p_adjust_off2.transpose()
df21= pd.concat([df20,p_adjust_off2], ignore_index=True)
```
> Cálculo de nuevos promedios y desviaciones estándar para las dos condiciones 
```python 
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
```
Por último, calculamos el Fold Change tomando como datos los promedios de control y condición problema. La operación se muestra a continuación:

Promedio tratado  / Promedio control = FC
```python 
#Fold Change
fc = promedio_tratnew / promedio_ctnew
fc_df = pd.DataFrame (fc)
fc_df2 = fc_df.transpose()
df26 = pd.concat([df25,fc_df2], ignore_index=True)
```
> Exportar el DataFrame a un nuevo archivo Excel
```python 
df27 = df26.transpose()
df27.to_excel(r'C:.xlsx')
```