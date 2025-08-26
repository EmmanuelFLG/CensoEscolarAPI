from __future__ import annotations
from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List, TYPE_CHECKING
from helpers.database import db
from flask_restful import fields as flaskFields

if TYPE_CHECKING:
    from .UF import tb_UF
    from .Microrregiao import tb_Microrregiao
    from .Municipio import tb_Municipio

tb_Mesorregiao_fields = {
    "codmesorregiao": flaskFields.Integer,
    "mesorregiao": flaskFields.String,
    "coduf": flaskFields.Integer,
    "regiao": flaskFields.String
}

class tb_Mesorregiao(db.Model):
    __tablename__ = "tb_Mesorregiao"

    codmesorregiao: Mapped[int] = mapped_column('codmesorregiao', Integer, primary_key=True)
    mesorregiao: Mapped[str] = mapped_column('mesorregiao', String)
    coduf: Mapped[int] = mapped_column('coduf', ForeignKey('tb_UF.coduf'))
    regiao: Mapped[str] = mapped_column('regiao', String)

   
    uf: Mapped[tb_UF] = relationship("tb_UF", back_populates="mesorregioes")
    
    microrregioes: Mapped[List[tb_Microrregiao]] = relationship(
        "tb_Microrregiao",
        back_populates="mesorregiao",
        cascade="all, delete-orphan"
    )
    
    municipios: Mapped[List[tb_Municipio]] = relationship(
        "tb_Municipio",
        back_populates="mesorregiao",
        cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"tb_Mesorregiao(cod={self.codmesorregiao}, nome={self.mesorregiao})"
    
    