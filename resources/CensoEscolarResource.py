from flask_restful import Resource, marshal
from flask import request
from Models.CensoEscolar import tb_CensoEscolar, tb_CensoEscolar_fields  

class CensoEscolarResource(Resource):
    def get(self):
        ano = request.args.get('ano')
        estado = request.args.get('estado')

        query = tb_CensoEscolar.query

        if ano:
            query = query.filter_by(ano=ano)
        if estado:
            query = query.filter_by(estado=estado)

        resultados = query.all()

        if not resultados:
            return {"mensagem": "Nenhum dado encontrado."}, 404

        return [marshal(r, tb_CensoEscolar_fields) for r in resultados], 200
