from flask import Blueprint

navio_bp = Blueprint('navio_bp', __name__)

@navio_bp.route("/navio")
def navio():
    return "Esta é a página do navio."
