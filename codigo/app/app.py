#!/usr/bin/env python
# coding: utf-8

import pandas as pd
import streamlit as st
from gensim import  models
from gensim.corpora import Dictionary

st.title ("Sistema de Recomendación de Noticias Sobre Clientes Corporativos")
#st.header("Seguimiento de Datos de Entrada")
st.caption("Seguimiento de Datos de Entrada")

#st.markdown("this is the header")
#st.subheader("this is the subheader")
#st.caption("this is the caption")
#st.code("x=2021")
#st.latex(r''' a+a r^1+a r^2+a r^3 ''')

#####################

clientes = pd.read_csv('./clientes.csv')
df_cli =  clientes.desc_ciiuu_clase.value_counts().reset_index()
df_cli = df_cli.rename({'index':'Actividad Económica', 'desc_ciiuu_clase':'Nro. Noticias'}, axis=1)
df_cli['% Noticias'] = (df_cli['Nro. Noticias']/len(df_cli)*100).round(2)
df_cli['% Noticias'] = df_cli['% Noticias'].astype(str) + '%'

###################################################
st.header("Actividad Económica Principales")
st.dataframe(df_cli)

#######################################
#Tópicos
#Métricas de Evaluación
#st.header("Tópicos")
#st.header("Métricas de Evaluación")

#######################################

df_news = pd.read_pickle("./data.pkl")  
clean_txt = [i.split() for i in df_news['news_text_content_clean'].values]


# Creamos la representación de diccionario del documento
dictionary = Dictionary(clean_txt)
corpus = [dictionary.doc2bow(doc) for doc in clean_txt]

model = models.ldamodel.LdaModel.load('model')

topic = [model.get_document_topics(item)[0][0] for item in corpus]
topic_proba = [model.get_document_topics(item)[0][1] for item in corpus]

df_news['topic'] = topic
df_news['topic_proba'] = topic_proba

def recomendador_lda(news_title, df, num_reco):
    topic_new = df[df.news_title == news_title].topic.values[0]
    subsec_new = df[df.news_title == news_title].subsec.values[0]
    df = df[df.subsec == subsec_new]
    df = df[df.news_title != news_title].copy()

    return df[df.topic == topic_new].sort_values(by='topic_proba', ascending=False)[['news_title',	'subsec']].reset_index(drop=True)[0:num_reco]

st.header("Sistema de recomendación")
#new = 2

new = st.selectbox(
   "Noticia:",
   df_news.news_title,
   index=None,
   placeholder="Elige la Noticia",
)
if (new != None):
    new_id = df_news[df_news.news_title == new].index[0]

#num_reco = 2

num_reco = st.selectbox(
   "Número de recomendaciones",
   list(range(2, 6)),
   index=None,
   placeholder="Elige el número de recomendaciones",
)

#st.write('You selected:', option)



#reco_id = 0


if (new != None) and (num_reco != None):
    st.dataframe(recomendador_lda(df_news.news_title[new_id], df_news, num_reco).rename({'news_title':'Noticia', 'subsec':'Actividad Económica Principal'}, axis=1))


