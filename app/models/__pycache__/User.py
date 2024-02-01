from . import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True, nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)

def criar_usuario(username, email, password):
    novo_usuario = User(
        username=username,
        email=email,
        password=password
    )
    db.session.add(novo_usuario)
    db.session.commit()

def consultar_usuarios():
    return User.query.all()

# Função para atualizar um usuário
def atualizar_usuario(id, novo_email):
    usuario = User.query.get(id)
    if usuario:
        usuario.email = novo_email
        db.session.commit()

# Função para excluir um usuário
def excluir_usuario(id):
    usuario = User.query.get(id)
    if usuario:
        db.session.delete(usuario)
        db.session.commit()
