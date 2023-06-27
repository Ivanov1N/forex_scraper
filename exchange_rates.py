import requests
from bs4 import BeautifulSoup
import pandas as pd

# Setting up BeautifulSoup
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36'
    }

url = 'https://bnb.bg/Statistics/StInterbankForexMarket/index.htm'
req = requests.get(url, headers)
soup = BeautifulSoup(req.content, 'html.parser')
table_box = soup.find('div', class_='table_box')
header_cells = table_box.find('tr', class_='header_cells_last')
data_cells = table_box.tbody.find_all('tr')

# Extracts columns names
def collect_col_names():
    column_names = []
    for header in header_cells:
        h = header.text.strip()
        if h != '':
            column_names.append(h)
    column_names = ['код на валута', 'валутна единица'] + column_names
    return column_names

# Extracts exchange rates data
def collect_data():
    data = []
    for row in data_cells[:len(data_cells) - 1]:
        data_row = [cell.get_text(strip=True) for cell in row.find_all(['th', 'td'])]
        data.append(data_row)
    return data

# Creates the newly extracted currencies table
currency_table_new = pd.DataFrame(collect_data(), columns=collect_col_names())

# Checks for an existing csv/old table
try:
    currency_old_table = pd.read_csv('currency_table.csv', encoding='utf-8-sig', index_col=False, dtype='object',
                                     keep_default_na=False)
except FileNotFoundError:
    currency_old_table = pd.DataFrame()

# Creates new CSV or overwrites the old one, if there are differences between the old forex data and the new one
if currency_old_table.empty:
    currency_table_new.to_csv('currency_table.csv', encoding='utf-8-sig', index=False)
    print("New CSV file generated!")
else:
    currency_old_table.columns = collect_col_names()
    if currency_table_new.equals(currency_old_table):
        print('Tables are equal!')
        pass
    else:
        currency_table_new.to_csv('currency_table.csv', encoding='utf-8-sig', index=False)
        print('CSV file was overwritten!')









