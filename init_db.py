import json
import csv
from helpers.database import db
from Models import tb_UF, tb_Mesorregiao, tb_Microrregiao, tb_Municipio, tb_instituicao
from sqlalchemy.exc import SQLAlchemyError

ARQUIVO_UF = "estados.json"
ARQUIVO_MESORREGIOES = "mesorregioes.json"
ARQUIVO_MICRORREGIOES = "microrregioes.json"
ARQUIVO_MUNICIPIOS = "municipios.json"
ARQUIVOS_CSV = ["censo_escolar2023.csv", "censo_escolar2024.csv"]

def limpar_chave(chave: str) -> str:
    return chave.strip().lower()

def popular_ufs():
    with open(ARQUIVO_UF, "r", encoding="utf-8") as f:
        dados = json.load(f)
    for uf_item in dados:
        uf_obj = tb_UF(
            coduf=int(uf_item["codUF"]),
            uf=uf_item["UF"].strip(),
            nomeestado=uf_item["nomeEstado"].strip(),
            regiao=uf_item["região"].strip()
        )
        existente = tb_UF.query.get(uf_obj.coduf)
        if existente:
            existente.uf = uf_obj.uf
            existente.nomeestado = uf_obj.nomeestado
            existente.regiao = uf_obj.regiao
        else:
            db.session.add(uf_obj)

def popular_mesorregioes():
    with open(ARQUIVO_MESORREGIOES, "r", encoding="utf-8") as f:
        dados = json.load(f)
    for item in dados:
        meso_obj = tb_Mesorregiao(
            codmesorregiao=int(item["codMesorregiao"]),
            mesorregiao=item["mesorregiao"].strip(),
            coduf=int(item["codUF"]),
            regiao=item["regiao"].strip()
        )
        existente = tb_Mesorregiao.query.get(meso_obj.codmesorregiao)
        if existente:
            existente.mesorregiao = meso_obj.mesorregiao
            existente.coduf = meso_obj.coduf
            existente.regiao = meso_obj.regiao
        else:
            db.session.add(meso_obj)

def popular_microrregioes():
    with open(ARQUIVO_MICRORREGIOES, "r", encoding="utf-8") as f:
        dados = json.load(f)
    for item in dados:
        micro_obj = tb_Microrregiao(
            codmicrorregiao=int(item["codMicrorregiao"]),
            microrregiao=item["microrregiao"].strip(),
            codmesorregiao=int(item["codMesorregiao"]),
            coduf=int(item["codUF"]),
            regiao=item["regiao"].strip()
        )
        existente = tb_Microrregiao.query.get(micro_obj.codmicrorregiao)
        if existente:
            existente.microrregiao = micro_obj.microrregiao
            existente.codmesorregiao = micro_obj.codmesorregiao
            existente.coduf = micro_obj.coduf
            existente.regiao = micro_obj.regiao
        else:
            db.session.add(micro_obj)

def popular_municipios():
    with open(ARQUIVO_MUNICIPIOS, "r", encoding="utf-8") as f:
        dados = json.load(f)
    for item in dados:
        municipio_obj = tb_Municipio(
            idmunicipio=int(item["idMunicipio"]),
            nomemunicipio=item["nomeMunicipio"].strip(),
            coduf=int(item["codUF"]),
            regiao=item["regiao"].strip(),
            codmesorregiao=int(item["codMesorregiao"]),
            codmicrorregiao=int(item["codMicrorregiao"])
        )
        existente = tb_Municipio.query.get(municipio_obj.idmunicipio)
        if existente:
            existente.nomemunicipio = municipio_obj.nomemunicipio
            existente.coduf = municipio_obj.coduf
            existente.regiao = municipio_obj.regiao
            existente.codmesorregiao = municipio_obj.codmesorregiao
            existente.codmicrorregiao = municipio_obj.codmicrorregiao
        else:
            db.session.add(municipio_obj)

def popular_instituicoes():
    for arquivo_csv in ARQUIVOS_CSV:
        print(f"Processando {arquivo_csv}...")
        with open(arquivo_csv, "r", encoding="utf-8-sig") as f:
            leitor = csv.DictReader(f, delimiter=';')
            mapa_chaves = {limpar_chave(k): k for k in leitor.fieldnames}
            for linha in leitor:
                try:
                    def valor(campo_normalizado):
                        chave_original = mapa_chaves.get(campo_normalizado)
                        if not chave_original:
                            raise KeyError(f"Campo '{campo_normalizado}' não encontrado")
                        return linha[chave_original].strip()
                    codentidade = int(float(valor("codentidade")))
                    entidade = valor("entidade")
                    codregiao = int(float(valor("codregiao")))
                    regiao = valor("regiao")
                    coduf = int(float(valor("coduf")))
                    uf = valor("uf")
                    codmunicipio = int(float(valor("codmunicipio")))
                    municipio = valor("municipio")
                    matriculas_str = valor("matriculas_base").replace('.', '')
                    matriculas = int(matriculas_str) if matriculas_str else 0
                    ano = int(float(valor("ano")))
                    existente = tb_instituicao.query.filter_by(codentidade=codentidade, ano=ano).first()
                    if existente:
                        existente.entidade = entidade
                        existente.codregiao = codregiao
                        existente.regiao = regiao
                        existente.coduf = coduf
                        existente.uf = uf
                        existente.codmunicipio = codmunicipio
                        existente.municipio = municipio
                        existente.matriculas_base = matriculas
                    else:
                        instituicao_obj = tb_instituicao(
                            codentidade=codentidade,
                            entidade=entidade,
                            codregiao=codregiao,
                            regiao=regiao,
                            coduf=coduf,
                            uf=uf,
                            codmunicipio=codmunicipio,
                            municipio=municipio,
                            matriculas_base=matriculas,
                            ano=ano
                        )
                        db.session.add(instituicao_obj)
                except Exception as e:
                    print(f"Erro ao processar linha {linha.get('codentidade', 'desconhecido')}: {e}")
                    db.session.rollback()

def inicializar_banco():
    try:
        popular_ufs()
        popular_mesorregioes()
        popular_microrregioes()
        popular_municipios()
        popular_instituicoes()
        db.session.commit()
        print("Dados inseridos com sucesso!")
    except SQLAlchemyError as e:
        db.session.rollback()
        print(f"Erro no banco de dados: {e}")

if __name__ == "__main__":
    inicializar_banco()
