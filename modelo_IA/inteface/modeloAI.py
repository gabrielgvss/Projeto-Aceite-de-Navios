import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import GridSearchCV, train_test_split
from sklearn.metrics import confusion_matrix, accuracy_score, classification_report
from sklearn.model_selection import cross_val_score
import joblib
import os

def treinar_modelo(caminho_arquivo):
    try:
        # Carregar o conjunto de dados
        df = pd.read_csv(caminho_arquivo)

        # Seleção de previsores e classe
        indices_previsores = [1, 2, 3, 4, 5, 9]
        previsores = df.iloc[:, indices_previsores].values
        classe = df.iloc[:, 13].values

        # Divisão dos dados em treino e teste
        p_train, p_test, c_train, c_test = train_test_split(previsores, classe, test_size=0.2, random_state=0)

        # Definição dos parâmetros para a Random Forest
        parametros = {
            'n_estimators': [10, 20, 30],
            'max_depth': [None, 10, 20],
            'min_samples_split': [2, 5, 10],
            'min_samples_leaf': [1, 2, 4],
            'max_features': ['sqrt', 'log2'],
            'criterion': ['gini', 'entropy'],
            'bootstrap': [True, False]
        }

        # Criação do classificador base
        classificador_base = RandomForestClassifier(random_state=0)

        # Configuração do GridSearchCV para escolha dos hiperparâmetros
        grid_search = GridSearchCV(classificador_base, parametros, cv=5, scoring='accuracy')

        # Execução da busca exaustiva
        grid_search.fit(p_train, c_train)

        # Obtenção dos melhores parâmetros
        melhores_parametros = grid_search.best_params_

        # Ajuste do classificador com os melhores parâmetros
        classificador = RandomForestClassifier(**melhores_parametros, random_state=0)
        classificador.fit(p_train, c_train)

        # Avaliação do modelo
        previsoes = classificador.predict(p_test)
        matriz = confusion_matrix(c_test, previsoes)
        precisao = accuracy_score(c_test, previsoes)

        print("RESULTADO DE CONFUSION MATRIZ:\n", matriz)
        print("\nACURÁCIA:", precisao)
        print("\nRELATÓRIO DE CLASSIFICAÇÃO:\n", classification_report(c_test, previsoes))

        # Avaliação através de cross-validation
        resultados_acuracia = cross_val_score(classificador, previsores, classe, cv=5, scoring='accuracy')

        print("Resultados Acurácia: ", resultados_acuracia)
        print("Acurácia média: ", np.mean(resultados_acuracia))

        # Salvando o modelo treinado
        joblib.dump(classificador, 'seu_modelo_treinado.pkl')

    except Exception as e:
        print(f"Erro durante o treinamento do modelo: {e}")

# Função para fazer previsões
def fazer_previsoes(teste_de_leitura, df, indices_previsores):
    seu_modelo_path = 'seu_modelo_treinado.pkl'

    if not os.path.exists(seu_modelo_path):
        raise FileNotFoundError(f'Modelo treinado não encontrado em {seu_modelo_path}')

    seu_modelo = joblib.load(seu_modelo_path)

    # Pré-processamento dos dados de teste
    teste_de_leitura = preprocess_data(teste_de_leitura, indices_previsores)

    # Fazer previsões
    teste_previsao = seu_modelo.predict(teste_de_leitura)

    return teste_previsao

# Função para pré-processamento dos dados de teste
def preprocess_data(df, indices_previsores):
    # Seleção das mesmas colunas usadas durante o treinamento
    df_preprocessed = df.iloc[:, indices_previsores]

    # Aplicação de codificação one-hot para variáveis categóricas
    df_preprocessed = pd.get_dummies(df_preprocessed)

    # Manipulação de valores ausentes, se necessário
    # ...

    return df_preprocessed

if __name__ == '__main__':
    # Caminho para o arquivo de dados
    caminho_arquivo = r'\Projeto-Aceite-de-Navios\dados_simulacao\dados_simulacao2.csv'

    # Treinar o modelo
    treinar_modelo(caminho_arquivo)


