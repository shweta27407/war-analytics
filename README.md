# 📜 Historical Wars Dashboard

An end-to-end data engineering project showcasing real-time war analytics using a pipeline that extracts structured data via **SPARQL**, processes and normalizes it, and loads it into a **Streamlit dashboard**.

> 🛠 Project is built With a focus on data pipeline architecture, semantic web querying, and dashboard-based analytics.

---

## 🔍 Project Overview

This project curates, cleans, and visualizes historical war data from 1600 to the present. 

I designed a custom data pipeline using SPARQL to extract semantically linked war data (e.g., from Wikidata), followed by transformations to standardize the dataset for analytics.

The result is an interactive dashboard where users can explore war statistics by country, time period, duration, and impact.

---

## 🧱 Data Engineering Pipeline

### ✅ 1. `data_extractor.py` (SPARQL-based)
- Queries **Wikidata** using SPARQL to retrieve war data including:
  - War names
  - Participants
  - Start/end dates
  - Casualties
  - Locations
  - Causes and effects
- Outputs raw structured data for downstream cleaning

### ✅ 2. `data_transformer.py`
- Parses and standardizes date fields
- Converts numerical values (e.g., casualties) into proper formats
- Normalizes participant names (e.g., merges variants like "USA", "United States")
- Sorts the dataset by start date
- Writes the final cleaned dataset to `war_data_sorted.csv`

### ✅ 3. `data_loader2.py`
- Loads the cleaned CSV (`war_data_sorted.csv`)
- Powers the **Streamlit dashboard** with this data for real-time visualization and filtering

---

## 📊 Dashboard Features 

| Feature                     | Description |
|----------------------------|-------------|
| 🌍 Filter by Country        | Select wars by participant countries |
| 📅 Filter by Time Range     | Select start year range via slider |
| 🔍 Keyword Search           | Search in "Cause" or "Effect" fields |
| 📈 Timeline Chart           | Line chart of wars per start year |
| 👥 Participants per War     | Bar chart showing participation counts |
| 💀 Casualty KPIs            | Total, average, and deadliest war insights |
| ⏳ War Duration Histogram   | Distribution of war lengths in days |

---

## 📦 Dataset

📁 I have hosted this dataset on Kaggle:  
➡️ [**Historical Wars Dataset**](https://www.kaggle.com/datasets/shwetabambal18/historical-wars)

- Source: Extracted using SPARQL queries from Wikidata
- Records: 20000+

---

## 🚀 How to Run

### 1. Install dependencies

```
pip install -r requirements.txt
```
### 2. Run the pipeline

```
python3 data_extractor.py               
python3 data_transfomer.py
python3 data_loader2.py 
```

### 3. Launch the dashboard

```
streamlit run data_loader2.py
```

## Key Highlights

This project demonstrates:
	•	✅ End-to-end pipeline design
	•	✅ SPARQL and semantic data querying skills
	•	✅ Clean transformation logic with custom rules
	•	✅ Dashboard development for real-time insights


##  Possible Extensions

	•	Add geolocation and world map overlays
	•	Store transformed data in a cloud DB (e.g., PostgreSQL, BigQuery)
	•	Schedule SPARQL refreshes with Airflow
	•	Deploy dashboard on Streamlit Cloud
