# config.py
"""This file calls the '.env' file, which has the following content:
DB_SERVER=10.0.14.27\\PRODMIXTIC2022,6538
DB_DATABASE=SAT-Nomina
DB_USERNAME=caarteaga
DB_PASSWORD=your_password
DB_DRIVER={ODBC Driver 18 for SQL Server}
The '.env' file is not provided in this repository.
"""

from dotenv import load_dotenv
import os
import sys
from pathlib import Path


def load_env():
    # Si está congelado (exe):
    if getattr(sys, 'frozen', False):
        base_path = Path(sys._MEIPASS)
    else:
        base_path = Path(__file__).resolve().parent

    env_path = base_path / ".env"
    load_dotenv(env_path)


load_env()

DB_CONFIG = {
    "server": os.getenv("DB_SERVER"),
    "database": os.getenv("DB_DATABASE"),
    "username": os.getenv("DB_USERNAME"),
    "password": os.getenv("DB_PASSWORD"),
    "driver": os.getenv("DB_DRIVER"),
}
