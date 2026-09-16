import pandas as pd


def prepare_dates(df: pd.DataFrame) -> pd.DataFrame:
    """Convert the date column to pandas datetime."""

    data = df.copy()

    data["date"] = pd.to_datetime(data["date"])

    return data


RAW_TO_WAREHOUSE_COLUMNS = {
    "time": "date",
    "temperature_2m_mean": "temp_avg",
    "temperature_2m_max": "temp_max",
    "temperature_2m_min": "temp_min",
    "precipitation_sum": "precipitation",
    "relative_humidity_2m_mean": "humidity",
    "wind_speed_10m_mean": "wind_speed",
}


def rename_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Rename raw Open-Meteo columns to warehouse column names."""

    data = df.copy()

    data = data.rename(
        columns=RAW_TO_WAREHOUSE_COLUMNS
    )

    return data


def build_dim_city(
    locations_df: pd.DataFrame
) -> pd.DataFrame:
    """Build the city dimension table."""

    data = locations_df[
        [
            "city",
            "country",
            "latitude",
            "longitude",
        ]
    ].copy()

    data.insert(
        0,
        "city_key",
        range(1, len(data) + 1)
    )

    return data


def attach_city_key(
    df: pd.DataFrame,
    dim_city: pd.DataFrame
) -> pd.DataFrame:
    """Attach city_key to weather data using city name."""

    data = df.copy()

    city_lookup = dim_city[
        [
            "city_key",
            "city",
        ]
    ].copy()

    data = data.merge(
        city_lookup,
        on="city",
        how="left",
        validate="many_to_one",
    )

    if data["city_key"].isna().any():
        raise ValueError(
            "Some weather records could not be matched to dim_city."
        )

    data = data.drop(
        columns=["city"]
    )

    return data


def attach_date_key(
    df: pd.DataFrame,
    dim_date: pd.DataFrame
) -> pd.DataFrame:
    """Attach date_key to weather data using date."""

    data = df.copy()

    date_lookup = dim_date[
        [
            "date",
            "date_key",
        ]
    ].copy()

    date_lookup["date"] = pd.to_datetime(
        date_lookup["date"]
    )

    data["date"] = pd.to_datetime(
        data["date"]
    )

    data = data.merge(
        date_lookup,
        on="date",
        how="left",
        validate="many_to_one",
    )

    if data["date_key"].isna().any():
        raise ValueError(
            "Some weather records could not be matched to dim_date."
        )

    data = data.drop(
        columns=["date"]
    )

    return data

def build_fact_weather(
    df: pd.DataFrame,
    dim_city: pd.DataFrame,
    dim_date: pd.DataFrame
) -> pd.DataFrame:
    """Build the final fact_weather table."""

    data = prepare_dates(df)

    data = rename_columns(data)

    data = attach_city_key(
        data,
        dim_city
    )

    data = attach_date_key(
        data,
        dim_date
    )

    return data