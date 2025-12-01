# settings.py
"""This file uses the 'config.py' file."""
import pyodbc
import pandas as pd
import time
import math
import warnings
from pkg.config import DB_CONFIG

# All tables and all RFCs to perform the queries
percepciones_table = "2024-AECF_0101_Anexo4-Detalle-Percepciones"
deducciones_table = "2024-AECF_0101_Anexo5-Detalle-Deducciones"
log_file = "Valores en percepciones y deducciones.txt"
path_results = "archivos"
# catalogo_excel = "catalogo.xlsx"
MAX_ROWS_PER_TABLE = 6              # Maximum number of rows per excel file
receptorRFC_list = input(
    "Escriba los RFCs separados por coma para las consultas: ")
receptorRFC_list = receptorRFC_list.split(",")
# receptorRFC_list = ["IMS421231I45"]

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
