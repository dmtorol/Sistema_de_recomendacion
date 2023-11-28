#!/usr/bin/env python
# coding: utf-8

import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import mlflow
import mlflow.sklearn
import dvc.api

# Función para cargar datos desde DVC
#def load_data_dvc(path):
#    with dvc.api.open(
#        path, repo='https://github.com/dmtorol/Sistema_de_recomendacion.git', rev='main'
#    ) as fd:
#        data = pd.read_csv(fd)
#    return data

# Carga de datos desde DVC ...
# clientes = load_data_dvc('data/clientes.csv.dvc')
# clientes_noticias = load_data_dvc('data/clientes_noticias.csv.dvc')
# noticias = load_data_dvc('data/noticias.csv.dvc')


clientes = pd.read_csv('clientes.csv')
clientes_noticias = pd.read_csv('clientes_noticias.csv')
noticias = pd.read_csv('noticias.csv')
extra_stopwords = pd.read_csv('extra_stopwords.csv')


cli = clientes_noticias.merge(clientes, how='left', on='nit')
noticias_subsec = cli[['news_id', 'subsec']].groupby('news_id').apply(pd.DataFrame.mode).reset_index(drop=True)
df = noticias.merge(noticias_subsec, how='inner', on='news_id')

top_news = list(df.subsec.value_counts()[10:13].index)
df_news = df[df.subsec.isin(top_news)].reset_index(drop=True).copy()

# Procesamiento de texto ...
import unidecode
import re
import spacy

nlp = spacy.load("es_core_news_sm")

extra_stopwords.columns = ['stopwords']
extra_stopwords = set(extra_stopwords['stopwords'].to_list())

nlp.Defaults.stop_words |= extra_stopwords

def text_cleaning(txt):
    out = unidecode.unidecode(txt)
    out = re.sub("[^\\w\\s]|\n", ' ', out)
    out = re.sub("\d+", "", out)
    out = re.sub('\s+', ' ', out)

    out = out.lower()
    out = nlp(out)
    out = [token.text for token in out if not token.is_stop]
    out = " ".join(out)
    lemmas = [token.lemma_ for token in nlp(out)]
    out = " ".join(lemmas)
    out = [token.text for token in nlp(out) if len(token) > 2]

    return out

clean_txt = list(map(text_cleaning, df_news['news_text_content']))
clean = [' '.join(i) for i in clean_txt]
df_news['news_text_content_clean'] = clean

# CountVectorizer
count = CountVectorizer(stop_words=list(nlp.Defaults.stop_words))
count_matrix = count.fit_transform(df_news['news_text_content_clean'])
cosine_sim_matrix = cosine_similarity(count_matrix, count_matrix)

# Define la función recomendador
def recomendador(news_title, cosine_sim, df):
    df = df.reset_index()
    indices = pd.Series(df.index, index=df['news_title']).drop_duplicates()
    idx = indices[news_title]
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:6]
    news_indices = [i[0] for i in sim_scores]
    reco = df['news_title'].iloc[news_indices].reset_index(drop=True)
    reco.index += 1
    return reco, df['subsec'].iloc[news_indices].reset_index(drop=True), sim_scores

# Registra el experimento
#mlflow.set_tracking_uri('http://localhost:5000')
experiment = mlflow.set_experiment("recommendation-system")

# Inicia el seguimiento de MLflow
with mlflow.start_run(experiment_id=experiment.experiment_id):
    # Define el modelo de recomendación
    target_news_title = df_news['news_title'][0]
    recommendations, subsec, sim_scores = recomendador(target_news_title, cosine_sim_matrix, df_news)

    # Registra información relevante en MLflow
    mlflow.log_param("target_news_title", target_news_title)
    mlflow.log_param("recommendations", recommendations.to_list())
    mlflow.log_param("subsec", subsec.to_list())

    # Registra la matriz de similitud de coseno como un artefacto
    pd.DataFrame(cosine_sim_matrix).to_csv("cosine_sim_matrix.csv", index=False, header=False)
    mlflow.log_artifact("cosine_sim_matrix.csv")

    # Imprime las recomendaciones y la similitud para verificar
    print("Recommendations:", recommendations)
    print("Subsec:", subsec)
    print("Similarity Scores:", sim_scores)
