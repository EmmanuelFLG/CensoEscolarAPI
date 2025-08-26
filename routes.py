from flask import jsonify, request
from helpers.database import db
from Models.Instituicao import tb_instituicao
from Models.UF import tb_UF
from sqlalchemy import func
from helpers.logging import logger

def register_routes(app):
    @app.route('/censoescolar', methods=['GET'])
    def get_censo_escolar():
        ano = request.args.get('ano', type=int)
        estado = request.args.get('estado', type=str)

        try:
            query = db.session.query(
                tb_UF.nome_estado.label('estado'),
                tb_instituicao.ano,
                func.sum(tb_instituicao.matriculas_base).label('total_matriculas')
            ).join(tb_UF, tb_instituicao.coduf == tb_UF.coduf)

            if ano:
                query = query.filter(tb_instituicao.ano == ano)
            if estado and estado.lower() != 'todos':
                query = query.filter(tb_UF.nome_estado == estado)

            query = query.group_by(tb_UF.nome_estado, tb_instituicao.ano).order_by(tb_UF.nome_estado)

            resultados = query.all()

        
            dados = [
                {
                    "estado": res.estado,
                    "ano": res.ano,
                    "total_matriculas": int(res.total_matriculas)
                }
                for res in resultados
            ]

            return jsonify(dados)
        
        except Exception as e:
            logger.error(f"Erro ao buscar dados do censo escolar: {e}")
            return jsonify({"erro": "Erro ao buscar dados do censo escolar"}), 500
