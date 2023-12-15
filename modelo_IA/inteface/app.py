# app.py
from flask import Flask, render_template, request
import pandas as pd
import os
import joblib

app = Flask(__name__)

# Obtenha o diretório atual do script
script_dir = os.path.dirname(os.path.abspath(__file__))

# Caminho completo do modelo treinado
seu_modelo_path = os.path.join(script_dir, 'seu_modelo_treinado.pkl')

# Carregue o modelo treinado
if os.path.exists(seu_modelo_path):
    seu_modelo = joblib.load(seu_modelo_path)
else:
    raise FileNotFoundError(f'Modelo treinado não encontrado em {seu_modelo_path}')

def preprocess_data(df):
    # Remova a coluna 'Nome' se estiver presente
    # if 'Nome' in df.columns:
    #     df = df.drop(['Nome'], axis=1)
    # Selecione as mesmas colunas usadas durante o treinamento
    indices_previsores = [1, 2, 3, 4, 5, 9]
    df_preprocessed = df.iloc[:, indices_previsores]

    # Aplicar codificação one-hot para variáveis categóricas
    df_preprocessed = pd.get_dummies(df_preprocessed)

    return df_preprocessed

@app.route('/', methods=['GET', 'POST'])
def index():
    aviso = None  # Adicionado: Inicializa a variável de aviso

    if request.method == 'POST':
        uploaded_file = request.files['file']
        if uploaded_file.filename != '':
            # Leitura do arquivo CSV enviado pelo usuário para teste
            df_uploaded = pd.read_csv(uploaded_file)

            # Verifique se as colunas do DataFrame de teste são as mesmas usadas durante o treinamento
            if set(df_uploaded.columns) == set(['Nome', 'LOA (m)', 'Boca (m)', 'DWT (ton)', 'Calado de Entrada (m)', 'Calado de Saída (m)', 'Calado Aéreo (m)', 'Pontal (m)', 'Tamanho de Lança (m)', 'Ano de Construção', 'Tipo do Navio', 'Último Porto', 'Próximo Porto']):
                # Pré-processamento dos dados de teste
                df_uploaded_preprocessed = preprocess_data(df_uploaded)

                # Faça previsões
                previsoes = seu_modelo.predict(df_uploaded_preprocessed)

                # Mapeie os resultados para "Aceito" ou "Recusado"
                resultados_mapeados = ['Aceito' if previsao == 1 else 'Recusado' for previsao in previsoes]

                # Adicione os resultados mapeados ao DataFrame original
                df_uploaded['Situação'] = resultados_mapeados

                # Converta o DataFrame resultante para HTML
                result_html = df_uploaded.to_html(classes='table table-bordered table-striped', index=False)

                # Determine o caminho do template de resultado em relação ao diretório 'templates'
                return render_template('resultado.html', result=result_html, aviso=aviso)
            else:
                aviso = 'As colunas do arquivo de upload não correspondem às colunas esperadas.'
    
    # Determine o caminho do template de índice em relação ao diretório 'templates'
    return render_template('index.html', aviso=aviso)  # Adicionado: Passa o aviso para o template
if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)
