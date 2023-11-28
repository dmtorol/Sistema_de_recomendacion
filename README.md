# Sistema de Recomendación de Noticias Sobre Clientes Corporativos

Repositorio correspondiente al proyecto **Sistema de recomendación de noticias sobre clientes corporativos**, elaborado por Marcela Toro, Natalia Sierra y Juan Latorre.

El problema abordado y su contexto es la necesidad del área comercial del grupo Bancolombia de conocer mejor a sus clientes corporativos a través de la información generada por medios de comunicación locales e internacionales. Actualmente, los comerciales del banco cuentan con miles de noticias relacionadas con cada uno de sus clientes y muy poco tiempo para su lectura y análisis. Por lo tanto, se busca determinar las noticias relevantes para un sector particular de clientes, permitiendo a la fuerza comercial informarse para atender determinado sector y ser más efectivos en su labor. Para esto sugieren segmentar las noticias relacionadas con base a los sectores y determinar las características comunes entre estas, para recomendar otras noticias relevantes, actualizadas y confiables para el área comercial.

## Datos

Fuente de datos: https://www.kaggle.com/datasets/juancamilodiazzapata/dataton-2022
Los datos utilizados en este estudio provienen del Dataton 2022, una competencia organizada por el Centro de Excelencia en Analítica, Inteligencia Artificial y Gobierno de Información del Grupo Bancolombia .  Se dividen en tres bases principales: clientes, noticias y cliente_noticias que es la relación entre ambos.

Descripción del contenido de las variables 

clientes.csv: Archivo con el listado de clientes a consultar, la descripción de su actividad económica y el subsector
-	nit: Identificador único del cliente
-	nombre: Nombre corporativo del cliente
-	desc_ciiu_división: Descripción general de la clasificación Industrial uniforme d todas las actividades económicas
-	desc_ciiu_grupo: Descripción por grupo de la clasificación Industrial uniforme d todas las actividades económicas
-	desc_ciiu_clase: : Descripción por clase de la clasificación Industrial uniforme d todas las actividades económicas
-	subsector: Clasificación de la actividad industrial
	
noticias.csv: Contenido de cada una de las noticias consultadas
-	new_id: Identificador único de noticias
-	news_url_absolute: Url de la noticia encontrada
-	news_init_date: Fecha mínima del intevalo de tiempo al que pertenece la noticia
-	news_final_date: Fecha máxima del del intevalo de tiempo al que pertenece la noticia
-	news_title: Título relacionado a la noticia
-	news__text__content: Texto contenido de la noticia
	
clientes_noticias.csv: Relación entre cliente y las noticias consultadas mediante el proceso de descarga de información
-	new_id: Identificador único del cliente
-	news_url_absolute: url de la noticia encontrada
-	news_init_date: Fecha mínima del intevalo de tiempo al que pertenece la noticia
-	news_final_date: Fecha máxima del del intevalo de tiempo al que pertenece la noticia

URL del tablero (http://44.202.237.158:8502/)
