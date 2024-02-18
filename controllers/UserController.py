from flask import Response, request
from app.models.__pycache__.User import User
from flask_sqlalchemy import SQLAlchemy
import json
from app import db
from werkzeug.security import generate_password_hash

def index():
    session = db.session()
    users = session.query(User).all()
    users_json = [user.serialize() for user in users]
    session.close()
    return Response(json.dumps(users_json))



def criar_usuario(username, email, password):
    novo_usuario = User(
        username=username,
        email=email,
        password_hash=generate_password_hash(password)
    )
    db.session.add(novo_usuario)
    db.session.commit()


def consultar_usuarios():
    return User.query.all()
