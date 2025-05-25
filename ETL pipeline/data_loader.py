import pandas as pd
import matplotlib.pyplot as plt

# Load the data
df = pd.read_csv("/Users/shwetabambal/Documents/myrepos/war-analytics/war_data_sorted.csv")

# Filter for selected world powers
selected_powers = ["India", "Pakistan", "USA", "Russia", "China", "Europe"]
filtered_df = df[df["Normalized Participant"].isin(selected_powers)]

# save fitered data to sorted csv
filtered_df.to_csv("/Users/shwetabambal/Documents/myrepos/war-analytics/war_by_super_powers.csv", index=True)


# Count wars by normalized country
war_counts = filtered_df.groupby("Normalized Participant").size().reset_index(name="War Count")

# Sort for better visualization
war_counts = war_counts.sort_values(by="War Count", ascending=False)
print(war_counts)

# Plot
plt.figure(figsize=(10, 6))
plt.bar(war_counts["Normalized Participant"], war_counts["War Count"], color='skyblue')
plt.title("Number of Wars Fought by Major World Powers (Based on Dataset)")
plt.xlabel("Country")
plt.ylabel("Number of Wars")
plt.tight_layout()
plt.show()