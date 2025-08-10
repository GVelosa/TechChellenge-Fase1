from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flasgger import Swagger
from . import routes

db = SQLAlchemy()

def create_app():
    """Cria e configura uma instância do aplicativo Flask."""
    app = Flask(__name__)
    app.config.from_object('api.config')
    db.init_app(app)
    Swagger(app)

    @app.route('/')
    def index():
        html_content = """
        <!DOCTYPE html>
        <html lang="pt-BR">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>API de Livros</title>
            <style>
                body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif; line-height: 1.6; color: #333; max-width: 800px; margin: 40px auto; padding: 0 20px; }
                h1 { color: #2c3e50; }
                h2 { border-bottom: 2px solid #ecf0f1; padding-bottom: 10px; }
                ul { list-style-type: none; padding-left: 0; }
                li { background-color: #f9f9f9; border: 1px solid #ecf0f1; padding: 15px; margin-bottom: 10px; border-radius: 5px; }
                code { background-color: #ecf0f1; padding: 2px 6px; border-radius: 3px; font-family: "Courier New", Courier, monospace; }
                .method { font-weight: bold; color: #2980b9; }
            </style>
        </head>
        <body>
            <h1>Bem-vindo à API de Livros!</h1>
            <p>Esta é uma API para consultar informações sobre livros, extraídas do site 'books.toscrape.com'.</p>
            
            <h2>Endpoints Disponíveis:</h2>
            
            <h3>Core</h3>
            <ul>
                <li><span class="method">GET</span> <code>/api/v1/health</code>: Verifica status da API e conectividade com os dados.</li>
                <li><span class="method">GET</span> <code>/api/v1/books</code>: Lista todos os livros disponíveis na base de dados.</li>
                <li><span class="method">GET</span> <code>/api/v1/books/{id}</code>: Retorna detalhes completos de um livro específico pelo ID.</li>
                <li><span class="method">GET</span> <code>/api/v1/categories</code>: Lista todas as categorias de livros disponíveis.</li>
                <li><span class="method">GET</span> <code>/api/v1/books/search?title={title}&category={category}</code>: Busca livros por título e/ou categoria.</li>
            </ul>

            <h3>Insights & Estatísticas</h3>
            <ul>
                <li><span class="method">GET</span> <code>/api/v1/stats/overview</code>: Estatísticas gerais da coleção (total de livros, preço médio, etc.).</li>
                <li><span class="method">GET</span> <code>/api/v1/stats/categories</code>: Estatísticas detalhadas por categoria.</li>
                <li><span class="method">GET</span> <code>/api/v1/books/top-rated</code>: Lista os livros com melhor avaliação (rating mais alto).</li>
                <li><span class="method">GET</span> <code>/api/v1/books/price-range?min={min}&max={max}</code>: Filtra livros dentro de uma faixa de preço específica.</li>
            </ul>
        </body>
        </html>
        """
        return html_content
    
    app.register_blueprint(routes.bp)

    return app