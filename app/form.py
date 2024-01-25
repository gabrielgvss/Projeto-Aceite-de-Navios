from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import StringField, FloatField, IntegerField, SubmitField, SelectField

class CadastroForm(FlaskForm):
    nome = StringField('Nome do Navio', render_kw={'class': 'form-control'})
    loa = FloatField('LOA (metros)', render_kw={'class': 'form-control'})
    boca = FloatField('Boca (metros)', render_kw={'class': 'form-control'})
    dwt = IntegerField('DWT', render_kw={'class': 'form-control'})
    calado_entrada = FloatField('Calado de Entrada (metros)', render_kw={'class': 'form-control'})
    calado_saida = FloatField('Calado de Saída (metros)', render_kw={'class': 'form-control'})
    calado_aereo = FloatField('Calado Aéreo (metros)', render_kw={'class': 'form-control'})
    pontal = FloatField('Pontal (metros)', render_kw={'class': 'form-control'})
    tamanho_lanca = FloatField('Tamanho da Lança (metros)', render_kw={'class': 'form-control'})
    ano_construcao = IntegerField('Ano de Construção', render_kw={'class': 'form-control'})
    tipo_navio = SelectField('Tipo de Navio', choices=["GS", "CG", "GSM", "GLP", "CNTR", "GL", "GLP"], render_kw={'class': 'form-control'})
    ultimo_porto = StringField('Último Porto', render_kw={'class': 'form-control'})
    proximo_porto = StringField('Próximo Porto', render_kw={'class': 'form-control'})
    arquivo_csv = FileField('Upload do arquivo CSV', validators=[
        FileRequired(),
        FileAllowed(['csv'], 'Apenas arquivos CSV são permitidos.')
        ], render_kw={'class': 'form-control'})

    submit = SubmitField('Enviar', render_kw={'class': 'btn btn-dark w-25 btn-submit'})
