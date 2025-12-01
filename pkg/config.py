# config.py
"""This file calls the '.env' file, which has the following content:
DB_SERVER=localHost
DB_DATABASE=SAT-Nomina
DB_USERNAME=caarteaga
DB_PASSWORD=your_password
DB_DRIVER={ODBC Driver 18 for SQL Server}
The '.env' file is not provided in this repository.
"""
from dotenv import load_dotenv
import os

load_dotenv()

DB_CONFIG = {
    "server": os.getenv("DB_SERVER"),
    "database": os.getenv("DB_DATABASE"),
    "username": os.getenv("DB_USERNAME"),
    "password": os.getenv("DB_PASSWORD"),
    "driver": os.getenv("DB_DRIVER"),
}
