import sys
import os
from api import create_app, db
from api.models import Book
from scripts.scraper import scrape_all_books, save_to_csv

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

def populate_database():
    """
    Executa o scraper e popula o banco de dados com os livros.
    Também salva uma cópia dos dados em CSV.
    """
    books_data = scrape_all_books()
    save_to_csv(books_data)
    
    app = create_app()
    with app.app_context():
        print("Criando tabelas do banco de dados...")
        db.create_all()
        
        print("Populando o banco de dados com os livros...")
        for book_data in books_data:
            new_book = Book(
                titulo=book_data['titulo'],
                preco=book_data['preco'],
                rating=book_data['rating'],
                disponibilidade=book_data['disponibilidade'],
                categoria=book_data['categoria'],
                imagem_url=book_data['imagem_url']
            )
            db.session.add(new_book)
        
        db.session.commit()
        print("Banco de dados populado com sucesso!")

if __name__ == '__main__':
    populate_database()