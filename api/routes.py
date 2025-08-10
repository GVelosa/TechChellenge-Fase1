from flask import Blueprint, jsonify, request
from . import db
from .models import Book
from collections import Counter

bp = Blueprint('api', __name__, url_prefix='/api/v1')

@bp.route('/health')
def health_check():
    """Verifica o status da API.
    Este endpoint pode ser usado para monitorar se a API está no ar e conectada à base de dados.
    ---
    tags:
      - Monitoramento
    responses:
      200:
        description: A API está saudável.
    """
    book_count = Book.query.count()
    return jsonify({
        'status': 'ok',
        'message': 'API is healthy and connected to the database',
        'book_count': book_count
    })

@bp.route('/books', methods=['GET'])
def get_all_books():
    """Lista todos os livros do banco de dados.
    ---
    tags:
      - Livros
    responses:
      200:
        description: Uma lista de todos os livros.
    """
    books = Book.query.all()
    return jsonify([book.to_dict() for book in books])

@bp.route('/books/<int:book_id>', methods=['GET'])
def get_book_by_id(book_id):
    """Retorna detalhes de um livro específico pelo ID.
    ---
    tags:
      - Livros
    parameters:
      - name: book_id
        in: path
        type: integer
        required: true
        description: O ID único do livro a ser consultado.
    responses:
      200:
        description: Detalhes do livro encontrados com sucesso.
      404:
        description: O livro com o ID especificado não foi encontrado.
    """
    book = Book.query.get_or_404(book_id)
    return jsonify(book.to_dict())

@bp.route('/books/search', methods=['GET'])
def search_books():
    """Busca livros por título e/ou categoria.
    ---
    tags:
      - Livros
    parameters:
      - name: title
        in: query
        type: string
        required: false
        description: Parte do título do livro para a busca (case-insensitive).
      - name: category
        in: query
        type: string
        required: false
        description: Categoria exata do livro para a busca (case-insensitive).
    responses:
      200:
        description: Uma lista de livros que correspondem aos critérios de busca.
    """
    query = Book.query
    query_title = request.args.get('title', '').lower()
    query_category = request.args.get('category', '').lower()
    if query_title:
        query = query.filter(Book.titulo.ilike(f'%{query_title}%'))
    if query_category:
        query = query.filter(Book.categoria.ilike(f'%{query_category}%'))
    results = query.all()
    return jsonify([book.to_dict() for book in results])

@bp.route('/categories', methods=['GET'])
def get_all_categories():
    """Lista todas as categorias únicas.
    ---
    tags:
      - Categorias
    responses:
      200:
        description: Uma lista ordenada de todas as categorias de livros disponíveis.
    """
    categories_query = db.session.query(Book.categoria).distinct().order_by(Book.categoria)
    categories = [row[0] for row in categories_query]
    return jsonify(categories)

@bp.route('/books/top-rated', methods=['GET'])
def get_top_rated_books():
    """Lista os livros com a melhor avaliação (Five).
    ---
    tags:
      - Livros
    responses:
      200:
        description: Uma lista de livros com avaliação 'Five'.
    """
    top_books = Book.query.filter_by(rating='Five').all()
    return jsonify([book.to_dict() for book in top_books])

@bp.route('/books/price-range', methods=['GET'])
def get_books_by_price_range():
    """Filtra livros dentro de uma faixa de preço.
    ---
    tags:
      - Livros
    parameters:
      - name: min
        in: query
        type: number
        format: float
        required: false
        description: Preço mínimo.
      - name: max
        in: query
        type: number
        format: float
        required: false
        description: Preço máximo.
    responses:
      200:
        description: Uma lista de livros dentro da faixa de preço especificada.
      400:
        description: Erro se os parâmetros não forem números válidos.
    """
    try:
        min_price = float(request.args.get('min', 0))
        max_price = float(request.args.get('max', float('inf')))
    except ValueError:
        return jsonify({'error': 'Invalid price format. Please use numbers.'}), 400

    query = Book.query.filter(Book.preco >= min_price).filter(Book.preco <= max_price)
    results = query.all()
    return jsonify([book.to_dict() for book in results])

@bp.route('/stats/overview', methods=['GET'])
def get_stats_overview():
    """Estatísticas gerais da coleção.
    ---
    tags:
      - Estatísticas
    responses:
      200:
        description: Um resumo com estatísticas gerais da coleção de livros.
    """
    total_livros = Book.query.count()

    preco_total = db.session.query(db.func.sum(Book.preco)).scalar()
    preco_medio = round(preco_total / total_livros, 2) if total_livros > 0 else 0

    ratings_query = db.session.query(Book.rating, db.func.count(Book.rating)).group_by(Book.rating).all()
    ratings_distribution = {rating: count for rating, count in ratings_query}
    
    return jsonify({
        'total_de_livros': total_livros,
        'preco_medio': preco_medio,
        'distribuicao_de_ratings': ratings_distribution
    })

@bp.route('/stats/categories', methods=['GET'])
def get_stats_by_category():
    """Estatísticas detalhadas por categoria.
    ---
    tags:
      - Estatísticas
    responses:
      200:
        description: Um objeto com estatísticas para cada categoria.
    """
    stats_query = db.session.query(
        Book.categoria, 
        db.func.count(Book.id), 
        db.func.avg(Book.preco)
    ).group_by(Book.categoria).all()
    
    stats = {
        categoria: {
            'quantidade_de_livros': count,
            'preco_medio': f'{round(avg_price, 2)}'
        }
        for categoria, count, avg_price in stats_query
    }
    return jsonify(stats)