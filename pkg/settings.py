# settings.py
import pyodbc
import pandas as pd
import time
import math
import warnings
from pkg.config import DB_CONFIG

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
