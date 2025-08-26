from __future__ import annotations
from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List, TYPE_CHECKING
from helpers.database import db
from flask_restful import fields as flaskFields

if TYPE_CHECKING:
    from .UF import tb_UF
    from .Mesorregiao import tb_Mesorregiao
    from .Microrregiao import tb_Microrregiao
    from .Instituicao import tb_instituicao

tb_Municipio_fields = {
    "idmunicipio": flaskFields.Integer,
    "nome_municipio": flaskFields.String,
    "coduf": flaskFields.Integer,
    "regiao": flaskFields.String,
    "codmesorregiao": flaskFields.Integer,
    "codmicrorregiao": flaskFields.Integer
}

class tb_Municipio(db.Model):
    __tablename__ = "tb_Municipio"

    idmunicipio: Mapped[int] = mapped_column('idmunicipio', Integer, primary_key=True)
    nome_municipio: Mapped[str] = mapped_column('nomemunicipio', String)
    coduf: Mapped[int] = mapped_column('coduf', ForeignKey('tb_UF.coduf'))
    regiao: Mapped[str] = mapped_column('regiao', String)
    codmesorregiao: Mapped[int] = mapped_column('codmesorregiao', ForeignKey('tb_Mesorregiao.codmesorregiao'))
    codmicrorregiao: Mapped[int] = mapped_column('codmicrorregiao', ForeignKey('tb_Microrregiao.codmicrorregiao'))

    
    uf: Mapped[tb_UF] = relationship("tb_UF", back_populates="municipios")
    mesorregiao: Mapped[tb_Mesorregiao] = relationship("tb_Mesorregiao", back_populates="municipios")
    microrregiao: Mapped[tb_Microrregiao] = relationship("tb_Microrregiao", back_populates="municipios")
    instituicoes: Mapped[List[tb_instituicao]] = relationship(
    "tb_instituicao", 
    back_populates="municipio_rel",
    primaryjoin="tb_Municipio.idmunicipio == tb_instituicao.codmunicipio"
    )

    def __init__(self, idmunicipio: int, nome_municipio: str, coduf: int, 
                 regiao: str, codmesorregiao: int, codmicrorregiao: int):
        self.idmunicipio = idmunicipio
        self.nome_municipio = nome_municipio
        self.coduf = coduf
        self.regiao = regiao
        self.codmesorregiao = codmesorregiao
        self.codmicrorregiao = codmicrorregiao

    def __repr__(self):
        return f"tb_Municipio(id={self.idmunicipio}, nome={self.nome_municipio})"