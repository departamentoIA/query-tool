#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
File:           sqlalchemy_sqlserver_example.py
Author:         Antonio Arteaga
Last Updated:   2025-11-26
Version:        1.0
Description:
Simple example of connection to a DB by using SQLServer, sqlalchemy and Python.
The query result is saved in an excel file.
Dependencies:   pandas==2.3.3, openpyxl==3.1.5, SQLAlchemy==2.0.44.
Usage:          The sql query has the form:
SELECT TOP 4 *
FROM "2024-AECF_0101_Anexo4-Detalle-Percepciones"
WHERE ReceptorRFC IN ('PEES540914FT3')
"""

import pandas as pd
from sqlalchemy import create_engine
import time

# Parameters to connect to the database
server = '10.0.14.27\\PRODMIXTIC2022,6538'
database = 'SAT-Nomina'
username = 'caarteaga'
password = 'Audi2025'

engine = create_engine(
    f"mssql+pyodbc://{username}:{password}@{server}/{database}?driver=SQL+Server"
)


table = [
    "2024-AECF_0101_Anexo4-Detalle-Percepciones",
    "2024-AECF_0101_Anexo5-Detalle-Deducciones"
]
receptor_RFC = 'PEES540914FT3'

query = f"""
SELECT TOP 4 *
FROM [{table[0]}]
WHERE ReceptorRFC = '{receptor_RFC}'
"""

t1 = time.time()
df = pd.read_sql(query, engine)
print("Tiempo de consulta (sqlalchemy):", time.time() - t1)
df.to_excel(f"{table[0]}.xlsx", index=False)
print(f"Tabla '{table[0]}' guardada con éxito!")
