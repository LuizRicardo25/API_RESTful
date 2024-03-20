import pytest
from flask import json, jsonify
# from app import app  # Aqui assumimos que o seu arquivo se chama app.py
from app import app, posts  # Importe a lista posts junto com app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

@pytest.fixture(autouse=True)
def reset_posts():
    global posts
    posts = [
        {'id': 1, 'title': 'Primeiro Post', 'content': 'Este é o conteúdo do primeiro post'},
        {'id': 2, 'title': 'Segundo Post', 'content': 'Este é o conteúdo do segundo post'}
    ]


def test_get_all_posts(client):
    """Teste para verificar se a listagem de todos os posts funciona corretamente."""
    response = client.get('/api/posts')
    assert response.status_code == 200
    assert len(response.json) == 2  # Considerando os 2 posts iniciais

def test_get_single_post(client):
    """Teste para verificar se a recuperação de um post específico pelo ID funciona corretamente."""
    response = client.get('/api/posts/1')
    assert response.status_code == 200
    assert response.json['id'] == 1

def test_post_not_found(client):
    """Teste para verificar o comportamento quando um post não é encontrado."""
    response = client.get('/api/posts/999')
    assert response.status_code == 404

def test_create_post(client):
    """Teste para verificar se a criação de um novo post funciona corretamente."""
    new_post = {'title': 'New Post', 'content': 'Content of new post'}
    response = client.post('/api/posts', data=json.dumps(new_post), content_type='application/json')
    assert response.status_code == 201
    assert response.json['id'] == 3  # Novo ID considerando os posts iniciais

def test_update_post(client):
    """Teste para verificar se a atualização de um post existente pelo seu ID funciona corretamente."""
    updated_post = {'title': 'Updated Title'}
    response = client.put('/api/posts/1', data=json.dumps(updated_post), content_type='application/json')
    assert response.status_code == 200
    assert response.json['title'] == 'Updated Title'

def test_delete_post(client):
    """Teste para verificar se a deleção de um post pelo seu ID funciona corretamente."""
    response = client.delete('/api/posts/1')
    assert response.status_code == 204
    follow_up_response = client.get('/api/posts')
    assert len(follow_up_response.json) == 2  # Verifica se o post foi realmente deletado
