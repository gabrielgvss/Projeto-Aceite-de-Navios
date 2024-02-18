from flask import Response, request
from app.models.__pycache__.Navio import Navio
from flask_sqlalchemy import SQLAlchemy
import json
from app import db
from flask_login import current_user



def index():
    session = db.session()
    navios = session.query(Navio).all()
    navios_json = [navio.serialize() for navio in navios] 
    session.close()
    return Response(json.dumps(navios_json))

def cadastrar_navio(navio_info):
    print("Dados recebidos para cadastro do navio:")
    print(navio_info)
    
    session = db.session()
    try:
        navio = Navio(
            nome=navio_info['Nome do Navio'],  
            loa=navio_info['LOA (metros)'],  
            boca=navio_info['Boca (metros)'],  
            dwt=navio_info['DWT'],  
            calado_entrada=navio_info['Calado de Entrada (metros)'],  
            calado_saida=navio_info['Calado de Saída (metros)'],  
            calado_aereo=navio_info['Calado Aéreo (metros)'],  
            pontal=navio_info['Pontal (metros)'],  
            tamanho_lanca=navio_info['Tamanho da Lança (metros)'],  
            ano_construcao=navio_info['Ano de Construção'],  
            tipo_navio=navio_info['Tipo de Navio'],  
            situacao=navio_info['Situacao'],
            user_id=current_user.id
        )
        session.add(navio)
        session.commit()
        print("Navio cadastrado com sucesso.")
        return Response(json.dumps(navio.serialize()))
    except Exception as e:
        session.rollback()
        print("Erro ao cadastrar o navio:", e)
        # Aqui você pode adicionar uma mensagem de erro ou qualquer tratamento adicional
        return Response(json.dumps({'error': 'Ocorreu um erro ao cadastrar o navio.'}), status=500)
    finally:
        session.close()
