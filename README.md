# 🌦️ Weather Data Engineering Pipeline

> **From API → Raw Data → Batch Processing → Star Schema → MySQL → SQL Analytics → Power BI**

A portfolio-grade **Data Engineering pipeline** that collects historical weather data for multiple cities, preserves raw API responses, processes the data through monthly checkpoints, transforms it into a dimensional model, loads it into MySQL, and generates analytical datasets ready for business intelligence.

---

## 🏗️ Pipeline Architecture

```text
                    ┌─────────────────┐
                    │   City Names    │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │    Geocoding    │
                    │ Lat / Lon / TZ  │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │   Weather API   │
                    │   Open-Meteo    │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │   Raw JSON      │
                    │  API Responses  │
                    └────────┬────────┘
                             │
                             ▼
              ┌─────────────────────────────┐
              │    Monthly Batch Layer      │
              │                             │
              │ Raw JSON + CSV Checkpoints  │
              └──────────────┬──────────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │      EDA        │
                    │ Quality Checks  │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │ Transformation  │
                    │ Cleaning + Keys │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │   Star Schema   │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │      MySQL      │
                    │ Data Warehouse  │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │  SQL Analytics  │
                    │ 16 Analytical   │
                    │    Datasets     │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │    Power BI     │
                    │ Climate Explorer│
                    └─────────────────┘
```

---

## 🎯 Project Objective

The goal is to build a realistic end-to-end data pipeline rather than simply download weather data.

The project demonstrates how raw API data can move through multiple engineering layers:

* Data acquisition
* Geocoding
* Raw data preservation
* Batch processing
* Checkpointing
* Data validation
* Exploratory analysis
* Transformation
* Dimensional modeling
* Relational data warehousing
* SQL analytics
* Business intelligence

---

## 🌍 Data Coverage

The pipeline currently processes weather data for **9 cities**:

| City     | Country        |
| -------- | -------------- |
| Riyadh   | Saudi Arabia   |
| Salalah  | Oman           |
| Amman    | Jordan         |
| Istanbul | Türkiye        |
| London   | United Kingdom |
| Munich   | Germany        |
| Zurich   | Switzerland    |
| Cairo    | Egypt          |
| Khartoum | Sudan          |

### Dataset

**Period:** January 1 → December 31, 2025

**Records:** 3,285 daily weather records

**Grain:**

```text
One city × one day = one fact record
```

This produces:

```text
9 cities × 365 days = 3,285 records
```

---

## 📦 Data Pipeline

### 1. Geocoding

City names are converted into geographic metadata:

```text
City
 ↓
Latitude
Longitude
Timezone
Country
```

This information becomes the foundation of `dim_city`.

---

### 2. API Extraction

Historical weather data is retrieved from **Open-Meteo**.

Variables include:

* Average temperature
* Maximum temperature
* Minimum temperature
* Precipitation
* Relative hu
