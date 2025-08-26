from flask_restful import Resource, marshal
from helpers.database import db
from Models.UF import tb_UF, tb_UF_fields
from flask import request
from sqlalchemy.exc import IntegrityError

class UfsResource(Resource):
    def get(self, coduf=None):
        try:
            if coduf:
                uf = db.session.get(tb_UF, coduf)
                if uf:
                    return marshal(uf, tb_UF_fields), 200
                return {"mensagem": "UF não encontrada."}, 404
            else:
                ufs = db.session.query(tb_UF).all()
                return marshal(ufs, tb_UF_fields), 200
        except Exception as e:
            return {"mensagem": f"Erro ao buscar UFs: {str(e)}"}, 500
        
    def post(self):
        dados = request.get_json()
        coduf = dados.get("coduf")
        if not coduf:
            return {"mensagem": "Campo 'coduf' é obrigatório."}, 400

        if db.session.get(tb_UF, coduf):
            return {"mensagem": "UF com esse código já existe."}, 409

        try:
            nova_uf = tb_UF(
                coduf=coduf,
                uf=dados.get("uf"),
                nome_estado=dados.get("nome_estado"),
                regiao=dados.get("regiao")
            )
            db.session.add(nova_uf)
            db.session.commit()
            return marshal(nova_uf, tb_UF_fields), 201
        except IntegrityError as e:
            db.session.rollback()
            return {"mensagem": f"Erro de integridade: {str(e)}"}, 400
        except Exception as e:
            db.session.rollback()
            return {"mensagem": f"Erro ao criar UF: {str(e)}"}, 500


class UfResource(Resource):
    def get(self, id):
        try:
            uf = db.session.get(tb_UF, id)
            if uf:
                return marshal(uf, tb_UF_fields), 200
            return {"mensagem": "UF não encontrada"}, 404
        except Exception as e:
            return {"mensagem": f"Erro ao buscar UF: {str(e)}"}, 500
     
    def put(self, id):
        uf = db.session.get(tb_UF, id)
        if not uf:
            return {"mensagem": "UF não encontrada."}, 404

        dados = request.get_json()
        uf.uf = dados.get("uf", uf.uf)
        uf.nome_estado = dados.get("nome_estado", uf.nome_estado)
        uf.regiao = dados.get("regiao", uf.regiao)

        try:
            db.session.commit()
            return marshal(uf, tb_UF_fields), 200
        except Exception as e:
            db.session.rollback()
            return {"mensagem": f"Erro ao atualizar UF: {str(e)}"}, 500
     
    def delete(self, id):
        uf = db.session.get(tb_UF, id)
        if not uf:
            return {"mensagem": "UF não encontrada."}, 404

        try:
            db.session.delete(uf)
            db.session.commit()
            return {"mensagem": "UF deletada com sucesso."}, 200
        except Exception as e:
            db.session.rollback()
            return {"mensagem": f"Erro ao deletar UF: {str(e)}"}, 500
