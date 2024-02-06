import pandas as pd
from flask import Flask, render_template, request
from app.form import CadastroForm, PerfilForm
from flask_wtf.csrf import CSRFProtect
import joblib
import numpy as np
from lime.lime_tabular import LimeTabularExplainer

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'sua_chave_secreta_aqui'

    csrf = CSRFProtect(app)

    modelo_treinado = joblib.load('modelo_a.joblib')

    def realizar_predicao(dados):
        dados_predicao = np.array([
            dados['LOA (metros)'],
            dados['Boca (metros)'],
            dados['DWT'],
            dados['Calado de Entrada (metros)'],
            dados['Calado de Saída (metros)'],
            dados['Ano de Construção']
        ]).reshape(1, -1)

        resultado_predicao = modelo_treinado.predict(dados_predicao)
        return resultado_predicao[0]

    def preencher_formulario_com_dados(form, dados):
        for campo, valor in dados.items():
            if campo in form._fields:
                form._fields[campo].data = valor

    @app.route("/")
    def homepage():
        return render_template("index.html")

    @app.route("/cadastro", methods=['GET', 'POST'])
    def cadastro():
        form = CadastroForm()

        if request.method == 'POST':
            if form.validate_on_submit():
                dados_formulario = {
                    'Nome do Navio': form.nome.data,
                    'LOA (metros)': form.loa.data,
                    'Boca (metros)': form.boca.data,
                    'DWT': form.dwt.data,
                    'Calado de Entrada (metros)': form.calado_entrada.data,
                    'Calado de Saída (metros)': form.calado_saida.data,
                    'Calado Aéreo (metros)': form.calado_aereo.data,
                    'Pontal (metros)': form.pontal.data,
                    'Tamanho da Lança (metros)': form.tamanho_lanca.data,
                    'Ano de Construção': form.ano_construcao.data,
                    'Tipo de Navio': form.tipo_navio.data
                }

                # Adicione campos extras do formulário, mesmo que não sejam usados na predição
                dados_formulario['Último Porto'] = form.ultimo_porto.data
                dados_formulario['Próximo Porto'] = form.proximo_porto.data

                # Verifique se o arquivo foi fornecido
                if form.arquivo_csv.data:
                    try:
                        arquivo_upload = form.arquivo_csv.data
                        df = pd.read_csv(arquivo_upload, skiprows=1)

                        # Verifique se o DataFrame do CSV não está vazio
                        if not df.empty:
                            print("DataFrame do CSV:")
                            print(df)

                            # Preencha os campos do formulário com os dados do arquivo CSV
                            form.nome.data = df['Nome'].iloc[0]
                            form.loa.data = df['LOA (m)'].iloc[0]
                            form.boca.data = df['Boca (m)'].iloc[0]
                            form.dwt.data = df['DWT (ton)'].iloc[0]
                            form.calado_entrada.data = df['Calado de Entrada (m)'].iloc[0]
                            form.calado_saida.data = df['Calado de Saída (m)'].iloc[0]
                            form.calado_aereo.data = df['Calado Aéreo (m)'].iloc[0]
                            form.pontal.data = df['Pontal (m)'].iloc[0]
                            form.tamanho_lanca.data = df['Tamanho de Lança (m)'].iloc[0]
                            form.ano_construcao.data = df['Ano de Construção'].iloc[0]
                            form.tipo_navio.data = df['Tipo do Navio'].iloc[0]
                    except Exception as e:
                        print(f"Erro ao processar o arquivo CSV: {e}")
                        # Trate o erro conforme necessário

                # Continue com a lógica de validação e predição
                resultado_predicao = realizar_predicao(dados_formulario)

                if resultado_predicao == 1:
                    return render_template("recusado.html", dados=dados_formulario)
                else:
                    return render_template("cadastro_sucesso.html", dados=dados_formulario)

        return render_template("cadastro.html", form=form)

    @app.route("/login")
    def login():
        return render_template("login.html")

    @app.route("/relatorio")
    def relatorio_solicitacao():
        dados_tabela = [
        {"id_navio": 1, "nome": "ANavio 1", "situacao" : "REPROVADO", "data" : "02/11/2022"},
        {"id_navio": 2, "nome": "CNavio 2","situacao" : "APROVADO", "data" : "30/09/2022"},
        {"id_navio": 3, "nome": "DNavio 3","situacao" : "REPROVADO", "data" : "17/09/2022"},
        {"id_navio": 4, "nome": "BNavio 4","situacao" : "REPROVADO", "data" : "21/10/2022"},
        {"id_navio": 5, "nome": "ENavio 5","situacao" : "APROVADO", "data" : "13/11/2022"}
        ]
        return render_template("relatorio_solicitacao.html", dados_tabela = dados_tabela)

    @app.route("/perfil/<int:id_navio>", methods=['GET', 'POST'])
    def perfil(id_navio):

        form = PerfilForm()

        if request.method == 'POST':
            if form.validate_on_submit():
                dados_formulario = {
                    'Nome do Navio': form.nome.data,
                    'LOA (metros)': form.loa.data,
                    'Boca (metros)': form.boca.data,
                    'DWT': form.dwt.data,
                    'Calado de Entrada (metros)': form.calado_entrada.data,
                    'Calado de Saída (metros)': form.calado_saida.data,
                    'Calado Aéreo (metros)': form.calado_aereo.data,
                    'Pontal (metros)': form.pontal.data,
                    'Tamanho da Lança (metros)': form.tamanho_lanca.data,
                    'Ano de Construção': form.ano_construcao.data,
                    'Tipo de Navio': form.tipo_navio.data
                }

        #fazer update dos dados do navio

        #pegar dados do navio e fazer um get no banco
        #dados fake
        navio = {
            'Nome do Navio': 'Navio20',
            'LOA (metros)': 285,
            'Boca (metros)': 48,
            'DWT': 143643,
            'Calado de Entrada (metros)': 17,
            'Calado de Saída (metros)': 14,
            'Calado Aéreo (metros)': 10,
            'Pontal (metros)': 14,
            'Tamanho da Lança (metros)': 16,
            'Ano de Construção': 2000,
            'Tipo de Navio': "BPL",
            'situacao': "REPROVADO",
            'motivacao': "Ano de construção"
        }

        form.nome.data = navio['Nome do Navio']
        form.loa.data = navio['LOA (metros)']
        form.boca.data = navio['Boca (metros)']
        form.dwt.data = navio['DWT']
        form.calado_entrada.data = navio['Calado de Entrada (metros)']
        form.calado_saida.data = navio['Calado de Saída (metros)']
        form.calado_aereo.data = navio['Calado Aéreo (metros)']
        form.pontal.data = navio['Pontal (metros)']
        form.tamanho_lanca.data = navio['Tamanho da Lança (metros)']
        form.ano_construcao.data = navio['Ano de Construção']
        form.tipo_navio.data = navio['Tipo de Navio']
        form.situacao.data = navio['situacao']
        form.motivacao.data = navio['motivacao']
                
        return render_template("perfil.html", form=form)
    
    @app.route("/solicitar")
    def solicitar():
        dados_tabela = [
            {"id_navio": 1, "nome": "ANavio 1", "situacao": "REPROVADO", "data": "02/11/2022"},
            {"id_navio": 2, "nome": "CNavio 2", "situacao": "APROVADO", "data": "30/09/2022"},
            {"id_navio": 3, "nome": "DNavio 3", "situacao": "REPROVADO", "data": "17/09/2022"},
            {"id_navio": 4, "nome": "BNavio 4", "situacao": "REPROVADO", "data": "21/10/2022"},
            {"id_navio": 5, "nome": "ENavio 5", "situacao": "APROVADO", "data": "13/11/2022"}
        ]
        return render_template("solicitar.html", dados_tabela=dados_tabela)


    @app.route("/ajuda")
    def ajuda():
        return render_template("ajuda.html")
    

    @app.route("/suporte")
    def suporte():
        return render_template("suporte.html")
    
    @app.route("/cadastro-user")
    def cadastro_user():
        return render_template("cadastro_usuario.html")
    
    @app.route("/perfil-user")
    def perfil_user():
        return render_template("perfil_usuario.html")

    return app

