from flask_restful import Resource, marshal, reqparse
from helpers.database import db
from Models.Municipio import tb_Municipio, tb_Municipio_fields
from flask import request
from sqlalchemy.exc import IntegrityError

class MunicipiosResource(Resource):
    def get(self):
        try:
            municipios = db.session.query(tb_Municipio).all()
            return marshal(municipios, tb_Municipio_fields), 200
        except Exception as e:
            return {"mensagem": f"Erro ao buscar municípios: {str(e)}"}, 500
        
    def post(self):
        dados = request.get_json()
        
        campos_obrigatorios = ["codmunicipio", "municipio", "coduf", "regiao"]
        for campo in campos_obrigatorios:
            if campo not in dados:
                return {"mensagem": f"Campo '{campo}' é obrigatório"}, 400

        try:
            novo_municipio = tb_Municipio(
                codmunicipio=dados["codmunicipio"],
                municipio=dados["municipio"],
                coduf=dados["coduf"],
                regiao=dados["regiao"]
            )
            db.session.add(novo_municipio)
            db.session.commit()
            return marshal(novo_municipio, tb_Municipio_fields), 201
        except IntegrityError:
            db.session.rollback()
            return {"mensagem": "Código já existente ou violação de integridade"}, 400
        except Exception as e:
            db.session.rollback()
            return {"mensagem": f"Erro ao criar município: {str(e)}"}, 500

class MunicipioResource(Resource):
    def get(self, id=None):
        try:
            if id is not None:
                municipio = db.session.get(tb_Municipio, id)
                if not municipio:
                    return {"mensagem": "Município não encontrado"}, 404
                return marshal(municipio, tb_Municipio_fields), 200
            
            municipios = db.session.query(tb_Municipio).all()
            return marshal(municipios, tb_Municipio_fields), 200
        except Exception as e:
            return {"mensagem": f"Erro ao buscar municípios: {str(e)}"}, 500
    
    def put(self, id):
        dados = request.get_json()
        municipio = db.session.get(tb_Municipio, id)
        if not municipio:
            return {"mensagem": "Município não encontrado"}, 404
        try:
            municipio.municipio = dados.get("municipio", municipio.municipio)
            municipio.coduf = dados.get("coduf", municipio.coduf)
            municipio.regiao = dados.get("regiao", municipio.regiao)
            db.session.commit()
            return marshal(municipio, tb_Municipio_fields), 200
        except Exception as e:
            db.session.rollback()
            return {"mensagem": f"Erro ao atualizar município: {str(e)}"}, 500
        
    def delete(self, id):
        municipio = db.session.get(tb_Municipio, id)
        if not municipio:
            return {"mensagem": "Município não encontrado"}, 404
        try:
            db.session.delete(municipio)
            db.session.commit()
            return {"mensagem": "Município excluído com sucesso"}, 200
        except Exception as e:
            db.session.rollback()
            return {"mensagem": f"Erro ao excluir município: {str(e)}"}, 500
