from pathlib import Path

import pandas as pd

from src.database import run_query


# ============================================================
# Paths
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent
ANALYTICS_DIR = BASE_DIR / "data" / "analytics"

ANALYTICS_DIR.mkdir(parents=True, exist_ok=True)


# ============================================================
# Generic Analytics Runner
# ============================================================

def run_analytics_query(sql, filename):
    df = run_query(sql, as_dataframe=True)

    output_path = ANALYTICS_DIR / filename
    df.to_csv(output_path, index=False)

    return df


# ============================================================
# 01. PRECIPITATION ANALYSIS
# ============================================================

def precipitation_by_city():
    sql = """
    SELECT
        c.city,
        ROUND(SUM(f.precipitation), 2) AS total_precipitation,
        SUM(
            CASE
                WHEN f.precipitation > 0 THEN 1
                ELSE 0
            END
        ) AS rainy_days
    FROM fact_weather f
    JOIN dim_city c
        ON f.city_key = c.city_key
    GROUP BY c.city, c.city_key
    ORDER BY total_precipitation DESC
    """

    return run_analytics_query(
        sql,
        "01_precipitation_by_city.csv"
    )


def precipitation_by_month():
    sql = """
    SELECT
        d.month,
        d.month_name,
        ROUND(SUM(f.precipitation), 2) AS total_precipitation,
        SUM(
            CASE
                WHEN f.precipitation > 0 THEN 1
                ELSE 0
            END
        ) AS rainy_days
    FROM fact_weather f
    JOIN dim_date d
        ON f.date_key = d.date_key
    GROUP BY d.month, d.month_name
    ORDER BY d.month
    """

    return run_analytics_query(
        sql,
        "02_precipitation_by_month.csv"
    )


def rainiest_days():
    sql = """
    SELECT
        c.city,
        c.country,
        d.date,
        f.precipitation
    FROM fact_weather f
    JOIN dim_city c
        ON f.city_key = c.city_key
    JOIN dim_date d
        ON f.date_key = d.date_key
    WHERE f.precipitation > 0
    ORDER BY f.precipitation DESC
    LIMIT 10
    """

    return run_analytics_query(
        sql,
        "03_rainiest_days.csv"
    )


# ============================================================
# 02. TEMPERATURE ANALYSIS
# ============================================================

def temperature_by_city():
    sql = """
    SELECT
        c.city,
        ROUND(AVG(f.temp_avg), 2) AS avg_temperature,
        ROUND(MAX(f.temp_max), 2) AS highest_temperature,
        ROUND(MIN(f.temp_min), 2) AS lowest_temperature
    FROM fact_weather f
    JOIN dim_city c
        ON f.city_key = c.city_key
    GROUP BY c.city, c.city_key
    ORDER BY avg_temperature DESC
    """

    return run_analytics_query(
        sql,
        "04_temperature_by_city.csv"
    )


def hottest_days():
    sql = """
    SELECT
        c.city,
        c.country,
        d.date,
        f.temp_max,
        f.temp_avg
    FROM fact_weather f
    JOIN dim_city c
        ON f.city_key = c.city_key
    JOIN dim_date d
        ON f.date_key = d.date_key
    ORDER BY f.temp_max DESC
    LIMIT 10
    """

    return run_analytics_query(
        sql,
        "05_hottest_days.csv"
    )


def coldest_days():
    sql = """
    SELECT
        c.city,
        c.country,
        d.date,
        f.temp_min,
        f.temp_avg
    FROM fact_weather f
    JOIN dim_city c
        ON f.city_key = c.city_key
    JOIN dim_date d
        ON f.date_key = d.date_key
    ORDER BY f.temp_min ASC
    LIMIT 10
    """

    return run_analytics_query(
        sql,
        "06_coldest_days.csv"
    )


# ============================================================
# 03. SEASONALITY ANALYSIS
# ============================================================

