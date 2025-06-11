from flask import Flask, jsonify, request
from marshmallow import ValidationError
import sqlite3
from schemas import InstituicaoSchema

app = Flask(__name__)

CAMINHO_BANCO = 'censoescolar.db'

def conectar_banco():
    return sqlite3.connect(CAMINHO_BANCO)

def carregar_dados():
    conn = conectar_banco()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tb_instituicao")
    dados = cursor.fetchall()
    conn.close()
    return dados

def obter_instituicao_db(co_instituicao):
    conn = conectar_banco()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tb_instituicao WHERE co_entidade = ?", (co_instituicao,))
    instituicao = cursor.fetchone()
    conn.close()
    return instituicao

def remover_instituicao_db(co_instituicao):
    conn = conectar_banco()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tb_instituicao WHERE co_entidade = ?", (co_instituicao,))
    conn.commit()
    conn.close()

def formatar_instituicao(row):
    return {
        'id': row[0],
        'co_entidade': row[1],
        'no_entidade': row[2],
        'co_uf': row[3],
        'sg_uf': row[4],
        'co_municipio': row[5],
        'municipio': row[6],
        'co_mesorregiao': row[7],
        'mesorregiao': row[8],
        'co_microrregiao': row[9],
        'microrregiao': row[10],
        'qt_mat_bas': row[11],
        'created': row[12]
    }

@app.route('/instituicoesensino', methods=['GET'])
def listar_instituicoes():
    dados = carregar_dados()
    instituicoes = [formatar_instituicao(row) for row in dados]
    return jsonify(instituicoes), 200

@app.route('/instituicoesensino/<co_instituicao>', methods=['GET'])
def obter_instituicao(co_instituicao):
    instituicao = obter_instituicao_db(co_instituicao)
    if instituicao:
        instituicao_dict = formatar_instituicao(instituicao)
        return jsonify(instituicao_dict), 200
    return jsonify({'erro': 'Instituição não encontrada'}), 404

@app.route('/instituicoesensino/<co_instituicao>', methods=['DELETE'])
def remover_instituicao(co_instituicao):
    instituicao = obter_instituicao_db(co_instituicao)
    if not instituicao:
        return jsonify({'erro': 'Instituição não encontrada'}), 404
    remover_instituicao_db(co_instituicao)
    return jsonify({'mensagem': 'Instituição removida com sucesso'}), 200

@app.route('/instituicoesensino', methods=['POST'])
def criar_instituicao():
    schema = InstituicaoSchema()
    try:
        instituicao_json = schema.load(request.get_json())
    except ValidationError as err:
        return jsonify({'erros': err.messages}), 400

    conn = conectar_banco()
    cursor = conn.cursor()
    cursor.execute('''INSERT INTO tb_instituicao (
                        no_entidade, co_entidade, qt_mat_bas, co_uf, sg_uf,
                        co_municipio, municipio, co_mesorregiao, mesorregiao,
                        co_microrregiao, microrregiao
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', 
                   (instituicao_json['no_entidade'], instituicao_json['co_entidade'], instituicao_json['qt_mat_bas'],
                    instituicao_json['co_uf'], instituicao_json['sg_uf'], instituicao_json['co_municipio'],
                    instituicao_json['municipio'], instituicao_json['co_mesorregiao'], instituicao_json['mesorregiao'],
                    instituicao_json['co_microrregiao'], instituicao_json['microrregiao']))
    conn.commit()
    id = cursor.lastrowid
    cursor.execute("SELECT * FROM tb_instituicao WHERE id = ?", (id,))
    instituicao = cursor.fetchone()
    conn.close()

    instituicao_dict = formatar_instituicao(instituicao)
    return jsonify(instituicao_dict), 201

@app.route('/instituicoesensino/<co_instituicao>', methods=['PUT'])
def atualizar_instituicao(co_instituicao):
    dados = request.get_json()
    update_fields = ['no_entidade', 'municipio', 'mesorregiao', 'microrregiao', 'qt_mat_bas']
    if not any(field in dados for field in update_fields):
        return jsonify({'erro': 'Nenhum dado a ser atualizado'}), 400

    fields_to_update = []
    values = []
    for field in update_fields:
        if field in dados:
            fields_to_update.append(f"{field} = ?")
            values.append(dados[field])
    values.append(co_instituicao)

    query = f'''UPDATE tb_instituicao SET {", ".join(fields_to_update)} WHERE co_entidade = ?'''
    conn = conectar_banco()
    cursor = conn.cursor()
    cursor.execute(query, tuple(values))
    conn.commit()

    cursor.execute("SELECT * FROM tb_instituicao WHERE co_entidade = ?", (co_instituicao,))
    instituicao_atualizada = cursor.fetchone()
    conn.close()

    if instituicao_atualizada:
        return jsonify(formatar_instituicao(instituicao_atualizada)), 200
    return jsonify({'erro': 'Instituição não encontrada'}), 404

if __name__ == '__main__':
    app.run(debug=True)
