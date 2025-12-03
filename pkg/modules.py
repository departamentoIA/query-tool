# modules.py
from pkg.settings import *
import os


def construct_queries(table_list: list[str], receptorRFC_list: list[str]) -> list[str]:
    """Construct every query for every table"""
    queries = []
    # Create placeholders: "?, ?" (needed when using pyodbc)
    placeholders = ", ".join("?" * len(receptorRFC_list))
    for table in table_list:
        query = f"""
        SELECT TOP 10 *
        FROM [{table}]
        WHERE EmisorRFC IN ({placeholders})
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
        destination_path = os.path.join(os.getcwd(), path_results, file_name)
        df_part.to_excel(destination_path, index=False)
    print(f"Tabla '{table}' guardada con éxito!\n")


def execute_queries(conn: pyodbc.Connection, table_list: list[str], queries: list[str]) -> None:
    """
    SQl queries are performed for every table in "table_list" and for every query.
    All queries are already built in "queries". All DataFrames are saved.
    """
    print("Se procede a ejecutar las consultas en las tablas 'Detalle-Percepciones' y 'Detalle-Deducciones'"
          + "después se creará un archivo txt con los diferentes valores encontrados en las columnas"
          + "'percepcionClave' y 'deduccionClave' de las tablas antes mencionadas.")
    for table, query in zip(table_list, queries):
        print("Ejecutando consulta...")
        t1 = time.time()
        df = pd.read_sql(query, conn, params=receptorRFC_list)
        print(f"Tiempo de consulta para la tabla '{table}':", int(
            time.time() - t1), "segundos.")
        print("Guardando tabla, espere por favor...")
        # Save the complete DataFrames, this part can be ommited -------
        if table == percepciones_table:
            destination_path = os.path.join(
                os.getcwd(), path_results, percepciones_table+".xlsx")
            df.to_excel(destination_path, index=False)
        if table == deducciones_table:
            destination_path = os.path.join(
                os.getcwd(), path_results, deducciones_table+".xlsx")
            df.to_excel(destination_path, index=False)
        # End of data analysis------------------------------------------
        split_DataFrame(table, df, MAX_ROWS_PER_TABLE)


def load_excel(path: str, table: str) -> pd.DataFrame:
    """Read DataFrame from an excel file."""
    full_path = os.path.join(os.getcwd(), path, table+".xlsx")
    df = pd.read_excel(full_path)
    return df


def open_DataFrame(path_results: str, excel_file: str) -> pd.DataFrame:
    """
    Read DataFrame from excel file, the name without '.xlsx'.
    """
    try:
        df = load_excel(path_results, excel_file)
        return df
    except:
        print(f"Archivo '{excel_file+".xlsx"}' no encontrado")
