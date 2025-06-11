from marshmallow import Schema, fields, validates, ValidationError

class InstituicaoSchema(Schema):
    co_entidade = fields.Str(required=True)
    no_entidade = fields.Str(required=True)
    co_uf = fields.Int(required=True)
    sg_uf = fields.Str(required=True)
    co_municipio = fields.Int(required=True)
    municipio = fields.Str(required=True)
    co_mesorregiao = fields.Int(required=True)
    mesorregiao = fields.Str(required=True)
    co_microrregiao = fields.Int(required=True)
    microrregiao = fields.Str(required=True)
    qt_mat_bas = fields.Int(required=True)
