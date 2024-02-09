from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Importar os modelos aqui
from .Navio import Navio
from .User import User

