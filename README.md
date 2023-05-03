# **TRANSCRIPTÓMICA**
---
## Tratamiento de datos para RNAseq
En este apartado se explicará las partes o fases principales del análisis de datos, con un método automatizado y verificado. Este sistema ayuda a obtener datos concluyentes de forma sencilla y fácil.

---
### Índice de los contenidos:
- Fase 0: Preparación de los datos 
    - Quitar la versión del gene ID 
    - Seleccionar datos de la matriz + genes 
- Fase 1: Transformar valores count a RPKM
- Fase 2: Análisis estadístico
    - DataFrame original:
        - Calcular:
            - Promedio 
            - Desviación estándar
        - Eliminar Outlayers
            - Límites positivo y negativo
            - Eliminar el gen del dataframe
        - Eliminar Missing Values
    - DataFrame nuevo:
        - Normalidad 
        - Homocedasticidad
        - Test Paramétrico
            - P-valor 
            - P-valor ajustado 
            - Promedio
            - Desviación estándar 
            - Fold Change 

- Fase 3: Comparar genes DEG entre diversos estudios
    - Obtener genes coincidentes
        - 2 datasets
        - 3 datasets
    - Obtener genes coincidentes con sus respectivos datos
        - 2 datasets
        - 3 datasets


---

## NOTAS IMPORTANTES SOBRE EL MÉTODO

1. DataFrame original:
    - Está pensado que sea un archivo Excel '.xlsx'
2. Conceptos básicos sobre python
    - Saber cómo importar/exportar un archivo Excel en python. 
    - Tener conocimiento para decir a python qué página del archivo Excel se quiere acceder.
    - Conocer el método de contaje que se utiliza para contar las filas y columnas del DataFrame. 
    - Instalar librerías complementarias a python con el método pip. 
    - Saber cómo importar librerías a tu archivo .py
3. El editor de texto usado es: 'Visual Studio Code'
---
## Librerías utilizadas durante el proceso

|Librerías   | Función  |
|--------   | --------  |
|Pandas   |Importar/Exportar Dataframe, Editar el archivo Excel |
|Numpy   | Creación de arrays y manajo de listas |
|  Pingouin |  Cálculo del P-valor |
|  Rpy2 | Cálculo del P-valor ajustado  |
|Xlsxwriter|Creación de hojas de Excel y la exportación de datos    |
| Matplotlib Seaborn  |Gráficos| 
|Scipy, Statsmodels |Preprocesado y análisis|
|Warnings |Configuración warnings
