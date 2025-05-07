from flask import Flask, jsonify, request
import sqlite3

app = Flask(__name__)

CAMINHO_BANCO = 'censoescolar.db'


def conectar_banco():
    return sqlite3.connect(CAMINHO_BANCO)


def carregar_dados(limit=20, offset=0):
    conn = conectar_banco()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tb_instituicao LIMIT ? OFFSET ?",(limit, offset))
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

@app.route('/instituicoesensino', methods=['GET'])
def listar_instituicoes():  
    dados = carregar_dados()
    return jsonify(dados), 200  
    

@app.route('/instituicoesensino/<co_instituicao>', methods=['GET'])
def obter_instituicao(co_instituicao):
    instituicao = obter_instituicao_db(co_instituicao)
    if instituicao:
        return jsonify(instituicao), 200  
    return jsonify({'erro': 'Instituição não encontrada'}), 404

@app.route('/instituicoesensino/<co_instituicao>', methods=['DELETE'])
def remover_instituicao(co_instituicao):
    instituicao = obter_instituicao_db(co_instituicao)
    if not instituicao:
        return jsonify({'erro': 'Instituição não encontrada'}), 404
    
    remover_instituicao_db(co_instituicao)
    return jsonify({'mensagem': 'Instituição removida com sucesso'}), 200

if __name__ == '__main__':
    app.run(debug=True)
