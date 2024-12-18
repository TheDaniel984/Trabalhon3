from .database import db  # ACHEI O ERRO krlrlrlrlr

class Usuario(db.Model):
    __tablename__ ='usuarios'

    id = db.Column( db.Integer, primary_key=True )
    nome = db.Column( db.String(100), nullable=False )
    email = db.Column( db.String(100), unique=True, nullable=False )

    def __repr__(self):
        # Corrigido dnv pq as rotas são mais instaveis que um buraco negro
        return f"<Usuario id={self.id}, nome={self.nome}, email={self.email}>"

    def to_dict(self):
        return {
            "id": self.id,
            "nome": self.nome,
            "email": self.email
        }


class Produto(db.Model):
    __tablename__ = 'produtos'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(80), nullable=False)
    preco = db.Column(db.Float, nullable=False)
    estoque = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"<Produto {self.nome}>"


class Pedido(db.Model):
    __tablename__ = 'pedidos'

    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    produto_id = db.Column(db.Integer, db.ForeignKey('produtos.id'), nullable=False)
    quantidade = db.Column(db.Integer, nullable=False)

    # Relacionamento
    usuario = db.relationship('Usuario', backref='pedidos')
    produto = db.relationship('Produto', backref='pedidos')

    def __repr__(self):
        return f"<Pedido id={self.id}, usuario_id={self.usuario_id}, produto_id={self.produto_id}, quantidade={self.quantidade}>"
