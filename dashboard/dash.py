import streamlit as st
import duckdb
import pandas as pd

# Função para carregar dados do arquivo Parquet
def load_data():
    con = duckdb.connect()
    df = con.execute("SELECT * FROM 'data/measurements_summary.parquet'").df()
    con.close()
    return df

# Função principal para criar o dashboard
def main():
    st.title("Análise de Performance: Processamento de 1 Milhão de Linhas")
    
    # Métricas de Performance
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("DuckDB", "0.50 segundos")
    with col2:
        st.metric("Polars", "1.54 segundos")
    with col3:
        st.metric("Pandas", "7.39 segundos")

    # Gráfico de Performance
    st.subheader("Comparação de Performance")
    performance_data = pd.DataFrame({
        'Biblioteca': ['DuckDB', 'Polars', 'Pandas'],
        'Tempo (segundos)': [0.50, 1.54, 7.39]
    })
    st.bar_chart(performance_data, x='Biblioteca', y='Tempo (segundos)')

    # Dados das Estações
    st.subheader("Resumo das Estações Meteorológicas")
    st.write("Este dashboard mostra o resumo dos dados das estações, incluindo temperaturas mínimas, médias e máximas.")

    # Carregar os dados
    data = load_data()

    # Estatísticas gerais
    st.write(f"Total de estações: {len(data)}")
    
    # Exibir os dados em formato de tabela
    st.dataframe(data)

if __name__ == "__main__":
    main()