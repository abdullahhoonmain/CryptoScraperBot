import sys

# Ensure output is encoded in utf-8 for printing
sys.stdout.reconfigure(encoding='utf-8')
from bs4 import BeautifulSoup
import requests
import csv

# Open CSV outside the page loop, so all data is written into one file
with open("coins_data.csv", "w", newline="", encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(["Name", "Value"])  # Write header

    # Loop through pages 1 to 100
    for page in range(1, 101):
        url = f"https://coinmarketcap.com/?page={page}"  # Corrected URL format
        result = requests.get(url).text
        doc = BeautifulSoup(result, "html.parser")

        tbody = doc.tbody
        trs = tbody.contents

        for tr in trs:
            # Extract the coin name (first case: <p> or second case: <span> inside <a>)
            name_tag = tr.find('p', class_='coin-item-name')  # For the first few rows
            if not name_tag:  # For the other rows
                name_tag = tr.find('a', class_='cmc-link').find('span', text=True)
            name = name_tag.get_text(strip=True) if name_tag else "N/A"
            
            # Extract the value
            value_tag = tr.find('span', string=lambda s: s and s.startswith('$'))  # Case 1
            if not value_tag:
                td_tags = tr.find_all('td')
                for td in td_tags:  # Look through all <td> elements for a value
                    if '$' in td.get_text():
                        value_tag = td
                        break  # Stop at the first match
            value = value_tag.get_text(strip=True) if value_tag else "N/A"
            
            # Write name and value to CSV
            writer.writerow([name, value])
            print(f"Page {page} - Name: {name}, Value: {value}")

print("Data from all 100 pages has been written to coins_data.csv")
