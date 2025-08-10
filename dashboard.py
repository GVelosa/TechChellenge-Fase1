import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide")

@st.cache_data
def load_data():
    df = pd.read_csv("data/books_data.csv")
    if 'disponibilidade' in df.columns:
        df = df.drop(columns=['disponibilidade'])
    df['id'] = df.index
    return df

df = load_data()

st.sidebar.header("Filtros Visuais")
categorias = df['categoria'].unique()
categorias_selecionadas = st.sidebar.multiselect("Categoria", sorted(categorias))

preco_min = int(df['preco'].min())
preco_max = int(df['preco'].max())
faixa_preco_selecionada = st.sidebar.slider(
    "Faixa de Preço (£)",
    preco_min,
    preco_max,
    (preco_min, preco_max)
)

ratings = sorted(df['rating'].unique(), reverse=True)
ratings_selecionados = st.sidebar.multiselect("Avaliação (Rating)", ratings)

df_filtrado_visual = df.copy()
if categorias_selecionadas:
    df_filtrado_visual = df_filtrado_visual[df_filtrado_visual['categoria'].isin(categorias_selecionadas)]
if ratings_selecionados:
    df_filtrado_visual = df_filtrado_visual[df_filtrado_visual['rating'].isin(ratings_selecionados)]
df_filtrado_visual = df_filtrado_visual[
    (df_filtrado_visual['preco'] >= faixa_preco_selecionada[0]) & (df_filtrado_visual['preco'] <= faixa_preco_selecionada[1])
]

st.title("Dashboard de Análise de Livros")
st.markdown("Use os filtros na barra lateral para explorar visualmente o catálogo.")

total_livros, preco_medio, num_categorias_unicas = len(df_filtrado_visual), df_filtrado_visual['preco'].mean() if len(df_filtrado_visual) > 0 else 0, df_filtrado_visual['categoria'].nunique()
col1, col2, col3 = st.columns(3)
col1.metric("Total de Livros (na seleção)", f"{total_livros}")
col2.metric("Preço Médio (na seleção)", f"£ {preco_medio:.2f}")
col3.metric("Categorias (na seleção)", f"{num_categorias_unicas}")

st.markdown("---")

col_graf1, col_graf2 = st.columns(2)
with col_graf1:
    st.subheader("Distribuição de Preços")
    fig_preco = px.histogram(df_filtrado_visual, x="preco", nbins=50)
    st.plotly_chart(fig_preco, use_container_width=True)
with col_graf2:
    st.subheader("Top 10 Categorias com Mais Livros")
    top_10_categorias = df_filtrado_visual['categoria'].value_counts().nlargest(10)
    fig_categorias = px.bar(top_10_categorias, x=top_10_categorias.values, y=top_10_categorias.index, orientation='h', labels={'x': 'Qtde. Livros', 'y': 'Categoria'})
    st.plotly_chart(fig_categorias, use_container_width=True)

st.markdown("---")

st.title("🔎 Explorador de Funcionalidades")
st.markdown("Interaja com os dados como se estivesse usando os endpoints da API.")

with st.expander("Listar Livros (GET /books, GET /books/top-rated)"):
    if st.button("Listar TODOS os Livros"):
        st.dataframe(df, use_container_width=True)

    if st.button("Listar Livros com 5 Estrelas (Top Rated)"):
        top_rated_df = df[df['rating'] == 'Five']
        st.dataframe(top_rated_df, use_container_width=True)

with st.expander("Buscar Livro por ID (GET /books/{id})"):
    book_id_input = st.number_input("Digite o ID do Livro", min_value=0, max_value=len(df)-1, step=1, value=0)
    if st.button("Buscar por ID"):
        result_df = df[df['id'] == book_id_input]
        if not result_df.empty:
            st.json(result_df.to_dict(orient='records')[0])
        else:
            st.error("Livro com este ID não encontrado.")

with st.expander("Busca Avançada (GET /search, GET /price-range)"):
    st.subheader("Busca por Título e Categoria")
    search_title = st.text_input("Título contém...")
    search_category = st.selectbox("Categoria é...", options=["Qualquer"] + sorted(categorias))
    
    st.subheader("Busca por Faixa de Preço")
    search_min_price, search_max_price = st.slider("Preço entre...", preco_min, preco_max, (preco_min, preco_max))
    
    if st.button("Executar Busca Avançada"):
        df_busca = df.copy()
        if search_title:
            df_busca = df_busca[df_busca['titulo'].str.contains(search_title, case=False, na=False)]
        if search_category != "Qualquer":
            df_busca = df_busca[df_busca['categoria'] == search_category]
        
        df_busca = df_busca[
            (df_busca['preco'] >= search_min_price) & (df_busca['preco'] <= search_max_price)
        ]
        
        st.write(f"Encontrados {len(df_busca)} livros.")
        st.dataframe(df_busca, use_container_width=True)

with st.expander("Listar Categorias (GET /categories)"):
    if st.button("Ver todas as categorias únicas"):
        st.json({"categorias": sorted(categorias)})

with st.expander("Estatísticas e Saúde (GET /stats)"):
    if st.button("Ver Estatísticas Gerais (Overview)"):
        stats_overview = {
            'total_de_livros': len(df),
            'preco_medio': df['preco'].mean(),
            'distribuicao_de_ratings': df['rating'].value_counts().to_dict()
        }
        st.json(stats_overview)

    if st.button("Ver Estatísticas por Categoria"):
        stats_by_category = df.groupby('categoria')['preco'].agg(['count', 'mean']).rename(
            columns={'count': 'quantidade_de_livros', 'mean': 'preco_medio'}
        ).to_dict('index')
        st.json(stats_by_category)