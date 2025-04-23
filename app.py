from flask import Flask, json, jsonify

app = Flask(__name__)

CAMINHO_JSON = 'escolas.json'

def carregar_dados():
    with open(CAMINHO_JSON, 'r', encoding='utf-8') as f:
        return json.load(f)

def salvar_dados(dados):
    with open(CAMINHO_JSON, 'w', encoding='utf-8') as f:
        json.dump(dados, f, ensure_ascii=False, indent=4)

@app.route('/instituicoesensino', methods=['GET'])
def listar_instituicoes():
    dados = carregar_dados()
    return jsonify(dados), 200

@app.route('/instituicoesensino/<co_instituicao>', methods=['GET'])
def obter_instituicao(co_instituicao):
    dados = carregar_dados()
    for inst in dados:
        if inst['co_instituicao'] == co_instituicao:
            return jsonify(inst), 200
    return jsonify({'erro': 'Instituição não encontrada'}), 404

@app.route('/instituicoesensino/<co_instituicao>', methods=['DELETE'])
def remover_instituicao(co_instituicao):
    dados = carregar_dados()
    nova_lista = [inst for inst in dados if inst['co_instituicao'] != co_instituicao]

    if len(dados) == len(nova_lista):
        return jsonify({'erro': 'Instituição não encontrada'}), 404

    salvar_dados(nova_lista)
    return jsonify({'mensagem': 'Instituição removida com sucesso'}), 200

if __name__ == '__main__':
    app.run(debug=True)
