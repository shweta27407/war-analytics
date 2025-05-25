import requests
import pandas as pd
import json

# SPARQL endpoint
url = 'https://query.wikidata.org/sparql'

# SPARQL query
query = """
SELECT ?war ?warLabel ?startDate ?endDate ?participantLabel ?locationLabel ?casualties ?causeLabel ?effectLabel WHERE {
  ?war wdt:P31 wd:Q198.  # must be an instance of war
  OPTIONAL { ?war wdt:P580 ?startDate. }
  OPTIONAL { ?war wdt:P582 ?endDate. }
  OPTIONAL { ?war wdt:P710 ?participant. }       # participant (country, person)
  OPTIONAL { ?war wdt:P276 ?location. }          # location
  OPTIONAL { ?war wdt:P1120 ?casualties. }       # number of victims
  OPTIONAL { ?war wdt:P828 ?cause. }             # cause
  OPTIONAL { ?war wdt:P1542 ?effect. }           # effects the war has
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

with open('response.json', 'w') as f:
    json.dump(data, f, indent=2)


# Parse data into rows
results = data['results']['bindings']
rows = []
for r in results:
    rows.append({
        'War': r.get('warLabel', {}).get('value', ''),
        'Start Date': r.get('startDate', {}).get('value', ''),
        'End Date': r.get('endDate', {}).get('value', ''),
        'Participant': r.get('participantLabel', {}).get('value', ''),
        'Location': r.get('locationLabel', {}).get('value', ''),
        'Casualties': r.get('casualties', {}).get('value', ''),
        'Cause': r.get('causeLabel', {}).get('value', ''),
        'Effect': r.get('effectLabel', {}).get('value', '')
    })

# Create DataFrame
df = pd.DataFrame(rows)

# Preview
print(df.head())

# Save DataFrame to CSV
df.to_csv('/Users/shwetabambal/Documents/myrepos/war-analytics/war_data.csv', index=False)

print("Data has been saved to 'war_data.csv'")