# **Fase 0: Preparación de los datos**
## Quitar la versión del gene ID
---
Este código está pensado para poder transformar el gene ID como, por ejemplo:

ENSG0000002345.1 -> ENSG0000002345

**CONSIDERACIONES:** 
1. Los datos deben de estar en: 
    - Vertical: Genes Ensembl ID + version
    - Ubicar los Gene ID en la columna A con un índice encima como 'Ensembl ID'
    - Horizontal: Réplicas
    - Los datos se pueden coger del propio excel original

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

``` df= pd.read_excel (r'C', sheet_name= '') ```

> Input de nuestro dataframe 

``` python
gene_start= 0 #Fila de inicio de la lista
gene_end= 17298 #Fila final de la lista
ensembl_id= 74 #Columna donde se ubica la lista de genes
```
> Convertir este dataframe a lista
``` python
a = df.iloc[gene_start:gene_end, ensembl_id]
ensembl_version = list (a)
```
> Quitar la versión del gene id
``` python
ensembl = []
for n in ensembl_version:
    m = n[0:15]
    ensembl.append (m)

ensembl_df = pd.DataFrame (ensembl) #convertir la lista nueva en DataFrame
```
> Exportar la lista a un Excel 
```python
ensembl_df.to_excel(r'C:\ .xlsx')
```
---
## Seleccionar datos + genes del DataFrame original
---
Cuando en un dataset de un estudio, obtienes un lista de gene name y quieres transformarlo a gene id. Tienes que ir a alguna web, como ensembl.org, donde obtendrás una lista de gene id desordenados y con una lista menos extensa, ya que algunos gene name no se han transformado. Por tanto, hay que seleccionar los genes que si que estan en la nueva lista de gene id, con los datos correspondientes. 

**CONSIDERACIONES:** 
1. El excel debe tener este formato:
    - Dataframe original
        - Horizontal: Muestras
        - Vertical: Genes 
    - Lista de genes de ensembl
        - Vertical : Lista de genes

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

> Directorios: 

``` python
df= pd.read_excel (r'C', sheet_name= '') #Genes transformados
df1 = pd.read_excel (r'C', sheet_name= '') # DataFrame original
```
> Input
```python
#input Dataframe
rep_counts_start = 0
rep_counts_end = 11
gene_counts_start = 0
gene_counts_end = 55618
#input lista de genes
rep_gene_start = 0
gene_start = 0
gene_end = 54623
```
> Transformar el DataFrame original a lista
```python
df1_1 = df1.iloc [gene_counts_start:gene_counts_end, rep_counts_start:rep_counts_end]
df1_2= np.array(df1_1)
df1_3 = list (df1_2)
df1_4 = []
for a in df1_3:
    b = list(a)
    df1_4.append(b)
```
> Transformar el DataFrame de genes transformados a lista 
```python
df_1 = df.iloc[gene_start:gene_end, rep_gene_start]
df_2 = list (df_1)
```
> Seleccionar los datos del DataFrame original
```python
output=[]
for a in df1_4:
    b= a[0]
    c = b in df_2
    if c is True:
        output.append (a)

output1 = pd.DataFrame (output)
```
> Exportar la lista a un Excel 
```python
ensembl_df.to_excel(r'C:\ .xlsx')
```  