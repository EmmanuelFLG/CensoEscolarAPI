import pandas as pd


caminho_csv_origem = "C:\\Users\\manin\\Downloads\\microdados_censo_escolar_2023\\microdados_censo_escolar_2023\\dados\\microdados_ed_basica_2023.csv"
caminho_csv_saida = "censoescolar.csv"


colunas_selecionadas = [
    "CO_ENTIDADE", "NO_ENTIDADE", "CO_UF", "SG_UF", 
    "CO_MUNICIPIO", "NO_MUNICIPIO", "CO_MESORREGIAO", 
    "NO_MESORREGIAO", "CO_MICRORREGIAO", "NO_MICRORREGIAO", 
    "QT_MAT_BAS"
]

dados_escola = pd.read_csv(caminho_csv_origem, usecols=colunas_selecionadas, delimiter=';', encoding='iso-8859-1', dtype=str)


uf_nordeste = ["AL", "BA", "CE", "MA", "PB", "PE", "PI", "RN", "SE"]
dados_escola_nordeste = dados_escola[dados_escola["SG_UF"].isin(uf_nordeste)]


dados_escola_nordeste.to_csv(caminho_csv_saida, index=False, encoding='utf-8-sig')

print(f"Arquivo CSV salvo como {caminho_csv_saida}")
