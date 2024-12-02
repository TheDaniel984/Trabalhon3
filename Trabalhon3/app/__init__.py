from flask import Flask
from .database import db  # Importando o banco de dados

def create_app():
    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    #não retia os # se não não funciona
    with app.app_context():
            from app.routes import bp as usuarios_bp  # type: ignore
            from app.routes import bp_produtos as produtos_bp  # type: ignore
            from app.routes import bp_pedidos as pedidos_bp  # type: ignore

            app.register_blueprint(usuarios_bp)
            app.register_blueprint(produtos_bp)
            app.register_blueprint(pedidos_bp)


            db.create_all()

    return app

