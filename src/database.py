import os
from pathlib import Path

import mysql.connector
from dotenv import load_dotenv
import pandas as pd


# ============================================================
# Load .env from the project root
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent
ENV_FILE = BASE_DIR / ".env"

load_dotenv(ENV_FILE)


# ============================================================
# MySQL Connection
# ============================================================

def get_connection():
    """
    Create and return a connection to the MySQL weather warehouse.
    """

    return mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        port=int(os.getenv("DB_PORT", 3306)),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME"),
    )


# ============================================================
# Run SQL Query
# ============================================================

def run_query(sql, as_dataframe=False):
    conn = get_connection()
    try:
        if as_dataframe:
            cursor = conn.cursor()
            cursor.execute(sql)

            rows = cursor.fetchall()
            columns = cursor.column_names

            cursor.close()

            return pd.DataFrame(rows, columns=columns)

        cursor = conn.cursor(dictionary=True)
        cursor.execute(sql)
        results = cursor.fetchall()
        cursor.close()

        return results

    finally:
        conn.close()
    """
    Execute a SQL query and return the results.

    If as_dataframe=True:
        Return a pandas DataFrame.

    Otherwise:
        Return a list of dictionaries.
    """

    conn = get_connection()

    try:

        if as_dataframe:
            return pd.read_sql(sql, conn)

        cursor = conn.cursor(dictionary=True)

        cursor.execute(sql)

        results = cursor.fetchall()

        cursor.close()

        return results

    finally:
        conn.close()


# ============================================================
# Load dim_city
# ============================================================

def load_dim_city(df):
    """
    Load city dimension into dim_city.
    """

    conn = get_connection()

    try:

        cursor = conn.cursor()

        sql = """
        INSERT INTO dim_city
        (
            city_key,
            city,
            country,
            latitude,
            longitude
        )
        VALUES (%s, %s, %s, %s, %s)
        """

        data = [
            (
                int(row["city_key"]),
                row["city"],
                row["country"],
                float(row["latitude"]),
                float(row["longitude"]),
            )
            for _, row in df.iterrows()
        ]

        cursor.executemany(sql, data)

        conn.commit()

    finally:
        cursor.close()
        conn.close()


# ============================================================
# Load dim_date
# ============================================================

def load_dim_date(df):
    """
    Load date dimension into dim_date.
    """

    conn = get_connection()

    try:

        cursor = conn.cursor()

        sql = """
        INSERT INTO dim_date
        (
            date_key,
            date,
            year,
            month,
            month_name
        )
        VALUES (%s, %s, %s, %s, %s)
        """

        data = [
            (
                int(row["date_key"]),
                row["date"],
                int(row["year"]),
                int(row["month"]),
                row["month_name"],
            )
            for _, row in df.iterrows()
        ]

        cursor.executemany(sql, data)

        conn.commit()

    finally:
        cursor.close()
        conn.close()


# ============================================================
# Load fact_weather
# ============================================================

def load_fact_weather(df):
    """
    Load weather fact records into fact_weather.

    weather_id is generated automatically by MySQL.
    """

    conn = get_connection()

    try:

        cursor = conn.cursor()

        sql = """
        INSERT INTO fact_weather
        (
            city_key,
            date_key,
            temp_avg,
            temp_max,
            temp_min,
            precipitation,
            humidity,
            wind_speed
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """

        data = [
            (
                int(row["city_key"]),
                int(row["date_key"]),
                float(row["temp_avg"]),
                float(row["temp_max"]),
                float(row["temp_min"]),
                float(row["precipitation"]),
                int(row["humidity"]),
                float(row["wind_speed"]),
            )
            for _, row in df.iterrows()
        ]

        cursor.executemany(sql, data)

        conn.commit()

    finally:
        cursor.close()
        conn.close()