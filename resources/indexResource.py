from flask_restful import Resource

class IndexResource(Resource):
    def get(self):
        versao = {"versao": "0.0.1"}
        return versao, 200