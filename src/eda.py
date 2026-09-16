# ============================================================
# Weather Data Pipeline - EDA Module
# ============================================================

import pandas as pd


NUMERIC_COLUMNS = [
    "temp_avg",
    "temp_max",
    "temp_min",
    "precipitation",
    "humidity",
    "wind_speed",
]


# ============================================================
# 1. Dataset Overview
# ============================================================

def dataset_overview(df):
    return {
        "rows": len(df),
        "columns": len(df.columns),
        "cities": df["city"].nunique(),
        "start_date": df["date"].min(),
        "end_date": df["date"].max(),
        "memory_bytes": df.memory_usage(deep=True).sum(),
    }


# ============================================================
# 2. Statistical Summary
# ============================================================

def statistical_summary(df):
    return (
        df[NUMERIC_COLUMNS]
        .describe()
        .round(2)
    )


# ============================================================
# 3. City Temperature Analysis
# ============================================================

def city_temperature_analysis(df):

    return (
        df
        .groupby("city")
        .agg(
            avg_temperature=("temp_avg", "mean"),
            max_temperature=("temp_max", "max"),
            min_temperature=("temp_min", "min"),
        )
        .sort_values(
            "avg_temperature",
            ascending=False
        )
        .round(2)
    )


# ============================================================
# 4. City Precipitation Analysis
# ============================================================

def city_precipitation_analysis(df):

    return (
        df
        .groupby("city")
        .agg(
            total_precipitation=("precipitation", "sum"),
            average_daily_precipitation=(
                "precipitation",
                "mean"
            ),
            rainy_days=(
                "precipitation",
                lambda x: (x > 0).sum()
            ),
        )
        .sort_values(
            "total_precipitation",
            ascending=False
        )
        .round(2)
    )


# ============================================================
# 5. City Environment Analysis
# ============================================================

def city_environment_analysis(df):

    return (
        df
        .groupby("city")
        .agg(
            average_humidity=("humidity", "mean"),
            max_humidity=("humidity", "max"),
            average_wind_speed=("wind_speed", "mean"),
            max_wind_speed=("wind_speed", "max"),
        )
        .sort_values(
            "average_humidity",
            ascending=False
        )
        .round(2)
    )


# ============================================================
# 6. Monthly Analysis
# ============================================================

def monthly_analysis(df):

    data = df.copy()

    data["month"] = data["date"].dt.month

    monthly_temperature = (
        data
        .groupby("month")
        .agg(
            avg_temp=("temp_avg", "mean"),
            max_temp=("temp_max", "max"),
            min_temp=("temp_min", "min"),
        )
        .round(2)
    )

    monthly_precipitation = (
        data
        .groupby("month")
        .agg(
            total_precipitation=("precipitation", "sum"),
            rainy_days=(
                "precipitation",
                lambda x: (x > 0).sum()
            ),
        )
        .round(2)
    )

    monthly_humidity = (
        data
        .groupby("month")["humidity"]
        .mean()
        .round(2)
    )

    monthly_wind = (
        data
        .groupby("month")["wind_speed"]
        .mean()
        .round(2)
    )

    return {
        "temperature": monthly_temperature,
        "precipitation": monthly_precipitation,
        "humidity": monthly_humidity,
        "wind": monthly_wind,
    }


# ============================================================
# 7. Seasonal Analysis
# ============================================================

def seasonal_analysis(df):

    data = df.copy()

    data["month"] = data["date"].dt.month

    data["season"] = data["month"].map({
        12: "Winter",
        1: "Winter",
        2: "Winter",
        3: "Spring",
        4: "Spring",
        5: "Spring",
        6: "Summer",
        7: "Summer",
        8: "Summer",
        9: "Summer",
        10: "Autumn",
        11: "Autumn",
    })

    return (
        data
        .groupby("season")
        .agg(
            avg_temperature=("temp_avg", "mean"),
            max_temperature=("temp_max", "max"),
            min_temperature=("temp_min", "min"),
            precipitation=("precipitation", "sum"),
            humidity=("humidity", "mean"),
            wind_speed=("wind_speed", "mean"),
        )
        .round(2)
    )


# ============================================================
# 8. Outlier Analysis
# ============================================================

def outlier_analysis(df):

    results = []

    for column in NUMERIC_COLUMNS:

        q1 = df[column].quantile(0.25)
        q3 = df[column].quantile(0.75)

        iqr = q3 - q1

        lower_bound = q1 - 1.5 * iqr
        upper_bound = q3 + 1.5 * iqr

        outlier_count = (
            (df[column] < lower_bound) |
            (df[column] > upper_bound)
        ).sum()

        results.append({
            "column": column,
            "q1": q1,
            "q3": q3,
            "iqr": iqr,
            "lower_bound": lower_bound,
            "upper_bound": upper_bound,
            "outlier_count": outlier_count,
        })

    return (
        pd.DataFrame(results)
        .round(2)
    )


# ============================================================
# 9. Correlation Analysis
# ============================================================

def correlation_analysis(df):

    return (
        df[NUMERIC_COLUMNS]
        .corr()
        .round(2)
    )


# ============================================================
# 10. Data Quality Analysis
# ============================================================

def data_quality_analysis(df):

    return {
        "missing_values": df.isna().sum(),
        "duplicate_rows": int(df.duplicated().sum()),
        "invalid_temperature": int(
            (
                (df["temp_min"] > df["temp_avg"]) |
                (df["temp_avg"] > df["temp_max"])
            ).sum()
        ),
        "invalid_humidity": int(
            (
                (df["humidity"] < 0) |
                (df["humidity"] > 100)
            ).sum()
        ),
        "invalid_precipitation": int(
            (df["precipitation"] < 0).sum()
        ),
        "invalid_wind": int(
            (df["wind_speed"] < 0).sum()
        ),
    }


# ============================================================
# 11. Complete EDA Runner
# ============================================================

def run_eda(df, year=None):

    results = {

        "overview":
            dataset_overview(df),

        "statistics":
            statistical_summary(df),

        "city_temperature":
            city_temperature_analysis(df),

        "city_precipitation":
            city_precipitation_analysis(df),

        "city_environment":
            city_environment_analysis(df),

        "monthly":
            monthly_analysis(df),

        "seasonal":
            seasonal_analysis(df),

        "outliers":
            outlier_analysis(df),

        "correlation":
            correlation_analysis(df),

        "data_quality":
            data_quality_analysis(df),
    }

    if year is not None:
        results["year"] = year

    return results