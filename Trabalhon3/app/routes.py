from flask import Blueprint, jsonify, request
from .models import Pedido, Usuario, Produto,db 
# Importação do krl todo

# Blueprint usuários
bp = Blueprint('usuarios', __name__, url_prefix='/usuarios')

# Rota dos usuarios
@bp.route ( '/', methods=['GET'] )
def listar_usuarios():
    usuarios = Usuario.query.all()
    usuarios_json = [{"id": u.id, "nome": u.nome, "email": u.email} for u in usuarios]
    return jsonify(usuarios_json)

#novo usuário so pesquisar no potman assim http://127.0.0.1:5000/usuario (POST) 
@bp.route('/', methods=['POST'])
def criar_usuario():
    dados = request.get_json()
    novo_usuario = Usuario(nome=dados['nome'], email=dados['email'])
    db.session.add(novo_usuario)
    db.session.commit()
    return jsonify({"message": "Usuário criado"}), 201

#Atualiza o uzuario la no potman(PUT /usuarios/<id>)
@bp.route('/<int:id>', methods=[ 'PUT' ])
def atualizar_usuario(id):
    usuario = Usuario.query.get(id)
    if not usuario:
        return jsonify({"error": "Usuário não encontrado"}), 404
    
    dados = request.get_json()
    usuario.nome = dados.get('nome', usuario.nome)
    usuario.email = dados.get('email', usuario.email)

    db.session.commit()
    return jsonify({"message": "Usuário atualizado"})

#msm esquema so que de apagar o usuario
@bp.route('/<int:id>', methods=['DELETE'])
def excluir_usuario(id):
    usuario = Usuario.query.get(id)
    if not usuario:
        return jsonify({"error": "Usuário não encontrado"}), 404

    db.session.delete(usuario)
    db.session.commit()
    return jsonify({"message": "Usuário excluído"})

# Blueprint produtos
bp_produtos = Blueprint('produtos', __name__, url_prefix='/produtos')

@bp_produtos.route('/', methods=['GET'])
def listar_produtos():
    produtos = Produto.query.all()
    produtos_json = [{"id": p.id, "nome": p.nome, "preco": p.preco, "estoque": p.estoque} for p in produtos]
    return jsonify(produtos_json)


@bp_produtos.route('/', methods=['POST'])
def criar_produto():
    dados = request.get_json()
    if not dados:
        return jsonify({"error": "Dados ausentes na requisição"}), 400
    
    novo_produto = Produto(nome=dados['nome'], preco=dados['preco'], estoque=dados['estoque'])
    db.session.add(novo_produto)

    try:
        db.session.commit()
        return jsonify({"message": "Produto criado"}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"deu ruim ao salvar o produto: {str(e)}"}), 500


@bp_produtos.route('/<int:id>', methods=['DELETE'])
def excluir_produto(id):
    produto = Produto.query.get(id)  # Busca o produto pelo ID
    if not produto:
        return jsonify({"error": "Produto não encontrado"}), 404 

    try:
        db.session.delete(produto)  # Remove o produto
        db.session.commit()  # Confirma a transação
        return jsonify({"message": "Produto excluído"})
    except Exception as e:
        db.session.rollback()  #volta caso der ruim
        return jsonify({"error": f"deu ruim ao excluir o produto: {str(e)}"}), 500

# aqui so se repete a msm coisa do resto
@bp_produtos.route('/<int:id>', methods=['PUT'])
def atualizar_produto(id):
    produto = Produto.query.get(id)
    if not produto:
        return jsonify({"error": "Produto não encontrado"}), 404

    dados = request.get_json()
    if not dados:
        return jsonify({"error": "Dados ausentes na requisição"}), 400

    # Atualiza
    produto.nome = dados.get('nome', produto.nome)
    produto.preco = dados.get('preco', produto.preco)
    produto.estoque = dados.get('estoque', produto.estoque)

    try:
        db.session.commit()
        return jsonify({"message": "Produto atualizado"})
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"deu ruim ao atualizar o produto: {str(e)}"}), 500

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
    return jsonify({"message": "Pedido criado", "pedido_id": novo_pedido.id}), 201
#o de sempre
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
    #aqui pega pelo id e liga os pedidos com os usuarios ao produto
    dados = request.get_json()
    pedido.usuario_id = dados.get('usuario_id', pedido.usuario_id)
    pedido.produto_id = dados.get('produto_id', pedido.produto_id)
    pedido.quantidade = dados.get('quantidade', pedido.quantidade)

    db.session.commit()
    return jsonify({"message": "Pedido atualizado"})

@bp_pedidos.route('/<int:id>', methods=['DELETE'])
def excluir_pedido(id):
    pedido = Pedido.query.get(id)
    if not pedido:
        return jsonify({"error": "Pedido não encontrado"}), 404

    db.session.delete(pedido)
    db.session.commit()
    return jsonify({"message": "Pedido excluído"})
