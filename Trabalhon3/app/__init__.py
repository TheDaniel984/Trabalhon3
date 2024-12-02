from flask import Flask
from .database import db  # Importando o banco de dados

def create_app():
    app = Flask(__name__)

    # Configurações do banco de dados
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'  # Banco SQLite local
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Desabilita alertas desnecessários

    # Inicializa o banco de dados com o Flask
    db.init_app(app)

    # Importa e registra os blueprints
    with app.app_context():
        from app.routes import bp as usuarios_bp  # type: ignore # Rotas de usuários
        from app.routes import bp_produtos as produtos_bp  # type: ignore # Rotas de produtos
        from app.routes import bp_pedidos as pedidos_bp  # type: ignore # Rotas de pedidos

        app.register_blueprint(usuarios_bp)
        app.register_blueprint(produtos_bp)
        app.register_blueprint(pedidos_bp)

        # Cria as tabelas no banco de dados
        db.create_all()

    return app

