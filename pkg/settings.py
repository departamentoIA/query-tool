# settings.py
"""This file uses the 'config.py' file."""
import pyodbc
import pandas as pd
import time
import math
import warnings
from pkg.config import DB_CONFIG

# Global variables ----------------------------------------
percepciones_table = "2024-AECF_0101_Anexo4-Detalle-Percepciones"
deducciones_table = "2024-AECF_0101_Anexo5-Detalle-Deducciones"
log_file = "Valores en percepciones y deducciones.txt"
path_results = "archivos"
catalogo_excel = "catalogo"
MAX_ROWS_PER_TABLE = 600_000              # Maximum number of rows per excel file
# Maximum number of different values in columns 'percepcionClave' or 'deduconClave'
MAX_COLUMN_VALS = 40
# -------------------------------------------------------

receptorRFC_list = input(
    "Escriba los RFCs separados por coma para las consultas: ")
receptorRFC_list = receptorRFC_list.split(",")
# receptorRFC_list = ["IMS421231I45"]
table_list = [percepciones_table, deducciones_table,
              "2024-AECF_0101_Anexo6F-Percepciones",
              "2024-AECF_0101_Anexo7G-Otros-Pagos",
              "2025-1S_AECF_1891_Anexo3C-Nomina"]

# File to write some text
f = open(log_file, "w", encoding="utf-8")

conn_str = (
    f"DRIVER={DB_CONFIG['driver']};"
    f"SERVER={DB_CONFIG['server']};"
    f"DATABASE={DB_CONFIG['database']};"
    f"UID={DB_CONFIG['username']};"
    f"PWD={DB_CONFIG['password']};"
    "Encrypt=no;"
    "TrustServerCertificate=yes;"
)

# To ignore all warnings
warnings.filterwarnings("ignore")
