#!/usr/bin/env python
# coding: utf-8

# ## Descripción Detallada de los Datos
# ### Sistema de Recomendación de Noticias sobre Clientes con Potencial Comercial

# In[191]:


import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from scipy import stats

clientes = pd.read_csv('C:/Users/dmtor/Desktop/Dataton/clientes.csv')
noticias = pd.read_csv('C:/Users/dmtor/Desktop/Dataton/noticias.csv')
clientes_noticias = pd.read_csv('C:/Users/dmtor/Desktop/Dataton/clientes_noticias.csv')



# ###  Base de datos de clientes 
# 
# * clientes.csv: Archivo con el listado de clientes a consultar, la descripción de su actividad económica y el subsector
# * nit: Identificador único del cliente
# * nombre: Nombre corporativo del cliente
# * desc_ciiu_división: Descripción general de la clasificación Industrial uniforme d todas las actividades económicas
# * desc_ciiu_grupo: Descripción por grupo de la clasificación Industrial uniforme d todas las actividades económicas
# * desc_ciiu_clase: : Descripción por clase de la clasificación Industrial uniforme d todas las actividades económicas
# * subsector: Clasificación de la actividad industrial

# In[182]:


# Estadísticas descriptivas
df = clientes
ini = len(df)
print("Dimensiones:""", str(df.shape))
print('Categorias:')
print(clientes.nunique())
print("\nDatos nulos:\n", str(df.isnull().sum()))
print("\nTipo de datos:\n",str(df.dtypes))

pd= clientes
columnas= ['subsec','desc_ciiu_division', 'desc_ciuu_grupo', 'desc_ciiuu_clase']

for i,column in enumerate(columnas):
    
    val_num = i
    print(column)
    
    dis = ['subsec','desc_ciiu_division', 'desc_ciuu_grupo', 'desc_ciiuu_clase']
    if column not in dis: 
        fig, axes = plt.subplots(1, 2, figsize=(16, 4))
        plt.title(column)
        top_100_categories = df[column].value_counts().nlargest(30).index
        df_filtered = df[df[column].isin(top_100_categories)]
        df_sorted = df_filtered.sort_values(by=column, key=lambda x: x.map(df_filtered[column].value_counts()), ascending=False)
        sns.histplot(data=df_sorted, x= column, kde=True, ax = axes[0], discrete=True)
        plt.title(column)
        sns.boxplot(data = df_sorted, y = df.columns[val_num], ax = axes[1])
        plt.xticks(rotation=90)
        def shorten_label(label):
            return label[:30]
        axes[0].set_xticklabels([shorten_label(label.get_text()) for label in axes[0].get_xticklabels()])
        plt.rcParams['font.family'] = 'arial'
        plt.rcParams['font.size'] = 14
        
        plt.show()
    else:
        fig, axes = plt.subplots(1, 1, figsize=(16, 4))
        plt.title(column)
        top_100_categories = df[column].value_counts().nlargest(30).index
        df_filtered = df[df[column].isin(top_100_categories)]
        df_sorted = df_filtered.sort_values(by=column, key=lambda x: x.map(df_filtered[column].value_counts()), ascending=False)
        sns.histplot(data=df_sorted, x= column, ax = axes, discrete=True)
        plt.title(column)
        plt.xticks(rotation=90)
        def shorten_label(label):
            return label[:30]
        axes.set_xticklabels([shorten_label(label.get_text()) for label in axes.get_xticklabels()])
        plt.rcParams['font.family'] = 'arial'
        plt.rcParams['font.size'] = 14
        
        plt.show()


# ### noticias.csv
# 
# noticias.csv: Contenido de cada una de las noticias consultadas
# * new_id: Identificador único de noticias
# * news_url_absolute: Url de la noticia encontrada
# * news_init_date: Fecha mínima del intevalo de tiempo al que pertenece la noticia
# * news_final_date: Fecha máxima del del intevalo de tiempo al que pertenece la noticia
# * news_title: Título relacionado a la noticia
# * news__text__content: Texto contenido de la noticia

