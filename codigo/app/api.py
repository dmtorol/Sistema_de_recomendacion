from flask import Flask, request, jsonify
import pandas as pd
from gensim import  models
from gensim.corpora import Dictionary


app = Flask(__name__)

# Ruta que requiere dos parámetros en la URL
@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json(force=True)
    num_reco   = int(data['num_reco'])
    news_title = data['news_title']
    
    # Obtener los parámetros de la URL
    #parametro1 = request.args.get('parametro1')
    #parametro2 = request.args.get('parametro2')

    # Verificar que ambos parámetros estén presentes
    #if parametro1 is None or parametro2 is None:
    #    return jsonify({'error': 'Se requieren dos parámetros: parametro1 y parametro2'}), 400

    # Realizar alguna operación con los parámetros (en este caso, simplemente sumarlos)
    #resultado = int(parametro1) + int(parametro2)
    #resultado = pd.DataFrame.from_dict(data, orient='columns')
    #resultado = pd.DataFrame([[parametro1,parametro2]], columns=['parametro1', 'parametro2']).to_json(orient='records')
    resultado = recomendador_lda(news_title, df_news, num_reco).to_json(orient='records')
    # Devolver dos parámetros en la respuesta
    respuesta = {'resultado' : resultado}#, 
                 #'parametro1': parametro1, 
                 #'parametro2': parametro2}
    #respuesta = {'resultado': parametro1}
    return jsonify(respuesta)


def recomendador_lda(news_title, df, num_reco):
    topic_new = df[df.news_title == news_title].topic.values[0]
    subsec_new = df[df.news_title == news_title].subsec.values[0]
    df = df[df.subsec == subsec_new]
    df = df[df.news_title != news_title].copy()

    return df[df.topic == topic_new].sort_values(by='topic_proba', ascending=False)[['news_title','subsec', 'news_url_absolute']].reset_index(drop=True)[0:num_reco]



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


# Ejecutar la aplicación en el puerto 5000 de forma predeterminada
if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=8080)
