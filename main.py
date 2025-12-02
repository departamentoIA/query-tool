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
FROM dbo.[2024-AECF_0101_Anexo4-Detalle-Percepciones]
WHERE EmisorRFC IN ('IMS421231I45','ISC091217HC7')
"""

from pkg.modules import *


def sql_process() -> None:
    """
    DB connection and sql queries are performed, then the 5 DataFrames are saved as excel files.
    """
    try:
        conn = pyodbc.connect(conn_str)
        print(f"Conexión exitosa con la DB '{DB_CONFIG['database']}'.")
        queries = construct_queries(table_list, receptorRFC_list)
        execute_queries(conn, table_list, queries)
        conn.close()

    except Exception as e:
        print("Error al conectar o ejecutar consulta:", e)


def analitics() -> None:
    """
    iles.
    """
    df_percepciones = open_DataFrame(path_results, percepciones_table)
    df_deducciones = open_DataFrame(path_results, deducciones_table)
    df_catalogo = open_DataFrame(path_results, catalogo_excel)
    df_catalogo.columns = ['EmisorRFC', 'Dependencia']

    # DataFrame merging
    percepcion = df_percepciones.merge(df_catalogo, on='EmisorRFC', how='left')
    deduccion = df_deducciones.merge(df_catalogo, on='EmisorRFC', how='left')

    percepcionClave_values = percepcion['PercepcionClave'].unique()
    deduccionClave_values = deduccion['DeduccionClave'].unique()
    print(f"percepcionClave_values = {percepcionClave_values}")
    print(f"deduccionClave_values = {deduccionClave_values}")
    if len(percepcionClave_values) < MAX_COLUMN_VALS:
        print("Sí se pivotea la tabla")
        # full_name = percepciones_table + "_pivoteada.xlsx"
        # percepcion.to_excel(full_name, index=False)
    else:
        print("No se pivotea la tabla")

    if len(deduccionClave_values) < MAX_COLUMN_VALS:
        print("Sí se pivotea la tabla")
        # full_name = deducciones_table + "_pivoteada.xlsx"
        # deduccion.to_excel(full_name, index=False)
    else:
        print("No se pivotea la tabla")


def main():
    sql_process()
    analitics()


if __name__ == "__main__":
    main()
