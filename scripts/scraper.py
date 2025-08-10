import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
import time
import os

def scrape_all_books():
    """
    Função para fazer scraping de todos os livros e retornar uma lista de dicionários.
    """
    print("Iniciando scraping de todos os livros de forma 'educada'...")
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    url_base = 'https://books.toscrape.com/catalogue/'
    next_page_url = 'page-1.html'
    all_books_data = []
    session = requests.Session()
    session.headers.update(headers)

    while next_page_url:
        current_page_url = url_base + next_page_url
        response = session.get(current_page_url, timeout=15)
        
        soup = BeautifulSoup(response.text, 'html.parser')
        livros_na_pagina = soup.find_all('article', class_='product_pod')

        print(f"Acessando página: {current_page_url} | Encontrados {len(livros_na_pagina)} livros.")

        for livro in livros_na_pagina:
            titulo = livro.h3.a['title']
            preco_str = livro.find('p', class_='price_color').text
            preco = float(re.search(r'[\d\.]+', preco_str).group())
            rating = livro.find('p', class_='star-rating')['class'][1]
            disponibilidade = livro.find('p', class_='instock availability').text.strip()
            url_imagem_relativa = livro.find('img')['src']
            url_imagem_completa = 'https://books.toscrape.com/' + url_imagem_relativa.replace('../', '')
            url_livro_relativa = livro.h3.a['href']
            url_livro_completa = url_base + url_livro_relativa
            pagina_livro_response = session.get(url_livro_completa, timeout=15)
            soup_livro = BeautifulSoup(pagina_livro_response.text, 'html.parser')
            categoria = soup_livro.find('ul', class_='breadcrumb').find_all('a')[-1].text
            all_books_data.append({
                'titulo': titulo,
                'preco': preco,
                'rating': rating,
                'disponibilidade': disponibilidade,
                'categoria': categoria,
                'imagem_url': url_imagem_completa
            })

            time.sleep(0.5)

        next_button = soup.find('li', class_='next')
        next_page_url = next_button.a['href'] if next_button else None
            
    print(f"\nScraping finalizado! {len(all_books_data)} livros encontrados.")
    return all_books_data

def save_to_csv(books_data, filename="data/books_data.csv"):
    """Salva os dados dos livros em um arquivo CSV."""
    df = pd.DataFrame(books_data)
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    df.to_csv(filename, index=False)
    print(f"Dados salvos em {filename}")

if __name__ == '__main__':
    scraped_data = scrape_all_books()
    save_to_csv(scraped_data)