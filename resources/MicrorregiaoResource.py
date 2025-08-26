from flask_restful import Resource, marshal, reqparse
from helpers.database import db
from Models.Microrregiao import tb_Microrregiao, tb_Microrregiao_fields
from flask import request
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

class MicrorregioesResource(Resource):
    def get(self):
        try:
            microrregioes = db.session.query(tb_Microrregiao).all()
            return marshal(microrregioes, tb_Microrregiao_fields), 200
        except Exception as e:
            return {"mensagem": f"Erro ao buscar microrregiões: {str(e)}"}, 500
        
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("codmicrorregiao", required=True)
        parser.add_argument("microrregiao", required=True)
        parser.add_argument("codmesorregiao", required=True)
        parser.add_argument("regiao", required=True)
        parser.add_argument("coduf", required=True)
        dados = parser.parse_args()

        try:
            nova_micro = tb_Microrregiao(
                codmicrorregiao=dados["codmicrorregiao"],
                microrregiao=dados["microrregiao"],
                codmesorregiao=dados["codmesorregiao"],
                regiao=dados["regiao"],
                coduf=dados["coduf"]
            )
            db.session.add(nova_micro)
            db.session.commit()
            return marshal(nova_micro, tb_Microrregiao_fields), 201
        except IntegrityError:
            db.session.rollback()
            return {"mensagem": "Código já existente ou violação de integridade"}, 400
        except Exception as e:
            db.session.rollback()
            return {"mensagem": f"Erro ao criar microrregião: {str(e)}"}, 500

class MicrorregiaoResource(Resource):
    def get(self, id=None):
        try:
            if id is not None:
                micro = db.session.get(tb_Microrregiao, id)
                if not micro:
                    return {"mensagem": "Microrregião não encontrada"}, 404
                return marshal(micro, tb_Microrregiao_fields), 200
            
            microrregioes = db.session.query(tb_Microrregiao).all()
            return marshal(microrregioes, tb_Microrregiao_fields), 200
        except Exception as e:
            return {"mensagem": f"Erro ao buscar microrregiões: {str(e)}"}, 500
    
    def put(self, id):
        dados = request.get_json()
        micro = db.session.get(tb_Microrregiao, id)
        if not micro:
            return {"mensagem": "Microrregião não encontrada"}, 404
        try:
            micro.microrregiao = dados.get("microrregiao", micro.microrregiao)
            micro.codmesorregiao = dados.get("codmesorregiao", micro.codmesorregiao)
            micro.regiao = dados.get("regiao", micro.regiao)
            micro.coduf = dados.get("coduf", micro.coduf)
            db.session.commit()
            return marshal(micro, tb_Microrregiao_fields), 200
        except Exception as e:
            db.session.rollback()
            return {"mensagem": f"Erro ao atualizar microrregião: {str(e)}"}, 500
        
    def delete(self, id):
        micro = db.session.get(tb_Microrregiao, id)
        if not micro:
            return {"mensagem": "Microrregião não encontrada"}, 404
        try:
            db.session.delete(micro)
            db.session.commit()
            return {"mensagem": "Microrregião excluída com sucesso"}, 200
        except Exception as e:
            db.session.rollback()
            return {"mensagem": f"Erro ao excluir microrregião: {str(e)}"}, 500
