import pandas as pd

df = pd.read_csv("/Users/shwetabambal/Documents/myrepos/war-analytics/war_data_sorted.csv")
unique_participant_df = df['Participant'].dropna().unique()
print(unique_participant_df[:20])

normalized_participant_df = df['Normalized Participant']
print(normalized_participant_df.to_list())