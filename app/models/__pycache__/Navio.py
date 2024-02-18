from flask import jsonify
from . import db

class Navio(db.Model):
    __tablename__ = 'Navios'
    id_navio = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(255), unique=True, nullable=False)
    loa = db.Column(db.Float, nullable=False)
    boca = db.Column(db.Float, nullable=False)
    dwt = db.Column(db.Float, nullable=False)
    calado_entrada = db.Column(db.Float, nullable=False)
    calado_saida = db.Column(db.Float, nullable=False)
    calado_aereo = db.Column(db.Float, nullable=False)
    pontal = db.Column(db.Float, nullable=False)
    tamanho_lanca = db.Column(db.Float, nullable=False)
    ano_construcao = db.Column(db.Integer, nullable=False)
    tipo_navio = db.Column(db.String(50), nullable=False)
    situacao = db.Column(db.String(50), nullable=False)
    
    # Relação com a tabela de Usuários
    user_id = db.Column(db.Integer, db.ForeignKey('Users.id', name='fk_user_id'), nullable=False)
    user = db.relationship('User', backref=db.backref('navios', lazy=True))

    def serialize(self):
        return {
            'id_navio': self.id_navio,
            'name': self.nome,
            'loa': self.loa,
            'boca': self.boca,
            'dwt': self.dwt,
            'calado_entrada': self.calado_entrada,
            'calado_saida': self.calado_saida,
            'calado_aereo': self.calado_aereo,
            'pontal': self.pontal,
            'tamanho_lanca': self.tamanho_lanca,
            'ano_construcao': self.ano_construcao,
            'tipo_navio': self.tipo_navio,
            'situacao': self.situacao,
            'user_id': self.user_id
        }


# def criar_navio(nome, loa, boca, dwt, calado_entrada, calado_saida, calado_aereo, pontal, tamanho_lanca, ano_construcao, tipo_navio):
#     novo_navio = Navio(
#         nome=nome,
#         loa=loa,
#         boca=boca,
#         dwt=dwt,
#         calado_entrada=calado_entrada,
#         calado_saida=calado_saida,
#         calado_aereo=calado_aereo,
#         pontal=pontal,
#         tamanho_lanca=tamanho_lanca,
#         ano_construcao=ano_construcao,
#         tipo_navio=tipo_navio
#     )
#     db.session.add(novo_navio)
#     db.session.commit()
#     return jsonify({"message": "Navio criado com sucesso!"})

# def consultar_navios():
#     navios = Navio.query.all()
#     navios_json = [{"nome": navio.nome, "tipo_navio": navio.tipo_navio} for navio in navios]
#     return jsonify({"navios": navios_json})

# def atualizar_navio(nome_antigo, novo_tipo_navio):
#     navio = Navio.query.filter_by(nome=nome_antigo).first()
#     if navio:
#         navio.tipo_navio = novo_tipo_navio
#         db.session.commit()
#         return jsonify({"message": "Navio atualizado com sucesso!"})
#     else:
#         return jsonify({"error": "Navio não encontrado."}), 404

# def excluir_navio(nome):
#     navio = Navio.query.filter_by(nome=nome).first()
#     if navio:
#         db.session.delete(navio)
#         db.session.commit()
#         return jsonify({"message": "Navio excluído com sucesso!"})
#     else:
#         return jsonify({"error": "Navio não encontrado."}), 404