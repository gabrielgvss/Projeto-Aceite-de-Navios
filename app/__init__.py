import os
import pandas as pd
from flask import Flask, render_template, request, redirect, url_for
from app.form import CadastroForm, PerfilForm, UserPerfil, LoginForm
from flask_wtf.csrf import CSRFProtect
import joblib
import numpy as np
from lime.lime_tabular import LimeTabularExplainer
from app.models.__pycache__.Navio import db, Navio
from app.models.__pycache__.User import UserM, User
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from controllers.UserController import index, criar_usuario # Importe a função cadastro_user do UserController
from controllers.NavioController import cadastrar_navio
from flask_login import LoginManager, login_user


login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    
    app.config['SECRET_KEY'] = 'hjshjhdjah kjshkjdhjs'

    basedir = os.path.abspath(os.path.dirname(__file__))
    app.config['SQLALCHEMY_DATABASE_URI'] =  'sqlite:///' + os.path.join(basedir, 'data.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    login_manager.init_app(app)
    login_manager.login_view = 'login'
    
    CSRFProtect(app)
    
    db.init_app(app)
    
    migrate = Migrate(app, db)

    modelo_treinado = joblib.load('modelo_a.joblib')
    
   # Registrar blueprints
    from routes.navio_bp import navio_bp
    from routes.User_bp import user_bp
    app.register_blueprint(navio_bp, url_prefix='/navio')
    app.register_blueprint(user_bp, url_prefix='/user')


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

    @app.route("/cadastro-navio", methods=['GET', 'POST'])
    def cadastro_navio():
        form = CadastroForm()

        if request.method == 'POST' and form.validate_on_submit():
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

            resultado_predicao = realizar_predicao(dados_formulario)

            # Adicione a situação do navio ao dicionário com base no resultado da predição
            if resultado_predicao == 1:
                dados_formulario['Situacao'] = 'APROVADO'
            else:
                dados_formulario['Situacao'] = 'REPROVADO'
            
            # Chame a função cadastrar_navio apenas uma vez, dentro do escopo do bloco condicional
            cadastrar_navio(dados_formulario)

            if resultado_predicao == 1:
                return render_template("recusado.html", dados=dados_formulario)
            else:
                return render_template("cadastro_sucesso.html", dados=dados_formulario)

        # Renderize o formulário caso o método não seja POST ou a validação do formulário falhe
        return render_template("cadastro-navio.html", form=form)



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
        {"id_navio": 1, "nome": "ANavio 1", "situacao" : "REPROVADO", "data" : "02/11/2022"},
        {"id_navio": 2, "nome": "CNavio 2","situacao" : "APROVADO", "data" : "30/09/2022"},
        {"id_navio": 3, "nome": "DNavio 3","situacao" : "REPROVADO", "data" : "17/09/2022"},
        {"id_navio": 4, "nome": "BNavio 4","situacao" : "REPROVADO", "data" : "21/10/2022"},
        {"id_navio": 5, "nome": "ENavio 5","situacao" : "APROVADO", "data" : "13/11/2022"}
        ]
        return render_template("solicitar.html", dados_tabela = dados_tabela)


    @app.route("/ajuda")
    def ajuda():
        return render_template("ajuda.html")
    

    @app.route("/suporte")
    def suporte():
        return render_template("suporte.html")
    

    @app.route("/cadastro-user", methods=['GET', 'POST'])
    def cadastro_user():
        form = UserPerfil()  # Definir o formulário antes de ser usado

        if request.method == 'POST':
            # Obter os dados enviados pelo formulário
            username = request.form['username']
            email = request.form['email']
            password = request.form['password']
            confirm_password = request.form['confirm_password']
            if password == confirm_password:
                criar_usuario(username, email, password)

        return render_template("cadastro_usuario.html", form=form)
    
    @app.route("/perfil-user",methods=['GET','POST'])
    def perfil_user():
        return render_template("perfil_usuario.html")
    
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    
    import logging

    # Configurando o logger    
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))


    @app.route("/login", methods=["GET", "POST"])
    def login():
        form = LoginForm()
        
        if request.method == "POST":
            print("entrou no metodo")
            # Obter os dados do formulário
            email = request.form["email"]
            password = request.form["password"]
            
            # Imprimir os dados recebidos para depuração
            print("Email recebido:", email)
            print("Senha recebida:", password)
            
            # Verificar se o usuário existe no banco de dados e se a senha está correta
            user = User.query.filter_by(email=email).first()
            if user:
                print("Usuário encontrado no banco de dados")
                if user.check_password(password):
                    print("Senha correta")
                    # Faça login no usuário
                    login_user(user)
                    
                    # Redirecione para a página após o login bem-sucedido
                    return redirect(url_for("homepage"))
                else:
                    print("Senha incorreta")
            else:
                print("Usuário não encontrado no banco de dados")
        
        # Renderize o template de login novamente se as credenciais forem inválidas
        return render_template('login.html', form=form)



    return app
