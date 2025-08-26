from helpers.application import app, api
from helpers.CORS import cors

from resources.indexResource import IndexResource
from resources.InstituicoesResource import InstituicoesResource, InstituicaoResource
from resources.MesorregiaoResource import MesorregioesResource, MesorregiaoResource
from resources.MicrorregiaoResource import MicrorregioesResource, MicrorregiaoResource
from resources.UfResource import UfsResource, UfResource
from resources.MunicipioResource import MunicipiosResource, MunicipioResource


import routes

cors.init_app(app)


api.add_resource(IndexResource, '/')
api.add_resource(InstituicoesResource, '/instituicoes')
api.add_resource(InstituicaoResource, '/instituicoes/<int:codentidade>/<int:ano>')
api.add_resource(MesorregioesResource, '/mesorregioes')
api.add_resource(MesorregiaoResource, '/mesorregioes/<int:id>')
api.add_resource(MicrorregioesResource, '/microrregioes')
api.add_resource(MicrorregiaoResource, '/microrregioes/<int:id>')
api.add_resource(UfsResource, '/ufs')
api.add_resource(UfResource, '/ufs/<int:id>')
api.add_resource(MunicipiosResource, '/municipios')
api.add_resource(MunicipioResource, '/municipios/<int:id>')

routes.register_routes(app)

if __name__ == '__main__':
    app.run(debug=True)
