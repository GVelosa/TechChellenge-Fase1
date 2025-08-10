from . import db

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(255), nullable=False)
    preco = db.Column(db.Float, nullable=False)
    rating = db.Column(db.String(20))
    disponibilidade = db.Column(db.String(50))
    categoria = db.Column(db.String(100), nullable=False)
    imagem_url = db.Column(db.String(255))

    def to_dict(self):
        """Converte o objeto Book para um dicionário, útil para a resposta JSON."""
        return {
            'id': self.id,
            'titulo': self.titulo,
            'preco': self.preco,
            'rating': self.rating,
            'disponibilidade': self.disponibilidade,
            'categoria': self.categoria,
            'imagem_url': self.imagem_url
        }