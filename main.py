#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
File:           main.py
Author:         Antonio Arteaga
Last Updated:   2025-11-28
Version:        2.0
Description:
Connection to a SQLServer DB for 5 tables and multiple values in column 'ReceptorRFC'.
The query result for every table is saved in an excel file (or multiple excel files).
Dependencies:   pyodbc==5.3.0, pandas==2.3.3, openpyxl==3.1.5, python-dotenv==1.2.1.
Usage:          Every sql query has the form:
SELECT TOP 10 *
FROM "2024-AECF_0101_Anexo4-Detalle-Percepciones"
WHERE ReceptorRFC IN ('PEES540914FT3')
"""

import pyodbc
import pandas as pd
import time
import math
import warnings
from config import DB_CONFIG

# All tables and all RFCs to perform the queries
percepciones_table = "2024-AECF_0101_Anexo4-Detalle-Percepciones"
deducciones_table = "2024-AECF_0101_Anexo5-Detalle-Deducciones"
receptorRFC_list = ["PEES540914FT3"]
# report_name = "Reporte de los datos.xlsx"
log_file = "Valores en percepciones y deducciones.txt"
MAX_ROWS_PER_TABLE = 6              # Maximum number of rows per excel file

table_list = [percepciones_table]

conn_str = (
    f"DRIVER={DB_CONFIG['driver']};"
    f"SERVER={DB_CONFIG['server']};"
    f"DATABASE={DB_CONFIG['database']};"
    f"UID={DB_CONFIG['username']};"
    f"PWD={DB_CONFIG['password']};"
    "Encrypt=yes;"
    "TrustServerCertificate=yes;"
)

# To ignore all warnings
warnings.filterwarnings("ignore")


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


def main():
    try:
        conn = pyodbc.connect(conn_str)
        print(f"Conexión exitosa con la DB '{DB_CONFIG['database']}'.")
        queries = construct_queries(table_list, receptorRFC_list)
        execute_queries(conn, table_list, queries)
        conn.close()

    except Exception as e:
        print("Error al conectar o ejecutar consulta:", e)


if __name__ == "__main__":
    main()