# In[184]:


#Estadísticas descriptivas
df= noticias
ini = len(df)
# Conteo de valores únicos
print("Dimensiones:""", str(df.shape))
print('Categorias:')
print(df.nunique())
print("\nDatos nulos:\n", str(df.isnull().sum()))
print("\nTipo de datos:\n",str(df.dtypes))

df['interval_duration'] = (df['news_final_date'] - df['news_init_date']).dt.days
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(16, 8))
#noticias por fecha
ax1.hist(df['news_init_date'], bins=30, edgecolor='black')
ax1.set_title('Histograma de Noticias por Fecha')
ax1.set_xlabel('Fecha')
ax1.set_ylabel('Cantidad de Noticias')
# duración del intervalo
ax2.hist(df['interval_duration'], bins=30, edgecolor='black')
ax2.set_title('Histograma de la Duración del Intervalo de las Noticias')
ax2.set_xlabel('Duración del Intervalo (días)')
ax2.set_ylabel('Cantidad de Noticias')
plt.subplots_adjust(hspace=0.5)
plt.rcParams['font.family'] = 'arial'
plt.rcParams['font.size'] = 14
plt.show()


# ### clientes_noticias.csv
# 
# clientes_noticias.csv: Relación entre cliente y las noticias consultadas mediante el proceso de descarga de información
# * new_id: Identificador único del cliente
# * news_url_absolute: url de la noticia encontrada
# * news_init_date: Fecha mínima del intevalo de tiempo al que pertenece la noticia
# * news_final_date: Fecha máxima del del intevalo de tiempo al que pertenece la noticia

# In[156]:


#Estadísticas descriptivas

df= clientes_noticias

ini = len(df)
# Conteo de valores únicos
print("Dimensiones:""", str(df.shape))
print('Categorias:')
print(df.nunique())
#from colorama import init, Fore, Back, Style
#df['Direction'] = df['Direction'].map({'Up': 1, 'Down': 0})
print("\nDatos nulos:\n", str(df.isnull().sum()))
print("\nTipo de datos:\n",str(df.dtypes))


# In[186]:


df['interval_duration'] = (df['news_final_date'] - df['news_init_date']).dt.days
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(16, 8))
#noticias por fecha
ax1.hist(df['news_init_date'], bins=30, edgecolor='black')
ax1.set_title('Histograma de Noticias por Fecha')
ax1.set_xlabel('Fecha')
ax1.set_ylabel('Cantidad de Noticias')
# duración del intervalo
ax2.hist(df['interval_duration'], bins=30, edgecolor='black')
ax2.set_title('Histograma de la Duración del Intervalo de las Noticias')
ax2.set_xlabel('Duración del Intervalo (días)')
ax2.set_ylabel('Cantidad de Noticias')
plt.subplots_adjust(hspace=0.5)
plt.rcParams['font.family'] = 'arial'
plt.rcParams['font.size'] = 14
plt.show()


# In[198]:


import pandas as pd
import matplotlib.pyplot as plt

# Carga la base de datos de clientes_noticias
#clientes_noticias = pd.read_csv('clientes_noticias.csv')

# Agrupa los datos por cliente y cuenta el número de noticias por cliente
noticias_por_cliente = clientes_noticias.groupby('nit')['news_id'].count()

# Calcula estadísticas descriptivas de la distribución de noticias por cliente
print('Estadísticas descriptivas de la distribución de noticias por cliente:')
print(noticias_por_cliente.describe())

# Crea un histograma del número de noticias por cliente
plt.hist(noticias_por_cliente, bins=30)
plt.xlabel('Número de noticias')
plt.ylabel('Número de clientes')
plt.title('Histograma del número de noticias por cliente')
plt.show()


# In[ ]:




