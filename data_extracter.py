import requests
import pandas as pd

# SPARQL endpoint
url = 'https://query.wikidata.org/sparql'

# SPARQL query
query = """
SELECT ?war ?warLabel ?startDate ?endDate ?causeLabel ?participantLabel WHERE {
  ?war wdt:P31 wd:Q198.
  OPTIONAL { ?war wdt:P580 ?startDate. }
  OPTIONAL { ?war wdt:P582 ?endDate. }
  OPTIONAL { ?war wdt:P828 ?cause. }
  OPTIONAL { ?war wdt:P710 ?participant. }
  SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }
}
LIMIT 100000
"""

# Set headers
headers = {
    'User-Agent': 'Shweta-WarDataFetcher/1.0',
    'Accept': 'application/sparql-results+json'
}

# Make request
response = requests.get(url, params={'query': query}, headers=headers)
data = response.json()

# Parse data into rows
results = data['results']['bindings']
rows = []
for r in results:
    rows.append({
        'War': r.get('warLabel', {}).get('value', ''),
        'Start Date': r.get('startDate', {}).get('value', ''),
        'End Date': r.get('endDate', {}).get('value', ''),
        'Cause': r.get('causeLabel', {}).get('value', ''),
        'Participant': r.get('participantLabel', {}).get('value', '')
    })

# Create DataFrame
df = pd.DataFrame(rows)

# Preview
print(df)

# Save DataFrame to CSV
df.to_csv('/Users/shwetabambal/Documents/myrepos/war-analytics/war_data.csv', index=False)

print("Data has been saved to 'war_data.csv'")