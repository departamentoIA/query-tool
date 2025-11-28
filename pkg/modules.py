# modules.py
from pkg.settings import *


def construct_queries(table_list: list[str], receptorRFC_list: list[str]) -> list[str]:
    """Construct every query for every table"""
    queries = []
    # Create placeholders: "?, ?" (needed when using pyodbc)
    placeholders = ", ".join("?" * len(receptorRFC_list))
    for table in table_list:
        query = f"""
        SELECT TOP 10 *
        FROM [{table}]
        WHERE ReceptorRFC IN ({placeholders})
        """
        queries.append(query)
    return queries


def split_DataFrame(table: str, df: pd.DataFrame, max_rows=600000) -> None:
    """Split every DataFrame and save it in different excel files,
    if it has many rows."""
    total_rows = len(df)
    if total_rows == 0:
        print("El DataFrame está vacío. No se guarda ningún archivo.")
        return
    # Calculate how many files parts for this DataFrame
    n_files = math.ceil(total_rows / max_rows)
    for i in range(n_files):
        inicio = i * max_rows
        fin = inicio + max_rows
        df_part = df.iloc[inicio:fin]
        file_name = f"{table}_part_{i+1}.xlsx"
        df_part.to_excel(file_name, index=False)
    print(f"Tabla '{table}' guardada con éxito!\n")


def execute_queries(conn: pyodbc.Connection, table_list: list[str], queries: list[str]) -> None:
    """
    SQl queries are performed for every table in "table_list" and for every query.
    All queries are already built in "queries".
    """
    percepcionClave_values = []
    deduccionClave_values = []
    for table, query in zip(table_list, queries):
        print("Ejecutando consulta...")
        t1 = time.time()
        df = pd.read_sql(query, conn, params=receptorRFC_list)
        print(f"Tiempo de consulta para la tabla '{table}':", time.time() - t1)
        # Analize the data, this part can be ommited -------
        if table == percepciones_table:
            percepcionClave_values = df['PercepcionClave'].unique()
        if table == deducciones_table:
            deduccionClave_values = df['DeduccionClave'].unique()
        # End of data analysis------------------------------
        split_DataFrame(table, df, MAX_ROWS_PER_TABLE)

    with open(log_file, "w", encoding="utf-8") as f:
        f.write(
            f"{len(percepcionClave_values)} Valores diferentes de percepcionClave:\n{percepcionClave_values}\n")
        f.write(
            f"{len(deduccionClave_values)} Valores diferentes de deduccionClave:\n{deduccionClave_values}\n")
