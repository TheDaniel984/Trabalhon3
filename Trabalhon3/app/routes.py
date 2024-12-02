from flask import Blueprint, jsonify, request
from .models import Pedido, Usuario, Produto, db  # Importação unificada

# Blueprint para usuários
bp = Blueprint('usuarios', __name__, url_prefix='/usuarios')

# Rota: Listar todos os usuários (GET /usuarios)
@bp.route('/', methods=['GET'])
def listar_usuarios():
    usuarios = Usuario.query.all()
    usuarios_json = [{"id": u.id, "nome": u.nome, "email": u.email} for u in usuarios]
    return jsonify(usuarios_json)

# Rota: Criar um novo usuário (POST /usuarios)
@bp.route('/', methods=['POST'])
def criar_usuario():
    dados = request.get_json()
    novo_usuario = Usuario(nome=dados['nome'], email=dados['email'])
    db.session.add(novo_usuario)
    db.session.commit()
    return jsonify({"message": "Usuário criado com sucesso!"}), 201

# Rota: Atualizar um usuário específico (PUT /usuarios/<id>)
@bp.route('/<int:id>', methods=['PUT'])
def atualizar_usuario(id):
    usuario = Usuario.query.get(id)
    if not usuario:
        return jsonify({"error": "Usuário não encontrado"}), 404
    
    dados = request.get_json()
    usuario.nome = dados.get('nome', usuario.nome)
    usuario.email = dados.get('email', usuario.email)

    db.session.commit()
    return jsonify({"message": "Usuário atualizado com sucesso!"})

# Rota: Excluir um usuário específico (DELETE /usuarios/<id>)
@bp.route('/<int:id>', methods=['DELETE'])
def excluir_usuario(id):
    usuario = Usuario.query.get(id)
    if not usuario:
        return jsonify({"error": "Usuário não encontrado"}), 404

    db.session.delete(usuario)
    db.session.commit()
    return jsonify({"message": "Usuário excluído com sucesso!"})

# Blueprint para produtos
bp_produtos = Blueprint('produtos', __name__, url_prefix='/produtos')

# Rota: Listar todos os produtos (GET /produtos)
@bp_produtos.route('/', methods=['GET'])
def listar_produtos():
    produtos = Produto.query.all()
    produtos_json = [{"id": p.id, "nome": p.nome, "preco": p.preco, "estoque": p.estoque} for p in produtos]
    return jsonify(produtos_json)

# Rota: Criar um novo produto (POST /produtos)
@bp_produtos.route('/', methods=['POST'])
def criar_produto():
    dados = request.get_json()
    if not dados:
        return jsonify({"error": "Dados ausentes na requisição"}), 400
    
    novo_produto = Produto(nome=dados['nome'], preco=dados['preco'], estoque=dados['estoque'])
    db.session.add(novo_produto)

    try:
        db.session.commit()
        return jsonify({"message": "Produto criado com sucesso!"}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Erro ao salvar o produto: {str(e)}"}), 500

# Rota: Excluir um produto específico (DELETE /produtos/<id>)
@bp_produtos.route('/<int:id>', methods=['DELETE'])
def excluir_produto(id):
    produto = Produto.query.get(id)  # Busca o produto pelo ID no banco de dados
    if not produto:
        return jsonify({"error": "Produto não encontrado"}), 404  # Retorna erro 404 se não encontrar

    try:
        db.session.delete(produto)  # Remove o produto do banco
        db.session.commit()  # Confirma a transação
        return jsonify({"message": "Produto excluído com sucesso!"})  # Retorna mensagem de sucesso
    except Exception as e:
        db.session.rollback()  # Reverte a transação em caso de erro
        return jsonify({"error": f"Erro ao excluir o produto: {str(e)}"}), 500

# Rota: Atualizar um produto (PUT /produtos/<id>)
@bp_produtos.route('/<int:id>', methods=['PUT'])
def atualizar_produto(id):
    produto = Produto.query.get(id)
    if not produto:
        return jsonify({"error": "Produto não encontrado"}), 404

    dados = request.get_json()
    if not dados:
        return jsonify({"error": "Dados ausentes na requisição"}), 400

    # Atualiza os dados
    produto.nome = dados.get('nome', produto.nome)
    produto.preco = dados.get('preco', produto.preco)
    produto.estoque = dados.get('estoque', produto.estoque)

    try:
        db.session.commit()
        return jsonify({"message": "Produto atualizado com sucesso!"})
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Erro ao atualizar o produto: {str(e)}"}), 500

bp_pedidos = Blueprint('pedidos', __name__, url_prefix='/pedidos')
@bp_pedidos.route('/', methods=['POST'])
def criar_pedido():
    dados = request.get_json()
    usuario_id = dados.get('usuario_id')
    produto_id = dados.get('produto_id')
    quantidade = dados.get('quantidade')

    if not usuario_id or not produto_id or not quantidade:
        return jsonify({"error": "Dados incompletos"}), 400

    novo_pedido = Pedido(usuario_id=usuario_id, produto_id=produto_id, quantidade=quantidade)
    db.session.add(novo_pedido)
    db.session.commit()
    return jsonify({"message": "Pedido criado com sucesso!", "pedido_id": novo_pedido.id}), 201

@bp_pedidos.route('/', methods=['GET'])
def listar_pedidos():
    pedidos = Pedido.query.all()
    pedidos_json = [
        {
            "id": p.id,
            "usuario_id": p.usuario_id,
            "produto_id": p.produto_id,
            "quantidade": p.quantidade,
        }
        for p in pedidos
    ]
    return jsonify(pedidos_json)

@bp_pedidos.route('/<int:id>', methods=['PUT'])
def atualizar_pedido(id):
    pedido = Pedido.query.get(id)
    if not pedido:
        return jsonify({"error": "Pedido não encontrado"}), 404

    dados = request.get_json()
    pedido.usuario_id = dados.get('usuario_id', pedido.usuario_id)
    pedido.produto_id = dados.get('produto_id', pedido.produto_id)
    pedido.quantidade = dados.get('quantidade', pedido.quantidade)

    db.session.commit()
    return jsonify({"message": "Pedido atualizado com sucesso!"})

@bp_pedidos.route('/<int:id>', methods=['DELETE'])
def excluir_pedido(id):
    pedido = Pedido.query.get(id)
    if not pedido:
        return jsonify({"error": "Pedido não encontrado"}), 404

    db.session.delete(pedido)
    db.session.commit()
    return jsonify({"message": "Pedido excluído com sucesso!"})
