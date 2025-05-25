import pandas as pd

# load data
df = pd.read_csv("/Users/shwetabambal/Documents/myrepos/war-analytics/war_data.csv",
                 names=["War", "Start Date", "End Date", "Participant", "Location", "Casualties", "Cause", "Effect"],)


# Convert both to datetime
df["Start Date"] = pd.to_datetime(df["Start Date"], errors='coerce')
df["End Date"] = pd.to_datetime(df["End Date"], errors='coerce')

# Create a "Sort Date" that uses Start Date first, then End Date
df["Sort Date"] = df["Start Date"].combine_first(df["End Date"])

# Clean participant names (optional)
df["Participant"] = df["Participant"].astype(str).str.strip()

# Normalize participant names
country_mapping = {
    "Dominion of India": "India",
    "India": "India",
    "Dominion of Pakistan": "Pakistan",
    "Pakistan Armed Forces": "Pakistan",
    "Pakistan": "Pakistan",
    "United States of America": "USA",
    "United States": "USA",
    "Soviet Union": "Russia",
    "Russian Empire": "Russia",
    "Russia": "Russia",
    "People's Republic of China": "China",
    "China": "China",
    "United Kingdom": "Europe",
    "France": "Europe",
    "Germany": "Europe",
    "British Indian Army": "India",
    "East India Company": "Europe",
    "Dutch East India Company": "Europe",
    "Dutch West India Company": "Europe",
    "Danish India": "Europe"
}

# Apply mapping
df["Normalized Participant"] = df["Participant"].map(country_mapping)

# Sort by that combined date
df_sorted = df.sort_values(by="Sort Date").drop(columns="Sort Date").reset_index(drop=True)


# Save to CSV
df_sorted.to_csv("/Users/shwetabambal/Documents/myrepos/war-analytics/war_data_sorted.csv", index=False)
print("Data sorted by Start Date and saved successfully.")






# Wars fought by India and Pakistan
#df_india_pakistan = df_sorted[df_sorted["Participant"].str.contains("India|Pakistan", na=False)]
#df_india_pakistan.to_csv("/Users/shwetabambal/Documents/myrepos/war-analytics/india_pakistan_wars.csv", index=False)

# Wars fought by USA and Russia
#df_usa_russia = df_sorted[df_sorted["Participant"].str.contains("United States|Russia", na=False)]
#df_usa_russia.to_csv("/Users/shwetabambal/Documents/myrepos/war-analytics/usa_russia_wars.csv", index=False)
