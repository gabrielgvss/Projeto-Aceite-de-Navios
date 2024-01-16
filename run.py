from flask import Flask, render_template
from app.form import CadastroForm
from flask_wtf.csrf import CSRFProtect
import joblib
import numpy as np
from lime.lime_tabular import LimeTabularExplainer

app = Flask(__name__)
app.config['SECRET_KEY'] = 'sua_chave_secreta_aqui'

csrf = CSRFProtect(app)

modelo_treinado = joblib.load('modelo_a.joblib')

@app.route("/")
def homepage():
    return render_template("index.html")


@app.route("/cadastro", methods=['GET', 'POST'])
def cadastro():
    form = CadastroForm()

    if form.validate_on_submit():
        dados_formulario = {
            'nome': form.nome.data,
            'loa': form.loa.data,
            'boca': form.boca.data,
            'dwt': form.dwt.data,
            'calado_entrada': form.calado_entrada.data,
            'calado_saida': form.calado_saida.data,
            'calado_aereo': form.calado_aereo.data,
            'pontal': form.pontal.data,
            'tamanho_lanca': form.tamanho_lanca.data,
            'ano_construcao': form.ano_construcao.data,
            'tipo_navio': form.tipo_navio.data,
            'ultimo_porto': form.ultimo_porto.data,
            'proximo_porto': form.proximo_porto.data,
           
        }
        # Realize a predição com o modelo treinado
        dados_predicao = [
            dados_formulario['loa'],
            dados_formulario['boca'],
            dados_formulario['dwt'],
            dados_formulario['calado_entrada'],
            dados_formulario['calado_saida'],
            dados_formulario['ano_construcao']
        ]

        # Adapte os dados de entrada conforme necessário para o modelo
        dados_predicao = np.array(dados_predicao).reshape(1, -1)

        # Realize a predição
        resultado_predicao = modelo_treinado.predict(dados_predicao)

        # Avalie o resultado e redirecione conforme necessário
        if resultado_predicao == 1:
            # Se a predição for 1 (recusado), redirecione para a página de recusa
            return render_template("recusado.html", dados=dados_formulario)
        else:
            # Se a predição for 0 (aceito), redirecione para a página de aceitação
            return render_template("cadastro_sucesso.html", dados=dados_formulario)

    return render_template("cadastro.html", form=form)


if __name__ == "__main__":
    app.run(debug=True)
