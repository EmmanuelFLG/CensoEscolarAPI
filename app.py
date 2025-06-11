from flask import Flask, jsonify, request, request
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
    try:
        page = int(request.args.get('page', 1))
        limit = int(request.args.get('limit', 10))
    except ValueError:
        return jsonify({'erro': 'Parâmetros page e limit devem ser inteiros'}), 400

    if page < 1 or limit < 1:
        return jsonify({'erro': 'Parâmetros page e limit devem ser maiores que 0'}), 400

    offset = (page - 1) * limit

    conn = conectar_banco()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM tb_instituicao")
    total = cursor.fetchone()[0]

    cursor.execute("SELECT * FROM tb_instituicao LIMIT ? OFFSET ?", (limit, offset))
    dados = cursor.fetchall()
    conn.close()

    instituicoes = [formatar_instituicao(row) for row in dados]

    response = {
        'page': page,
        'limit': limit,
        'total': total,
        'instituicoes': instituicoes,
        'next_page': page + 1 if offset + limit < total else None,
        'prev_page': page - 1 if page > 1 else None
    }

    return jsonify(response), 200

    dados = carregar_dados()
    instituicoes = [formatar_instituicao(row) for row in dados]
    return jsonify(instituicoes), 200

@app.route('/instituicoesensino/<co_instituicao>', methods=['GET'])
def obter_instituicao(co_instituicao):
    instituicao = obter_instituicao_db(co_instituicao)
    if instituicao:
        instituicao_dict = formatar_instituicao(instituicao)
        return jsonify(instituicao_dict), 200
        return jsonify(formatar_instituicao(instituicao)), 200
    return jsonify({'erro': 'Instituição não encontrada'}), 404


@app.route('/instituicoesensino/<co_instituicao>', methods=['DELETE'])
def remover_instituicao(co_instituicao):
    if not obter_instituicao_db(co_instituicao):
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


@app.route('/instituicoesensino', methods=['POST'])
def criar_instituicao():
    dados = request.get_json()

    campos = [
        'no_entidade', 'co_entidade', 'qt_mat_bas', 'co_uf', 'sg_uf',
        'co_municipio', 'municipio', 'co_mesorregiao', 'mesorregiao',
        'co_microrregiao', 'microrregiao'
    ]

    for campo in campos:
        if campo not in dados:
            return jsonify({'erro': f'Dado faltando: {campo}'}), 400

    conn = conectar_banco()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO tb_instituicao (
            no_entidade, co_entidade, qt_mat_bas, co_uf, sg_uf,
            co_municipio, municipio, co_mesorregiao, mesorregiao,
            co_microrregiao, microrregiao
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        dados['no_entidade'], dados['co_entidade'], dados['qt_mat_bas'],
        dados['co_uf'], dados['sg_uf'], dados['co_municipio'], dados['municipio'],
        dados['co_mesorregiao'], dados['mesorregiao'], dados['co_microrregiao'],
        dados['microrregiao']
    ))

    conn.commit()
    id_novo = cursor.lastrowid
    cursor.execute("SELECT * FROM tb_instituicao WHERE id = ?", (id_novo,))
    nova_instituicao = cursor.fetchone()
    conn.close()

    return jsonify(formatar_instituicao(nova_instituicao)), 201


@app.route('/instituicoesensino/<co_instituicao>', methods=['PUT'])
def atualizar_instituicao(co_instituicao):
    dados = request.get_json()

    campos_permitidos = ['no_entidade', 'municipio', 'mesorregiao', 'microrregiao', 'qt_mat_bas']
    campos_para_atualizar = []
    valores = []

    for campo in campos_permitidos:
        if campo in dados:
            campos_para_atualizar.append(f"{campo} = ?")
            valores.append(dados[campo])

    if not campos_para_atualizar:
        return jsonify({'erro': 'Nenhum dado a ser atualizado'}), 400

    valores.append(co_instituicao)
    query = f"UPDATE tb_instituicao SET {', '.join(campos_para_atualizar)} WHERE co_entidade = ?"

    conn = conectar_banco()
    cursor = conn.cursor()
    cursor.execute(query, valores)
    conn.commit()

    cursor.execute("SELECT * FROM tb_instituicao WHERE co_entidade = ?", (co_instituicao,))
    atualizada = cursor.fetchone()
    conn.close()

    if atualizada:
        return jsonify(formatar_instituicao(atualizada)), 200
    return jsonify({'erro': 'Instituição não encontrada'}), 404


if __name__ == '__main__':
    app.run(debug=True)
