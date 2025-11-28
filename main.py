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


from pkg.modules import *


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
