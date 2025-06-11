import requests
import sqlite3

def extrair_ufs():
    url = 'https://servicodados.ibge.gov.br/api/v1/localidades/estados'
    response = requests.get(url)
    data = response.json()

    conn = sqlite3.connect('censoescolar.db')
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS uf (
            id INTEGER PRIMARY KEY,
            nome TEXT NOT NULL,
            sigla TEXT NOT NULL
        )
    ''')

    for uf in data:
        cursor.execute('INSERT OR IGNORE INTO uf (id, nome, sigla) VALUES (?, ?, ?)', 
                       (uf['id'], uf['nome'], uf['sigla']))
    
    conn.commit()
    conn.close()

if __name__ == '__main__':
    extrair_ufs()
