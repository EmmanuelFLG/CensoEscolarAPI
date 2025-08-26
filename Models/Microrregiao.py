from __future__ import annotations
from sqlalchemy import String, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List, TYPE_CHECKING
from helpers.database import db
from flask_restful import fields as flaskFields

if TYPE_CHECKING:
    from .UF import tb_UF
    from .Mesorregiao import tb_Mesorregiao
    from .Municipio import tb_Municipio

tb_Microrregiao_fields = {
    "codmicrorregiao": flaskFields.Integer,
    "microrregiao": flaskFields.String,
    "codmesorregiao": flaskFields.Integer,
    "coduf": flaskFields.Integer,
    "regiao": flaskFields.String
}

class tb_Microrregiao(db.Model):
    __tablename__ = "tb_Microrregiao"

    codmicrorregiao: Mapped[int] = mapped_column('codmicrorregiao', Integer, primary_key=True, autoincrement=False)
    microrregiao: Mapped[str] = mapped_column('microrregiao', String)
    codmesorregiao: Mapped[int] = mapped_column('codmesorregiao', ForeignKey('tb_Mesorregiao.codmesorregiao'))
    coduf: Mapped[int] = mapped_column('coduf', ForeignKey('tb_UF.coduf'))
    regiao: Mapped[str] = mapped_column('regiao', String)

    
    uf: Mapped[tb_UF] = relationship("tb_UF", back_populates="microrregioes")
    mesorregiao: Mapped[tb_Mesorregiao] = relationship("tb_Mesorregiao", back_populates="microrregioes")
    municipios: Mapped[List[tb_Municipio]] = relationship("tb_Municipio", back_populates="microrregiao")

    def __init__(self, codmicrorregiao: int, microrregiao: str, codmesorregiao: int, coduf: int, regiao: str):
        self.codmicrorregiao = codmicrorregiao
        self.microrregiao = microrregiao
        self.codmesorregiao = codmesorregiao
        self.coduf = coduf
        self.regiao = regiao

    def __repr__(self):
        return f"tb_Microrregiao(cod={self.codmicrorregiao}, nome={self.microrregiao})"