import requests
from bs4 import BeautifulSoup
import csv
import hashlib


# Function to download the webpage and extract data
def extract_data():
    url = 'https://bnb.bg/Statistics/StInterbankForexMarket/index.htm'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Convert the soup to a string
    html_string = str(soup)

    # Search for the specified string
    target_string = 'Спот търговия на банките с чуждестранна валута  срещу левове*'
    start_index = html_string.find(target_string)

    if start_index == -1:
        print("String not found. Please inspect the HTML structure and update the script accordingly.")
        return []

    # Extract data_rows from the content after the found string
    data_start_index = start_index + len(target_string)
    data_rows = []

    # Check if there is a table after the target string
    if '<table' in html_string[data_start_index:]:
        # Extract data from the table
        table_start_index = html_string[data_start_index:].find('<table')
        table_end_index = html_string[data_start_index + table_start_index:].find('</table>') + len('</table>')
        table_html = html_string[data_start_index + table_start_index:data_start_index + table_end_index]
        table_soup = BeautifulSoup(table_html, 'html.parser')

        for row in table_soup.find_all('tr')[1:]:
            columns = row.find_all('td')
            data_row = [col.text.strip() for col in columns]
            data_rows.append(data_row)

    return data_rows


# Function to save data to CSV file
def save_to_csv(data_rows):
    # Sort the data before saving to CSV
    print(data_rows)
    print(data_rows[1:-2])
    sorted_data = sorted(data_rows[1:-2], key=lambda x: float(x[7].replace(' ', '')), reverse=True)

    with open('forex_data.csv', 'w', newline='', encoding='utf-8') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerows(sorted_data)


# Function to compare current data with the existing CSV file
def is_data_changed(data_rows):
    current_hash = hashlib.md5(str(data_rows).encode()).hexdigest()

    try:
        with open('forex_data_hash.txt', 'r') as hash_file:
            previous_hash = hash_file.read()
            return current_hash != previous_hash
    except FileNotFoundError:
        return True


# Main script
if __name__ == "__main__":
    # Extract data from the webpage
    extracted_data = extract_data()

    # Check if the data has changed
    if is_data_changed(extracted_data):
        # Save the sorted data to a CSV file
        save_to_csv(extracted_data)

        # Update the hash file with the new hash
        with open('forex_data_hash.txt', 'w') as hash_file:
            hash_file.write(hashlib.md5(str(extracted_data).encode()).hexdigest())

        print("CSV file updated.")
    else:
        print("No changes in data. CSV file not updated.")
