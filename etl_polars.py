import polars as pl
import time

# Definindo o caminho do arquivo
filename = "data/measurements.txt"

def process_chunk_polars(chunk):
    # Agrega os dados dentro do chunk usando Polars
    aggregated = (
        chunk.group_by("station")
        .agg([
            pl.col("measure").min().alias("min"),
            pl.col("measure").max().alias("max"),
            pl.col("measure").mean().alias("mean")
        ])
    )
    return aggregated

def create_df_with_polars(filename):
    # Lê o arquivo usando scan_csv para lidar com arquivos grandes
    scan = pl.scan_csv(filename, separator=';', has_header=False)
    
    # Coletar o DataFrame completo e renomear as colunas
    df = scan.collect().rename({"column_1": "station", "column_2": "measure"})
    
    # Processar o DataFrame completo
    result = process_chunk_polars(df)

    # Agrega os resultados finais
    final_aggregated_df = (
        result.group_by("station")
        .agg([
            pl.col("min").min(),
            pl.col("max").max(),
            pl.col("mean").mean()
        ])
        .sort("station")
    )

    return final_aggregated_df

if __name__ == "__main__":
    print("Iniciando o processamento do arquivo com Polars.")
    start_time = time.time()
    df = create_df_with_polars(filename)
    took = time.time() - start_time

    print(df.head())
    print(f"Processing with Polars took: {took:.2f} sec")
