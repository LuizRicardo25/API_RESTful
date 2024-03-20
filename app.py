# Importa as funções necessárias do módulo flask
from flask import Flask, jsonify, request

# Cria uma instância do aplicativo Flask
app = Flask(__name__)

# Uma lista de dicionários que simula um banco de dados em memória para armazenar posts
posts = [
    {'id': 1, 'title': 'Primeiro Post', 'content': 'Este é o conteúdo do primeiro post'},
    {'id': 2, 'title': 'Segundo Post', 'content': 'Este é o conteúdo do segundo post'}
]

# Define um endpoint GET para '/api/posts' que retorna a lista de todos os posts
@app.route('/api/posts', methods=['GET'])
def get_posts():
    # Converte a lista de posts para JSON e retorna com o status HTTP 200 (OK)
    return jsonify(posts), 200

# Define um endpoint GET para '/api/posts/<int:post_id>' que retorna um post específico pelo seu ID
@app.route('/api/posts/<int:post_id>', methods=['GET'])
def get_post(post_id):
    # Procura na lista de posts o post com o ID fornecido, retorna None se não for encontrado
    post = next((post for post in posts if post['id'] == post_id), None)
    # Se um post for encontrado, retorna o post como JSON com status HTTP 200 (OK)
    if post is not None:
        return jsonify(post), 200
    # Se não, retorna uma mensagem de erro como JSON com status HTTP 404 (Not Found)
    else:
        return jsonify({'message': 'Post not found'}), 404

# Define um endpoint POST para '/api/posts' que cria um novo post
@app.route('/api/posts', methods=['POST'])
def create_post():
    # Obtém os dados JSON enviados com a requisição POST
    new_post = request.get_json()
    # Atribui um novo ID ao post, que é um mais que o número de posts existentes
    new_post['id'] = len(posts) + 1
    # Adiciona o novo post à lista de posts
    posts.append(new_post)
    # Retorna o novo post como JSON com status HTTP 201 (Created)
    return jsonify(new_post), 201

# Define um endpoint PUT para '/api/posts/<int:post_id>' que atualiza um post existente pelo seu ID
@app.route('/api/posts/<int:post_id>', methods=['PUT'])
def update_post(post_id):
    # Procura na lista de posts o post com o ID fornecido, retorna None se não for encontrado
    post = next((post for post in posts if post['id'] == post_id), None)
    # Se um post for encontrado, atualiza-o com os dados enviados
    if post is not None:
        data = request.get_json()
        post.update(data)
        # Retorna o post atualizado como JSON com status HTTP 200 (OK)
        return jsonify(post), 200
    # Se não, retorna uma mensagem de erro como JSON com status HTTP 404 (Not Found)
    else:
        return jsonify({'message': 'Post not found'}), 404
'''
# Define um endpoint DELETE para '/api/posts/<int:post_id>' que deleta um post específico pelo seu ID
@app.route('/api/posts/<int:post_id>', methods=['DELETE'])
def delete_post(post_id):
    # A palavra-chave 'global' é usada para modificar a variável global 'posts'
    global posts
    # Cria uma nova lista de posts que não inclui o post com o ID fornecido
    posts = [post for post in posts if post['id'] != post_id]
    # Retorna uma mensagem de sucesso como JSON com status HTTP 204 (No Content)
    return jsonify({'message': 'Post deleted'}), 204
'''

@app.route('/api/posts/<int:post_id>', methods=['DELETE'])
def delete_post(post_id):
    global posts  # Garante que estamos modificando a variável global
    post = next((post for post in posts if post['id'] == post_id), None)
    if post:
        posts = [post for post in posts if post['id'] != post_id]  # Filtra fora o post deletado
        return jsonify({'message': 'Post deleted'}), 204
    else:
        return jsonify({'error': 'Post not found'}), 404


# Verifica se o arquivo é o módulo principal e executa o aplicativo Flask
if __name__ == '__main__':
    # Inicia o aplicativo Flask em modo de depuração
    app.run(debug=True)


