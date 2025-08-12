# API Pública de Consulta de Livros - Tech Challenge FIAP

Projeto de pipeline de dados e API RESTful, desenvolvido para o Tech Challenge de Machine Learning Engineering (Turma 6MLET - FIAP). A solução extrai dados de livros do site `books.toscrape.com` via web scraping, os processa e armazena em um banco de dados local, e os disponibiliza através de uma API e de um dashboard interativo.

## Arquitetura do Projeto

A solução é dividida em componentes desacoplados, garantindo modularidade и escalabilidade:

1.  **Ingestão e Processamento (`/scripts`)**: Um script Python (`scraper.py`) usa `requests` e `BeautifulSoup` para extrair os dados. O script `database_setup.py` orquestra a execução do scraper e a carga dos dados em um banco de dados e em um arquivo CSV.
2.  **Armazenamento (`/data`)**: Os dados são persistidos em um banco de dados **SQLite** (`books.db`), gerenciado pelo ORM **SQLAlchemy**. Uma cópia dos dados brutos também é salva em formato **CSV** (`books_data.csv`).
3.  **API RESTful (`/api`)**: Construída com **Flask**, esta API serve os dados armazenados no banco de dados. Ela utiliza **Blueprints** para organização de rotas e **Flasgger** para gerar uma documentação interativa com Swagger UI.
4.  **Dashboard Interativo (`dashboard.py`)**: Uma aplicação **Streamlit** que atua como cliente dos dados, oferecendo visualizações, filtros e uma interface para explorar as funcionalidades da API de forma intuitiva, lendo diretamente do arquivo CSV.

**Fluxo de Dados:**
`Site Web` → `Scraper` → `Banco de Dados (SQLite) / CSV` → `API Flask` → `Dashboard / Consumidor Final`

## Instalação e Configuração

Siga os passos abaixo para configurar o ambiente e executar o projeto localmente.

### Pré-requisitos

* [Python](https://www.python.org/downloads/) (versão 3.9 ou superior)
* [Git](https://git-scm.com/downloads/)

### Passo a Passo

1.  **Clone o repositório:**
    ```bash
    git clone https://github.com/GVelosa/TechChellenge-Fase1.git
    cd TechChellenge-Fase1
    ```

2.  **Crie e ative um ambiente virtual:**
    * **Windows:**
        ```bash
        python -m venv venv
        .\venv\Scripts\activate
        ```
    * **macOS / Linux:**
        ```bash
        python3 -m venv venv
        source venv/bin/activate
        ```

3.  **Instale as dependências:**
    ```bash
    pip install -r requirements.txt
    ```

## Instruções para Execução

Após a instalação, é possivel rodar o scraper e popular o ban.

### 1. Iniciar a API RESTful

Em um terminal, execute o seguinte comando para iniciar o servidor Flask:
```bash
python run.py
```
Após isso a menssagem: 'Deseja executar o web scraping para atualizar a base de dados? (s/n):' será exibida, caso queira executar o scraper digite 's' caso o banco de dados eo csv já estejam criados digite 'n' para pular essa etapa.

Após isso a API estará disponível em `http://127.0.0.1:5000`.

### 2. Iniciar o Dashboard Interativo

**Abra um novo terminal**, navegue até a pasta do projeto e ative o ambiente virtual novamente. Em seguida, execute:
```bash
streamlit run dashboard.py
```
O dashboard será aberto automaticamente no seu navegador, geralmente em `http://127.0.0.1:8501`.

## Documentação da API

### Acesso via Swagger UI

Uma das maneira mais fácil de explorar e testar todos os endpoints da API é através da documentação interativa gerada pelo Swagger UI. Com o servidor da API rodando, acesse:

* **[http://127.0.0.1:5000/apidocs](http://127.0.0.1:5000/apidocs)**

### Exemplos de Chamadas e Respostas

A seguir, exemplos de como chamar cada endpoint e o formato esperado da resposta em JSON.

#### `GET /api/v1/health`
Verifica a saúde da API.

**Chamada:**
```bash
  http://127.0.0.1:5000/api/v1/health
```
**Resposta:**
```json
{
  "book_count": 1000,
  "message": "API is healthy and connected to the database",
  "status": "ok"
}
```

#### `GET /api/v1/books`
Lista todos os livros.

**Chamada:**
```bash
  http://127.0.0.1:5000/api/v1/books
```
**Resposta (mostrando o primeiro livro):**
```json
[
  {
    "categoria": "Poetry",
    "id": 1,
    "imagem_url": "[http://books.toscrape.com/media/cache/2c/da/2cdad67c44b002e7ead0cc35693c0e8b.jpg](http://books.toscrape.com/media/cache/2c/da/2cdad67c44b002e7ead0cc35693c0e8b.jpg)",
    "preco": 51.77,
    "rating": "Three",
    "titulo": "A Light in the Attic"
  }
]
```

#### `GET /api/v1/books/{id}`
Retorna os detalhes de um livro específico.

**Chamada:**
```bash
  http://127.0.0.1:5000/api/v1/books/10
```
**Resposta:**
```json
{
    "categoria": "Mystery",
    "id": 10,
    "imagem_url": "[http://books.toscrape.com/media/cache/c0/59/c0597280562c46f1184f3d242f895c81.jpg](http://books.toscrape.com/media/cache/c0/59/c0597280562c46f1184f3d242f895c81.jpg)",
    "preco": 47.82,
    "rating": "Four",
    "titulo": "Sharp Objects"
}
```

#### `GET /api/v1/categories`
Lista todas as categorias únicas.

**Chamada:**
```bash
  http://127.0.0.1:5000/api/v1/categories
```
**Resposta:**
```json
[
  "Add a comment",
  "Art",
  "Autobiography",
  "Biography",
  "Business",
  "Childrens"
]
```

#### `GET /api/v1/books/search`
Busca livros por título e/ou categoria.

**Chamada (título contendo "story"):**
```bash
  http://127.0.0.1:5000/api/v1/books/search?title=story
```

#### `GET /api/v1/books/price-range`
Filtra livros dentro de uma faixa de preço.

**Chamada (preço entre £20 e £25):**
```bash
  http://127.0.0.1:5000/api/v1/books/price-range?min=20&max=25
```

#### `GET /api/v1/books/top-rated`
Lista os livros com avaliação máxima (5 estrelas).

**Chamada:**
```bash
  http://127.0.0.1:5000/api/v1/books/top-rated
```

#### `GET /api/v1/stats/overview`
Retorna estatísticas gerais da coleção.

**Chamada:**
```bash
  http://127.0.0.1:5000/api/v1/stats/overview
```
**Resposta:**
```json
{
  "distribuicao_de_ratings": {
    "Five": 196,
    "Four": 203,
    "One": 202,
    "Three": 203,
    "Two": 196
  },
  "preco_medio": 35.07,
  "total_de_livros": 1000
}
```

#### `GET /api/v1/stats/categories`
Retorna estatísticas detalhadas por categoria.

**Chamada:**
```bash
  http://127.0.0.1:5000/api/v1/stats/categories
```
**Resposta (parcial):**
```json
{
  "Add a comment": {
    "preco_medio": 35.53,
    "quantidade_de_livros": 67
  },
  "Art": {
    "preco_medio": 39.22,
    "quantidade_de_livros": 18
  }
}
```
**Dica:** Todas essas informações também podem ser exploradas de forma visual e interativa através do **Dashboard Streamlit**.