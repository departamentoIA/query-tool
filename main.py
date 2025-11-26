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

# To ignore all warnings
warnings.filterwarnings("ignore")

# Connection parameters
server = '10.0.14.27\\PRODMIXTIC2022,6538'
database = 'SAT-Nomina'
username = 'caarteaga'
password = 'Audi2025'

table_list = ["2024-AECF_0101_Anexo4-Detalle-Percepciones"]
receptor_RFC_list = ["PEES540914FT3"]
# Create placeholders: "?, ?"
placeholders = ", ".join("?" * len(receptor_RFC_list))
MAX_ROWS_PER_TABLE = 6

# Connection configuration
connection_string = (
    "DRIVER={ODBC Driver 18 for SQL Server};"
    f"SERVER={server};"
    f"DATABASE={database};"
    f"UID={username};"
    f"PWD={password};"
    "Encrypt=no;"              # o "Encrypt=yes;TrustServerCertificate=yes;"
)

# Construct every query for every table
queries = []
for table in table_list:
    query = f"""
    SELECT TOP 10 *
    FROM [{table}]
    WHERE ReceptorRFC IN ({placeholders})
    """
    queries.append(query)


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
    return


def execute_queries(table_list: list, queries: list) -> None:
    """
    SQl queries are performed for every table in "table_list" and for every query in "queries".
    All queries are already built in "queries".
    """
    for table, query in zip(table_list, queries):
        print("Ejecutando consulta...")
        t1 = time.time()
        df = pd.read_sql(query, conn, params=receptor_RFC_list)
        print(f"Tiempo de consulta para la tabla '{table}':", time.time() - t1)
        split_DataFrame(table, df, MAX_ROWS_PER_TABLE)
    return


try:
    conn = pyodbc.connect(connection_string)
    print(f"Conexión exitosa con la base de datos '{database}'.")
    execute_queries(table_list, queries)
    conn.close()

except Exception as e:
    print("Error al conectar o ejecutar consulta:", e)
