from flask_restful import Resource, marshal
from helpers.database import db
from Models.Mesorregiao import tb_Mesorregiao, tb_Mesorregiao_fields
from flask import request
from sqlalchemy.exc import IntegrityError

class MesorregioesResource(Resource):
    def get(self):
        try:
            mesorregioes = db.session.query(tb_Mesorregiao).all()
            return marshal(mesorregioes, tb_Mesorregiao_fields), 200
        except Exception as e:
            return {"mensagem": f"Erro ao buscar mesorregioes: {str(e)}"}, 500
        
    def post(self):
        dados = request.get_json()
        try:
            nova_meso = tb_Mesorregiao(
                codmesorregiao=dados["codmesorregiao"],
                mesorregiao=dados["mesorregiao"],
                coduf=dados["coduf"],
                regiao=dados["regiao"]
            )
            db.session.add(nova_meso)
            db.session.commit()
            return marshal(nova_meso, tb_Mesorregiao_fields), 201
        except IntegrityError:
            db.session.rollback()
            return {"mensagem": "Código já existente ou violação de integridade"}, 400
        except Exception as e:
            db.session.rollback()
            return {"mensagem": f"Erro ao criar mesorregião: {str(e)}"}, 500

class MesorregiaoResource(Resource):
    def get(self, id=None):
        try:
            if id is not None:
                meso = db.session.get(tb_Mesorregiao, id)
                if not meso:
                    return {"mensagem": "Mesorregião não encontrada"}, 404
                return marshal(meso, tb_Mesorregiao_fields), 200
            
            mesorregioes = db.session.query(tb_Mesorregiao).all()
            
            return marshal(mesorregioes, tb_Mesorregiao_fields), 200
        except Exception as e:
            return {"mensagem": f"Erro ao buscar mesorregioes: {str(e)}"}, 500
    
    def put(self, id):
        dados = request.get_json()
        meso = db.session.get(tb_Mesorregiao, id)
        if not meso:
            return {"mensagem": "Mesorregião não encontrada"}, 404
        try:
            meso.mesorregiao = dados.get("mesorregiao", meso.mesorregiao)
            meso.coduf = dados.get("coduf", meso.coduf)
            meso.regiao = dados.get("regiao", meso.regiao)
            db.session.commit()
            return marshal(meso, tb_Mesorregiao_fields), 200
        except Exception as e:
            db.session.rollback()
            return {"mensagem": f"Erro ao atualizar mesorregião: {str(e)}"}, 500
        
    def delete(self, id):
        meso = db.session.get(tb_Mesorregiao, id)
        if not meso:
            return {"mensagem": "Mesorregião não encontrada"}, 404
        try:
            db.session.delete(meso)
            db.session.commit()
            return {"mensagem": "Mesorregião excluída com sucesso"}, 200
        except Exception as e:
            db.session.rollback()
            return {"mensagem": f"Erro ao excluir mesorregião: {str(e)}"}, 500
