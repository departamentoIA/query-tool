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
Dependencies:   pyodbc==5.3.0, pandas==2.3.3, openpyxl==3.1.5, python-dotenv==1.2.1,
Driver 'ODBC Driver 18 for SQL Server' installed (file "msodbcsql.msi").
Usage:          Every sql query has the form:
----
SELECT TOP 10 *
FROM dbo.[2024-AECF_0101_Anexo4-Detalle-Percepciones]
WHERE EmisorRFC IN ('IMS421231I45','ISC091217HC7','SSI220901JS5')
----
Portability:    To make this project executable, run:
pyinstaller --onefile --add-data "pkg/.env;." main.py
"""

from pkg.modules import *
from pkg.settings import conn_str
import pyodbc


def sql_process() -> None:
    """
    DB connection and sql queries are performed, the 5 DataFrames are saved as excel files.
    """
    try:
        conn = pyodbc.connect(conn_str)
        drivers = [driver for driver in pyodbc.drivers() if "SQL" in driver]
        print("Drivers encontrados:", drivers)
        print(f"Conexión exitosa con la DB '{DB_CONFIG['database']}'.")
        queries = construct_queries(table_list, receptorRFC_list)
        execute_queries(conn, table_list, queries)
        conn.close()

    except Exception as e:
        print("Error al conectar o ejecutar consulta:", e)


def merge_Dataframes(path_results: str, table_name: str, catalogo_name: str) -> pd.DataFrame:
    df = open_DataFrame(path_results, table_name)
    df_catalogo = open_DataFrame(path_results, catalogo_name)
    df_catalogo.columns = ['EmisorRFC', 'Dependencia']
    # Merge DataFrames
    return df.merge(df_catalogo, on='EmisorRFC', how='left')


def pivot_table(df: pd.DataFrame, percepciones_table: str) -> None:
    pass


def analitics() -> None:
    """
    Two DataFrames are merged with 'catalog' file to obtain one column,
    if there are more than 50 different values in columns 'PercepcionClave'
    and 'DeduccionClave', these two DataFrames are not pivoted, else they are pivoted.
    """
    percepcion = merge_Dataframes(
        path_results, percepciones_table, catalogo_excel)

    deduccion = merge_Dataframes(
        path_results, deducciones_table, catalogo_excel)

    percepcionClave_values = percepcion['PercepcionClave'].unique()
    deduccionClave_values = deduccion['DeduccionClave'].unique()

    f.write(f"{len(percepcionClave_values)} Valores diferentes de percepcionClave:\n{percepcionClave_values}\n")
    if len(percepcionClave_values) < MAX_COLUMN_VALS:
        print("La tabla 'Detalle-Percepciones' sí se pivotea")
        f.write(f"Pocas columnas, la tabla sí se pivotea.\n\n")
        # pivot_table(percepcion,percepciones_table)
    else:
        print("La tabla 'Detalle-Percepciones' no se pivotea la tabla")
        f.write(f"Demasiadas columnas, la tabla no se pivotea.\n")

    f.write(f"{len(deduccionClave_values)} Valores diferentes de deduccionClave:\n{deduccionClave_values}\n")
    if len(deduccionClave_values) < MAX_COLUMN_VALS:
        print("La tabla 'Detalle-Deducciones' sí se pivotea")
        f.write(f"Pocas columnas, la tabla sí se pivotea.\n\n")
        # pivot_table(deduccion,deduccionClave_values)
    else:
        print("La tabla 'Detalle-Deducciones' no se pivotea la tabla")
        f.write(f"Demasiadas columnas, la tabla no se pivotea.\n")


def main():
    sql_process()
    analitics()
    f.close()


if __name__ == "__main__":
    main()
