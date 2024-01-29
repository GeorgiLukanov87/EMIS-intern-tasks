import requests
from bs4 import BeautifulSoup

# Step a: Open the webpage
url = 'https://en.wikipedia.org/wiki/List_of_European_Union_member_states_by_population'
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

# Step b: Extract data from the table
table = soup.find('table', {'class': 'wikitable'})
countries_data = []

for row in table.find_all('tr')[2:]:
    columns = row.find_all('td')
    country = columns[1].text.strip()
    population = int(columns[2].text.replace(',', '').strip())
    countries_data.append({country: {'country_population': population}})

# Step c: Create the countries_dictionary
countries_dictionary = {}

for data in countries_data:
    countries_dictionary.update(data)

# Step d: Calculate total_country_population and country_population_percentage
total_country_population = sum(data['country_population'] for data in countries_dictionary.values())

for country, data in countries_dictionary.items():
    country_percentage = (data['country_population'] / total_country_population) * 100
    data['country_population_percentage'] = round(country_percentage, 1)

for country, cdata in countries_dictionary.items():
    print(country)
    print(cdata)