def monthly_temperature():
    sql = """
    SELECT
        d.month,
        d.month_name,
        ROUND(AVG(f.temp_avg), 2) AS avg_temperature,
        ROUND(AVG(f.temp_max), 2) AS avg_max_temperature,
        ROUND(AVG(f.temp_min), 2) AS avg_min_temperature
    FROM fact_weather f
    JOIN dim_date d
        ON f.date_key = d.date_key
    GROUP BY d.month, d.month_name
    ORDER BY d.month
    """

    return run_analytics_query(
        sql,
        "07_monthly_temperature.csv"
    )


def monthly_precipitation():
    sql = """
    SELECT
        d.month,
        d.month_name,
        ROUND(SUM(f.precipitation), 2) AS total_precipitation,
        ROUND(AVG(f.precipitation), 2) AS avg_daily_precipitation
    FROM fact_weather f
    JOIN dim_date d
        ON f.date_key = d.date_key
    GROUP BY d.month, d.month_name
    ORDER BY d.month
    """

    return run_analytics_query(
        sql,
        "08_monthly_precipitation.csv"
    )


def seasonal_summary():
    sql = """
    SELECT
        CASE
            WHEN d.month IN (12, 1, 2) THEN 'Winter'
            WHEN d.month IN (3, 4, 5) THEN 'Spring'
            WHEN d.month IN (6, 7, 8) THEN 'Summer'
            WHEN d.month IN (9, 10, 11) THEN 'Autumn'
        END AS season,

        ROUND(AVG(f.temp_avg), 2) AS avg_temperature,
        ROUND(MAX(f.temp_max), 2) AS highest_temperature,
        ROUND(MIN(f.temp_min), 2) AS lowest_temperature,
        ROUND(SUM(f.precipitation), 2) AS total_precipitation

    FROM fact_weather f
    JOIN dim_date d
        ON f.date_key = d.date_key

    GROUP BY
        CASE
            WHEN d.month IN (12, 1, 2) THEN 'Winter'
            WHEN d.month IN (3, 4, 5) THEN 'Spring'
            WHEN d.month IN (6, 7, 8) THEN 'Summer'
            WHEN d.month IN (9, 10, 11) THEN 'Autumn'
        END

    ORDER BY
        CASE
            WHEN season = 'Winter' THEN 1
            WHEN season = 'Spring' THEN 2
            WHEN season = 'Summer' THEN 3
            WHEN season = 'Autumn' THEN 4
        END
    """

    return run_analytics_query(
        sql,
        "09_seasonal_summary.csv"
    )


# ============================================================
# 04. CITY COMPARISON
# ============================================================

def city_climate_profile():
    sql = """
    SELECT
        c.city,
        c.country,

        ROUND(AVG(f.temp_avg), 2) AS avg_temperature,
        ROUND(MAX(f.temp_max), 2) AS highest_temperature,
        ROUND(MIN(f.temp_min), 2) AS lowest_temperature,

        ROUND(SUM(f.precipitation), 2) AS total_precipitation,

        SUM(
            CASE
                WHEN f.precipitation > 0 THEN 1
                ELSE 0
            END
        ) AS rainy_days,

        ROUND(AVG(f.humidity), 2) AS avg_humidity,
        ROUND(AVG(f.wind_speed), 2) AS avg_wind_speed

    FROM fact_weather f
    JOIN dim_city c
        ON f.city_key = c.city_key

    GROUP BY
        c.city_key,
        c.city,
        c.country

    ORDER BY c.city
    """

    return run_analytics_query(
        sql,
        "10_city_climate_profile.csv"
    )


def city_rankings():
    sql = """
    SELECT
        c.city,

        ROUND(AVG(f.temp_avg), 2) AS avg_temperature,
        ROUND(SUM(f.precipitation), 2) AS total_precipitation,
        ROUND(AVG(f.humidity), 2) AS avg_humidity,

        RANK() OVER (
            ORDER BY AVG(f.temp_avg) DESC
        ) AS temperature_rank,

        RANK() OVER (
            ORDER BY SUM(f.precipitation) DESC
        ) AS precipitation_rank

    FROM fact_weather f
    JOIN dim_city c
        ON f.city_key = c.city_key

    GROUP BY
        c.city_key,
        c.city

    ORDER BY temperature_rank
    """

    return run_analytics_query(
        sql,
        "11_city_rankings.csv"
    )


