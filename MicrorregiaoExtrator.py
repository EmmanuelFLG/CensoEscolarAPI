import requests
import sqlite3

def extrair_microrregioes():
    url = 'https://servicodados.ibge.gov.br/api/v1/localidades/microrregioes'
    response = requests.get(url)
    data = response.json()

    conn = sqlite3.connect('censoescolar.db')
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS microrregiao (
            id INTEGER PRIMARY KEY,
            nome TEXT NOT NULL,
            mesorregiao_id INTEGER,
            FOREIGN KEY (mesorregiao_id) REFERENCES mesorregiao(id)
        )
    ''')

    for item in data:
        cursor.execute('INSERT OR IGNORE INTO microrregiao (id, nome, mesorregiao_id) VALUES (?, ?, ?)',
                       (item['id'], item['nome'], item['mesorregiao']['id']))
    
    conn.commit()
    conn.close()

if __name__ == '__main__':
    extrair_microrregioes()
