#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
File:           pyodbc_sqlserver_example.py
Author:         Antonio Arteaga
Last Updated:   2025-11-26
Version:        1.0
Description:
Simple example of connection to a DB by using SQLServer and Python.
The query result is saved in an excel file.
Dependencies:   pyodbc==5.3.0, pandas==2.3.3, openpyxl==3.1.5.
"""


import pyodbc
import pandas as pd
import time

# Connection parameters
server = '10.0.14.27\\PRODMIXTIC2022,6538'
database = 'SAT-Nomina'
username = 'caarteaga'
password = 'Audi2025'

# Connection configuration
connection_string = (
    "DRIVER={ODBC Driver 18 for SQL Server};"
    f"SERVER={server};"
    f"DATABASE={database};"
    f"UID={username};"
    f"PWD={password};"
    "Encrypt=no;"              # o "Encrypt=yes;TrustServerCertificate=yes;"
)

table = "2024-AECF_0101_Anexo4-Detalle-Percepciones"
receptor_RFC = "SSI220901JS5"

query = f"""
SELECT TOP 4 *
FROM [{table}]
WHERE ReceptorRFC = ?
"""

try:
    conn = pyodbc.connect(connection_string)
    t1 = time.time()
    df = pd.read_sql(query, conn, params=[receptor_RFC])
    print("Tiempo de consulta (pyodbc):", time.time() - t1)
    df.to_excel(f"{table}.xlsx", index=False)
    print(f"Tabla '{table}' guardada con exito!")
    conn.close()

except Exception as e:
    print("Error al conectar o ejecutar consulta:", e)
