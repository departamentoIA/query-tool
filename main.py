#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
File:           main.py
Author:         Antonio Arteaga
Last Updated:   2025-11-26
Version:        1.0
Description:
Connection to a SQLServer DB for 5 tables and multiple values in column 'ReceptorRFC'.
The query result for every table is saved in an excel file (or multiple excel files).
Dependencies:   pyodbc==5.3.0, pandas==2.3.3, openpyxl==3.1.5.
Usage:          Every sql query has the form:
SELECT TOP 4 *
FROM "2024-AECF_0101_Anexo4-Detalle-Percepciones"
WHERE ReceptorRFC IN ('PEES540914FT3')
"""

import pyodbc
import pandas as pd
import time
import math
import warnings

# Set Connection parameters
server = '10.0.14.27\\PRODMIXTIC2022,6538'
database = 'SAT-Nomina'
username = 'caarteaga'
password = 'Audi2025'

# Set all tables and all RFCs to perform the queries
percepciones_table = "2024-AECF_0101_Anexo4-Detalle-Percepciones"
deducciones_table = "2024-AECF_0101_Anexo5-Detalle-Deducciones"
receptorRFC_list = ["SSI220901JS5"]
report_name = "Reporte de los datos.xlsx"
MAX_ROWS_PER_TABLE = 6              # Maximum number of rows per excel file

table_list = [percepciones_table,
              deducciones_table]

# Connection configuration
connection_string = (
    "DRIVER={ODBC Driver 18 for SQL Server};"
    f"SERVER={server};"
    f"DATABASE={database};"
    f"UID={username};"
    f"PWD={password};"
    "Encrypt=no;"                   # or "Encrypt=yes;TrustServerCertificate=yes;"
)

# To ignore all warnings
warnings.filterwarnings("ignore")


def construct_queries(table_list: list, receptorRFC_list: list) -> list:
    """Construct every query for every table"""
    queries = []
    # Create placeholders: "?, ?"
    placeholders = ", ".join("?" * len(receptorRFC_list))
    for table in table_list:
        query = f"""
        SELECT TOP 10 *
        FROM [{table}]
        WHERE ReceptorRFC IN ({placeholders})
        """
        queries.append(query)
    return queries


def value_count_in_column(col_name: str, df: pd.DataFrame) -> list:
    """Calculate all different values in a column and return a list with all values."""
    col_name_values = []
    if col_name in df.columns:
        col_name_values = df[col_name].unique()
    return col_name_values


def split_DataFrame(table: str, df: pd.DataFrame, max_rows=600000) -> None:
    """Split every DataFrame and save it in different excel files,
    if it has more that 600,000 rows."""
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


def save_lists_as_DataFrame(report_name: str, percepcion_values: list, deduccion_values: list) -> None:
    """Create a DataFrame with the entry lists and save it in an excel file."""
    # Fill the shortest list
    max_len = max(len(percepcion_values), len(deduccion_values))
    print(max_len)
    percepcion = percepcion_values + [None] * \
        (max_len - len(percepcion_values))
    deduccion = deduccion_values + [None] * (max_len - len(deduccion_values))

    df = pd.DataFrame({"Percepcion_Valores": percepcion,
                      "Deduccion_Valores": deduccion})
    print(percepcion)
    print(deduccion)
    print(df)
    df.to_excel(report_name, index=False)


def execute_queries(conn: pyodbc.Connection, table_list: list, queries: list) -> None:
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
            percepcionClave_values = value_count_in_column(
                "PercepcionClave", df)
        if table == deducciones_table:
            deduccionClave_values = value_count_in_column("DeduccionClave", df)
        # End of data analysis------------------------------
        split_DataFrame(table, df, MAX_ROWS_PER_TABLE)
    print(f"Valores diferentes de percepcion = {percepcionClave_values}")
    print(f"Valores diferentes de deduccion= {deduccionClave_values}")
    save_lists_as_DataFrame(
        report_name, percepcionClave_values, deduccionClave_values)
    return


def main():
    try:
        conn = pyodbc.connect(connection_string)
        print(f"Conexión exitosa con la base de datos '{database}'.")
        queries = construct_queries(table_list, receptorRFC_list)
        execute_queries(conn, table_list, queries)
        conn.close()

    except Exception as e:
        print("Error al conectar o ejecutar consulta:", e)


if __name__ == "__main__":
    main()
