import requests
import sqlite3

def extrair_municipios():
    url = 'https://servicodados.ibge.gov.br/api/v1/localidades/municipios'
    response = requests.get(url)
    data = response.json()

    conn = sqlite3.connect('censoescolar.db')
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS municipio (
            id INTEGER PRIMARY KEY,
            nome TEXT NOT NULL,
            uf_id INTEGER,
            FOREIGN KEY (uf_id) REFERENCES uf(id)
        )
    ''')

    for m in data:
        cursor.execute('INSERT OR IGNORE INTO municipio (id, nome, uf_id) VALUES (?, ?, ?)', 
                       (m['id'], m['nome'], m['microrregiao']['mesorregiao']['UF']['id']))
    
    conn.commit()
    conn.close()

if __name__ == '__main__':
    extrair_municipios()
