import streamlit as st
import pandas as pd

# Load Data
@st.cache_data
def load_data():
    df = pd.read_csv("/Users/shwetabambal/Documents/myrepos/war-analytics/war_data_sorted.csv")
    df['Start Date'] = pd.to_datetime(df['Start Date'], errors='coerce')
    df['End Date'] = pd.to_datetime(df['End Date'], errors='coerce')
    df['Casualties'] = pd.to_numeric(df['Casualties'], errors='coerce')
    return df

df = load_data()

# Title
st.title("📜 Historical Wars Dashboard")

# --------------- Sidebar configuration ---------------

st.sidebar.header("Filter Options")

# filter by time range
min_year = int(df['Start Date'].dropna().dt.year.min())
max_year = int(df['End Date'].dropna().dt.year.max())

selected_year_range = st.sidebar.slider(
    "Select Time Period",
    min_value=min_year,
    max_value=max_year,
    value=(min_year, max_year)
)

# filter by Country (from Normalized Participant column)
st.sidebar.header("Filter by Country")
normalized_countries = sorted(df['Normalized Participant'].dropna().unique())
selected_countries = st.sidebar.multiselect("Select Countries", normalized_countries)


# ------------- Data Filtering ---------------

# Filter data using the selected countries
if selected_countries:
    filtered_df = df[df['Normalized Participant'].isin(selected_countries)]
else:
    filtered_df = df.copy()

# Filter data using the selected year range
filtered_df = filtered_df[
    (filtered_df['Start Date'].dt.year >= selected_year_range[0]) &
    (filtered_df['End Date'].dt.year <= selected_year_range[1])
]

# --------------------------
# Dashboard Display
# --------------------------

# Summary
st.subheader("🔢 Summary")
st.write(f"Total Entries: {filtered_df.shape[0]}")
st.write(f"Unique Wars: {filtered_df['War'].nunique()}")
st.write(f"Unique Participants: {filtered_df['Participant'].nunique()}")

# Timeline Visualization
st.subheader("📅 War Timeline")
timeline_df = filtered_df.dropna(subset=['Start Date'])
timeline_counts = timeline_df.groupby(timeline_df['Start Date'].dt.year).size()
st.line_chart(timeline_counts)

# Participants per War
st.subheader("👥 Participants per War")
participant_counts = filtered_df.groupby('War')['Participant'].nunique().sort_values(ascending=False)
st.bar_chart(participant_counts)

# Display Filtered Table
st.subheader("📊 Filtered War Data")
st.dataframe(filtered_df)