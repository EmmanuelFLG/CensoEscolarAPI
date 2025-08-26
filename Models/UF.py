from __future__ import annotations
from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List, TYPE_CHECKING
from helpers.database import db
from flask_restful import fields as flaskFields

if TYPE_CHECKING:
    from .Mesorregiao import tb_Mesorregiao
    from .Microrregiao import tb_Microrregiao
    from .Municipio import tb_Municipio

tb_UF_fields = {
    "coduf": flaskFields.Integer,
    "uf": flaskFields.String,
    "nome_estado": flaskFields.String,
    "regiao": flaskFields.String
}

class tb_UF(db.Model):
    __tablename__ = "tb_UF"

    coduf: Mapped[int] = mapped_column('coduf', Integer, primary_key=True)
    uf: Mapped[str] = mapped_column('uf', String)
    nome_estado: Mapped[str] = mapped_column('nomeestado', String)
    regiao: Mapped[str] = mapped_column('regiao', String)

    
    mesorregioes: Mapped[List[tb_Mesorregiao]] = relationship(
        "tb_Mesorregiao", 
        back_populates="uf",
        cascade="all, delete-orphan"
    )
    
    microrregioes: Mapped[List[tb_Microrregiao]] = relationship(
        "tb_Microrregiao",
        back_populates="uf",
        cascade="all, delete-orphan"
    )
    
    municipios: Mapped[List[tb_Municipio]] = relationship(
        "tb_Municipio",
        back_populates="uf",
        cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"tb_UF(cod={self.coduf}, nome={self.nomeestado})"