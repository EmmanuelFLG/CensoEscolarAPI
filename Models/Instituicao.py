from __future__ import annotations
from sqlalchemy import Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from helpers.database import db
from flask_restful import fields as flaskFields
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .Municipio import tb_Municipio

tb_instituicao_fields = {
    "regiao": flaskFields.String,
    "codregiao": flaskFields.Integer,
    "uf": flaskFields.String,
    "coduf": flaskFields.Integer,
    "municipio": flaskFields.String,
    "codmunicipio": flaskFields.Integer,
    "entidade": flaskFields.String,
    "codentidade": flaskFields.Integer,
    "matriculas_base": flaskFields.Integer,
    "ano": flaskFields.Integer,
    "created": flaskFields.DateTime(dt_format='iso8601')
}

class tb_instituicao(db.Model):
    __tablename__ = "tb_instituicao"
    
    regiao: Mapped[str] = mapped_column(String)
    codregiao: Mapped[int] = mapped_column('codregiao', Integer) 
    uf: Mapped[str] = mapped_column('uf', String)
    coduf: Mapped[int] = mapped_column('coduf', Integer)
    municipio: Mapped[str] = mapped_column(String)
    codmunicipio: Mapped[int] = mapped_column(ForeignKey('tb_Municipio.idmunicipio'))
    entidade: Mapped[str] = mapped_column(String)
    codentidade: Mapped[int] = mapped_column('codentidade', Integer)
    matriculas_base: Mapped[int] = mapped_column(Integer)
    ano: Mapped[int] = mapped_column(Integer)
    created: Mapped[datetime] = mapped_column(DateTime, server_default=db.func.now())

    municipio_rel: Mapped[tb_Municipio] = relationship(
    "tb_Municipio", 
    back_populates="instituicoes"
)


    __mapper_args__ = {
        "primary_key": [codentidade, ano]
    }

    def __init__(self, regiao: str, codregiao: int, uf: str, coduf: int, 
                 municipio: str, codmunicipio: int, entidade: str, 
                 codentidade: int, matriculas_base: int, ano: int):
        self.regiao = regiao
        self.codregiao = codregiao
        self.uf = uf
        self.coduf = coduf
        self.municipio = municipio
        self.codmunicipio = codmunicipio
        self.entidade = entidade
        self.codentidade = codentidade
        self.matriculas_base = matriculas_base
        self.ano = ano

    def __repr__(self):
        return f"tb_instituicao(cod={self.codentidade}, ano={self.ano}, entidade={self.entidade})"