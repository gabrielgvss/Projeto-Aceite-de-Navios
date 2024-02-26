import os
import time
import pandas as pd
from flask import Flask, render_template, request, redirect, url_for, jsonify, session
from werkzeug.security import generate_password_hash
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
from flask_login import LoginManager, login_user, current_user
from datetime import datetime
import logging
from logging.handlers import RotatingFileHandler

login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    handler = RotatingFileHandler('app.log', maxBytes=10000, backupCount=1)  # Arquivo de log rotativo
    handler.setLevel(logging.DEBUG)  # Define o nível de log para DEBUG

    app.logger.addHandler(handler)
    
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
        if current_user.is_authenticated:
            return render_template('index.html')  # Página principal quando logado
        else:
            return redirect(url_for('login'))  # Redireciona para a página de login

      

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

            dados_formulario['Situacao'] = 'EM ANÁLISE'
            
            # Chame a função cadastrar_navio apenas uma vez, dentro do escopo do bloco condicional
            
            cadastrar_navio(dados_formulario)
            time.sleep(4)

        # Renderize o formulário caso o método não seja POST ou a validação do formulário falhe
        return render_template("cadastro-navio.html", form=form)



    @app.route("/relatorio")
    def relatorio_solicitacao():
        navios = Navio.query.all()
        
        dados_tabela = []
       
        for navio in navios:
            dados_navios = {
                "id_navio": navio.id_navio,
                "nome": navio.nome,
                "situacao": navio.situacao,
                "data": navio.data_cadastro.strftime("%d/%m/%Y")
            }
            dados_tabela.append(dados_navios)
        return render_template("relatorio_solicitacao.html", dados_tabela = dados_tabela)

    @app.route("/perfil/<int:id_navio>", methods=['GET', 'POST'])
    def perfil(id_navio):
        navio = Navio.query.get_or_404(id_navio)
        form = PerfilForm(obj=navio)

        if request.method == 'POST':
            if 'editar' in request.form:
                return render_template("perfil.html", form=form, id_navio=id_navio)  # Retorna o template sem fazer nada

            if form.validate_on_submit():
                form.populate_obj(navio)
                db.session.commit()
                return redirect(url_for('perfil', id_navio=id_navio))

        return render_template("perfil.html", form=form, id_navio=id_navio)
    
    
    @app.route("/visualizar", methods=['GET'])
    def visualizar():
        navios = Navio.query.all()
        
        dados_tabela = []
       
        for navio in navios:
            dados_navios = {
                "id_navio": navio.id_navio,
                "nome": navio.nome,
                "situacao": navio.situacao,
                "data": navio.data_cadastro.strftime("%d/%m/%Y")
            }
            dados_tabela.append(dados_navios)
        return render_template("relatorio_solicitacao.html", dados_tabela = dados_tabela)
    
    @app.route("/editar/<int:id_navio>", methods=['GET', 'POST'])
    def editar(id_navio):
        navio = Navio.query.get_or_404(id_navio)
        form = PerfilForm(obj=navio)

        if request.method == 'POST':
            if form.validate_on_submit():
                form.populate_obj(navio)
                db.session.commit()
                return redirect(url_for('visualizar', id_navio=id_navio))

        return render_template("editar.html", form=form, id_navio=id_navio)
    
        
    @app.route("/solicitar", methods=['GET'])
    def exibir_solicitar():
        navios = Navio.query.all()  # Recupera todos os navios do banco de dados
        return render_template("solicitar.html", navios=navios)

    @app.route("/solicitar/<int:id_navio>", methods=['GET'])
    def exibir_pagina_solicitar(id_navio):
        if request.method == 'GET':
            navios = Navio.query.filter_by(id_navio=id_navio).first()  # Alterado aqui
            return render_template("solicitar.html", navios=navios,id_navio=id_navio ) 
       

    @app.route("/processar_solicitacao/<int:id_navio>", methods=['POST','PUT'])
    def processar_solicitacao(id_navio):
        if request.method == 'POST' or request.method == 'PUT':
            print("Recebendo solicitação para processar o navio ID:", id_navio)
            navio = Navio.query.get_or_404(id_navio)
            mensagem = None

            if navio:
                # Realizar a predição
                dados_para_predicao = {
                    'LOA (metros)': navio.loa,
                    'Boca (metros)': navio.boca,
                    'DWT': navio.dwt,
                    'Calado de Entrada (metros)': navio.calado_entrada,
                    'Calado de Saída (metros)': navio.calado_saida,
                    'Ano de Construção': navio.ano_construcao
                }
                resultado_predicao = realizar_predicao(dados_para_predicao)

                # Editar a situação do navio com base no resultado da predição
                if resultado_predicao == 1:
                    navio.situacao = 'REPROVADO'
                elif resultado_predicao == 0:
                    navio.situacao = 'APROVADO'
                else:
                    navio.situacao = 'EM ANÁLISE'

                # Salvar alterações no banco de dados
                db.session.commit()

                # Preparar mensagem com base na nova situação do navio
                situacao_atualizada = navio.situacao
                if situacao_atualizada == 'REPROVADO':
                    mensagem = "Solicitação recusada!"
                elif situacao_atualizada == 'APROVADO':
                    mensagem = "Solicitação aprovada!"
                else:
                    mensagem = "Situação do navio desconhecida."
            
        print("Mensagem de resposta:", mensagem)
        return render_template("resultado_solicitacao.html", mensagem=mensagem)



    @app.route("/ajuda")
    def ajuda():
        return render_template("ajuda.html")
    

    @app.route("/suporte")
    def suporte():
        return render_template("suporte.html")
        
    @app.route("/cadastro-user", methods=['GET', 'POST'])
    def cadastro_user():
        form = UserPerfil()
        if request.method == 'POST':
            username = request.form['username']
            email = request.form['email']
            password = request.form['password']
            confirm_password = request.form['confirm_password']

            # Verificar se o nome de usuário já está em uso
            existing_user = User.query.filter_by(username=username).first()
            if existing_user:
                return "Nome de usuário já está em uso. Por favor, escolha outro."

            # Criptografar a senha antes de armazená-la no banco de dados
            hashed_password = generate_password_hash(password)

            # Criar um novo usuário
            new_user = User(username=username, email=email)
            new_user.set_password(password)


            # Adicionar o novo usuário ao banco de dados
            db.session.add(new_user)
            db.session.commit()

            return redirect(url_for('login'))  # Redirecionar para a página de login após o cadastro bem-sucedido

        return render_template("cadastro_usuario.html", form=form)
    
    @app.route("/perfil-user",methods=['GET','POST'])
    def perfil_user():
        return render_template("perfil_usuario.html")
    
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    

    # Configurando o logger    
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    @app.route("/login", methods=["GET", "POST"])
    def login():
        if 'logged_in' in session:
            return redirect(url_for('homepage'))  # Redireciona para a página principal se o usuário já estiver logado

        form = LoginForm()
        
        if request.method == "POST":
            print("Entrou no método POST do login")  # Adicionando mensagem de depuração
            
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
                    
                    # Adicionando mensagem de depuração antes do redirecionamento
                    print("Redirecionando para a página principal após o login bem-sucedido")
                    
                    # Redirecione para a página após o login bem-sucedido
                    return redirect(url_for("homepage"))
                else:
                    print("Senha incorreta")
            else:
                print("Usuário não encontrado no banco de dados")
        
        # Renderize o template de login novamente se as credenciais forem inválidas
        return render_template('login.html', form=form)
    




    return app
