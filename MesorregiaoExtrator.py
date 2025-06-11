import requests
import sqlite3

def extrair_mesorregioes():
    url = 'https://servicodados.ibge.gov.br/api/v1/localidades/mesorregioes'
    response = requests.get(url)
    data = response.json()

    conn = sqlite3.connect('censoescolar.db')
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS mesorregiao (
            id INTEGER PRIMARY KEY,
            nome TEXT NOT NULL,
            uf_id INTEGER,
            FOREIGN KEY (uf_id) REFERENCES uf(id)
        )
    ''')

    for item in data:
        cursor.execute('INSERT OR IGNORE INTO mesorregiao (id, nome, uf_id) VALUES (?, ?, ?)',
                       (item['id'], item['nome'], item['UF']['id']))
    
    conn.commit()
    conn.close()

if __name__ == '__main__':
    extrair_mesorregioes()