def humidity_comparison():
    sql = """
    SELECT
        c.city,
        ROUND(AVG(f.humidity), 2) AS avg_humidity,
        MIN(f.humidity) AS minimum_humidity,
        MAX(f.humidity) AS maximum_humidity
    FROM fact_weather f
    JOIN dim_city c
        ON f.city_key = c.city_key
    GROUP BY c.city_key, c.city
    ORDER BY avg_humidity DESC
    """

    return run_analytics_query(
        sql,
        "12_humidity_comparison.csv"
    )


# ============================================================
# 05. DATA QUALITY
# ============================================================

def missing_values():
    sql = """
    SELECT 'temp_avg' AS column_name,
           COUNT(*) - COUNT(temp_avg) AS missing_count
    FROM fact_weather

    UNION ALL

    SELECT 'temp_max',
           COUNT(*) - COUNT(temp_max)
    FROM fact_weather

    UNION ALL

    SELECT 'temp_min',
           COUNT(*) - COUNT(temp_min)
    FROM fact_weather

    UNION ALL

    SELECT 'precipitation',
           COUNT(*) - COUNT(precipitation)
    FROM fact_weather

    UNION ALL

    SELECT 'humidity',
           COUNT(*) - COUNT(humidity)
    FROM fact_weather

    UNION ALL

    SELECT 'wind_speed',
           COUNT(*) - COUNT(wind_speed)
    FROM fact_weather
    """

    return run_analytics_query(
        sql,
        "13_missing_values.csv"
    )


def duplicate_records():
    sql = """
    SELECT
        city_key,
        date_key,
        COUNT(*) AS record_count
    FROM fact_weather
    GROUP BY city_key, date_key
    HAVING COUNT(*) > 1
    ORDER BY record_count DESC
    """

    return run_analytics_query(
        sql,
        "14_duplicates.csv"
    )


def data_validity():
    sql = """
    SELECT
        'negative_precipitation' AS validation_type,
        COUNT(*) AS invalid_count
    FROM fact_weather
    WHERE precipitation < 0

    UNION ALL

    SELECT
        'negative_wind_speed',
        COUNT(*)
    FROM fact_weather
    WHERE wind_speed < 0

    UNION ALL

    SELECT
        'humidity_out_of_range',
        COUNT(*)
    FROM fact_weather
    WHERE humidity < 0 OR humidity > 100

    UNION ALL

    SELECT
        'min_temperature_above_max',
        COUNT(*)
    FROM fact_weather
    WHERE temp_min > temp_max
    """

    return run_analytics_query(
        sql,
        "15_data_validity.csv"
    )


def coverage():
    sql = """
    SELECT
        c.city,
        MIN(d.date) AS first_date,
        MAX(d.date) AS last_date,
        COUNT(DISTINCT d.date) AS number_of_days
    FROM fact_weather f
    JOIN dim_city c
        ON f.city_key = c.city_key
    JOIN dim_date d
        ON f.date_key = d.date_key
    GROUP BY c.city_key, c.city
    ORDER BY c.city
    """

    return run_analytics_query(
        sql,
        "16_coverage.csv"
    )


# ============================================================
# RUN ALL ANALYTICS
# ============================================================

def run_all_analytics():
    results = {}

    analytics = {
        "01_precipitation_by_city": precipitation_by_city,
        "02_precipitation_by_month": precipitation_by_month,
        "03_rainiest_days": rainiest_days,
        "04_temperature_by_city": temperature_by_city,
        "05_hottest_days": hottest_days,
        "06_coldest_days": coldest_days,
        "07_monthly_temperature": monthly_temperature,
        "08_monthly_precipitation": monthly_precipitation,
        "09_seasonal_summary": seasonal_summary,
        "10_city_climate_profile": city_climate_profile,
        "11_city_rankings": city_rankings,
        "12_humidity_comparison": humidity_comparison,
        "13_missing_values": missing_values,
        "14_duplicates": duplicate_records,
        "15_data_validity": data_validity,
        "16_coverage": coverage,
    }

    for name, function in analytics.items():
        results[name] = function()

    return results