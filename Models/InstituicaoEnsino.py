from marshmallow import Schema, fields, validates, ValidationError
from marshmallow.validate import Range, Length
from flask_restful import fields as flaskFields

instituicao_fields = {
    'regiao':   flaskFields.String,
    'codRegiao':   flaskFields.Integer,
    'uf':   flaskFields.String,
    'codUF':   flaskFields.Integer,
    'municipio':   flaskFields.String,
    'codMunicipio':   flaskFields.Integer,
    'entidade':   flaskFields.String,
    'codEntidade':   flaskFields.Integer,
    'matriculas_base':   flaskFields.Integer,
    'ano': flaskFields.Integer
}

class InstituicaoEnsino:
    def __init__(self, regiao, codRegiao, uf, codUF, municipio,
                 codMunicipio, entidade, codEntidade, matriculas_base, ano,  created=None):
        self.regiao = regiao
        self.codRegiao = codRegiao
        self.uf = uf
        self.codUF = codUF
        self.municipio = municipio
        self.codMunicipio = codMunicipio
        self.entidade = entidade
        self.codEntidade = codEntidade
        self.matriculas_base = matriculas_base
        self.ano = ano


class InstituicaoEnsinoSchemas(Schema):
     regiao = fields.String(required=True, validate=Length(min=2, max=20))
     codRegiao = fields.Integer(required=True, validate=Range(min=1))
     uf = fields.String(required=True, validate=Length(equal=2))  
     codUF = fields.Integer(required=True, validate=Range(min=2))
     municipio = fields.String(required=True, validate=Length(min=2, max=150))
     codMunicipio = fields.Integer(required=True, validate=Range(min=7))
     entidade = fields.String(required=True, validate=Length(min=2, max=100))
     codEntidade = fields.Integer(required=True, validate=Range(min=1))
     matriculas_base = fields.Integer(required=True, validate=Range(min=0))
     ano = fields.Integer(required=True, validate=Range(min=0))

class UF:
    def __init__(self, codUF, uf, nomeUF, regiao):
        self.codUF = codUF
        self.uf = uf
        self.nomeUF = nomeUF
        self.regiao = regiao

class UFSchema(Schema):
    codUF = fields.Integer()
    uf = fields.String(required=True, validate=Length(min=2, max=100))
    nomeUF = fields.String(required=True, validate=Length(min=2, max=100))
    regiao = fields.String(required=True, validate=Length(min=2, max=100))

class Municipio:
    def __init__(self, codMunicipio, nomeMunicipio, codUF, regiao, codMesorregiao, codMicrorregiao):
        self.codMunicipio = codMunicipio
        self.nomeMunicipio = nomeMunicipio
        self.codUF = codUF
        self.regiao = regiao
        self.codMesorregiao = codMesorregiao
        self.codMicrorregiao = codMicrorregiao

class MunicipioSchema(Schema):
    codMunicipio = fields.Integer()
    nomeMunicipio = fields.String(required=True, validate=Length(min=2, max=100))
    codUF = fields.Integer()
    regiao = fields.String(required=True, validate=Length(min=2, max=100))
    codMesorregiao = fields.Integer()
    codMicrorregiao = fields.Integer()

class Mesorregiao:
    def __init__(self, codMesorregiao, mesorregiao, codUF, regiao):
        self.codMesorregiao = codMesorregiao
        self.mesorregiao = mesorregiao
        self.codUF = codUF
        self.regiao = regiao

class MesorregiaoSchema(Schema):
    codMesorregiao = fields.Integer()
    mesorregiao = fields.String(required=True, validate=Length(min=2, max=100))
    codUF = fields.Integer()
    regiao = fields.String(required=True, validate=Length(min=2, max=100))

class Microrregiao:
    def __init__(self, codMicrorregiao, microrregiao, codMesorregiao, codUF, regiao):
        self.codMicrorregiao = codMicrorregiao
        self.microrregiao = microrregiao
        self.codMesorregiao = codMesorregiao
        self.codUF = codUF
        self.regiao = regiao

class MicrorregiaoSchema(Schema):
    codMicrorregiao = fields.Integer()
    microrregiao = fields.String(required=True, validate=Length(min=2, max=100))
    codMesorregiao = fields.Integer()
    codUF = fields.Integer()
    regiao = fields.String(required=True, validate=Length(min=2, max=100))