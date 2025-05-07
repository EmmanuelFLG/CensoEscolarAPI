import sqlite3
import pandas as pd


caminho_banco = 'censoescolar.db'
caminho_csv = 'censoescolar.csv'
caminho_schema = 'schemas.sql'


connection = sqlite3.connect(caminho_banco)
cursor = connection.cursor()


with open(caminho_schema, 'r') as schema_file:
    cursor.executescript(schema_file.read())


dados_escola = pd.read_csv(caminho_csv, encoding='utf-8-sig')


dados_escola.columns = dados_escola.columns.str.strip()


for _, row in dados_escola.iterrows():
   
    qt_mat_bas = row['QT_MAT_BAS'] if pd.notna(row['QT_MAT_BAS']) else 0  
    cursor.execute("""
    INSERT INTO tb_instituicao (
        "CO_ENTIDADE", "NO_ENTIDADE", "CO_UF", "SG_UF",
        "CO_MUNICIPIO", "NO_MUNICIPIO", "CO_MESORREGIAO", "NO_MESORREGIAO",
        "CO_MICRORREGIAO", "NO_MICRORREGIAO", "QT_MAT_BAS"
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        row['CO_ENTIDADE'], row['NO_ENTIDADE'], row['CO_UF'], row['SG_UF'],
        row['CO_MUNICIPIO'], row['NO_MUNICIPIO'], row['CO_MESORREGIAO'], row['NO_MESORREGIAO'],
        row['CO_MICRORREGIAO'], row['NO_MICRORREGIAO'], int(qt_mat_bas)  
    ))


connection.commit()


connection.close()

print("Dados inseridos com sucesso no banco de dados.")
