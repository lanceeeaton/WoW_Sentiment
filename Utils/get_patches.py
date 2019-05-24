from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import requests
import pandas as pd
import csv
from bs4 import BeautifulSoup

write_csv = 'Data\\patch_data.csv'

urls = ['https://wowwiki.fandom.com/wiki/Patches'] # Initialized with this url as it doesn’t fit the pattern 

for x in range(6,0,-1):
  urls.append('https://wowwiki.fandom.com/wiki/Patches/{}.x'.format(x)) # getting all our urls

browser = webdriver.Chrome('G:\\ChromeWebDriver\\chromedriver.exe')

with open(write_csv, 'a', newline='') as csvFile: # adding header 
  writer = csv.writer(csvFile)
  writer.writerow(['Patch','Release Date','Version','Interface','Notes'])

  for url in urls:
    browser.get(url)
    tables = browser.find_elements_by_class_name('sortable')
    for table in tables:
      soup = BeautifulSoup(table.get_attribute('innerHTML'), 'html.parser')
      rows = soup.select('tbody tr')
      for row in rows:
        cells = row.select('td')
        all_cell_values = []
        for cell in cells:
          notes = cell.find_all('li')
          if len(notes) == 0:
            all_cell_values.append(cell.text.strip())
          else:
            notes = [note.text.strip() for note in notes]
            all_cell_values.append(notes)

        writer.writerow(all_cell_values)

browser.close()


