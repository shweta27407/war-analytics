import streamlit as st
import pandas as pd
import altair as alt

# Load Data
@st.cache_data
def load_data():
    df = pd.read_csv("/Users/shwetabambal/Documents/myrepos/war-analytics/war_data_sorted.csv")
    df['Start Date'] = pd.to_datetime(df['Start Date'], errors='coerce')
    df['End Date'] = pd.to_datetime(df['End Date'], errors='coerce')
    df['Casualties'] = pd.to_numeric(df['Casualties'], errors='coerce')
    return df

df = load_data()

# ----- Sidebar Configuration -----
st.sidebar.header("📌 Filter Options")

# Filter by Country
normalized_countries = sorted(df['Normalized Participant'].dropna().unique())
selected_countries = st.sidebar.multiselect("Select Country", normalized_countries)

# Filter by Time Range (Start or End Year)
all_years = pd.concat([
    df['Start Date'].dropna().dt.year,
    df['End Date'].dropna().dt.year
])
min_year = int(all_years.min())
max_year = int(all_years.max())

selected_year_range = st.sidebar.slider(
    "Select Time Period",
    min_value=min_year,
    max_value=max_year,
    value=(min_year, max_year)
)

# Filter by Keyword in Cause or Effect
search_term = st.sidebar.text_input("Search in Cause/Effect (optional)").strip()

# ----- Apply Filters -----
filtered_df = df.copy()

if selected_countries:
    filtered_df = filtered_df[filtered_df['Normalized Participant'].isin(selected_countries)]

filtered_df = filtered_df[
    filtered_df['Start Date'].dt.year.between(selected_year_range[0], selected_year_range[1])
]

if search_term:
    filtered_df = filtered_df[
        filtered_df['Cause'].fillna('').str.contains(search_term, case=False) |
        filtered_df['Effect'].fillna('').str.contains(search_term, case=False)
    ]

# Calculate Duration
filtered_df['Duration (days)'] = (filtered_df['End Date'] - filtered_df['Start Date']).dt.days

# ----- Title -----
st.title("📜 Historical Wars Dashboard")

# ----- KPIs -----
col1, col2, col3 = st.columns(3)
col1.metric("🧮 Total Wars", filtered_df['War'].nunique())
col2.metric("👥 Unique Participants", filtered_df['Participant'].nunique())
col3.metric("💀 Total Casualties", f"{int(filtered_df['Casualties'].sum()):,}")

# ----- Timeline -----
st.subheader("📅 War Timeline by Start Year")
timeline_df = filtered_df.dropna(subset=['Start Date'])
timeline_counts = timeline_df.groupby(timeline_df['Start Date'].dt.year).size()
st.line_chart(timeline_counts)

# ----- Participants per War -----
st.subheader("👥 Participants per War")
participant_counts = filtered_df.groupby('War')['Participant'].nunique().sort_values(ascending=False)
st.bar_chart(participant_counts)

# ----- Top Countries by War Frequency -----
st.subheader("🌍 Top Participant Countries (by frequency)")
top_participants = filtered_df['Normalized Participant'].value_counts().head(10)
st.bar_chart(top_participants)

# ----- War Duration Distribution -----
st.subheader("⏳ War Duration Distribution")
st.write("Shows the distribution of war lengths in days (where end date is known).")

# Remove NaN durations
duration_data = filtered_df['Duration (days)'].dropna()

# Create a histogram using Altair
if not duration_data.empty:
    hist_df = pd.DataFrame({'Duration (days)': duration_data})
    chart = alt.Chart(hist_df).mark_bar().encode(
        alt.X("Duration (days):Q", bin=alt.Bin(maxbins=30)),
        y='count()',
    ).properties(width=700, height=400)

    st.altair_chart(chart)
else:
    st.info("No duration data available to plot a histogram.")

# ----- Insights -----
st.subheader("🧠 Insights")
if not filtered_df.empty:
    deadliest_war = filtered_df.loc[filtered_df['Casualties'].idxmax()]
    st.write(f"• The deadliest war is **{deadliest_war['War']}** with approximately **{int(deadliest_war['Casualties']):,} casualties**.")
    if not top_participants.empty:
        st.write(f"• **{top_participants.idxmax()}** appeared in the highest number of wars among selected countries.")

# ----- Data Table -----
st.subheader("📊 Filtered War Data")
st.dataframe(filtered_df)

