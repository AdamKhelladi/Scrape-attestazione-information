# Scrape attestazione.net:

import requests
from bs4 import BeautifulSoup as bs
import pandas as pd

def attestazione_info(page_number):

  url = f"https://attestazione.net/SoaEngine?Page={page_number}"

  html = requests.get(url).text 
  soup = bs(html, "html.parser")

  records = soup.find_all("tr")

  master_list = []

  for record in records[1:]: 
    denominazione = record.find("a", {"class": "text-info"}).text

    link = record.find("a", {"class": "text-info"}).get("href")
    link = "https://attestazione.net/"+link
    
    codice_fiscale = record.find("td").find_next_sibling().text

    indirizzo = record.find("td").find_next_sibling().find_next_sibling().text  

    info = {
      "Denominazione": denominazione,
      "Link": link,
      "Codice Fiscale": codice_fiscale,
      "indirizzo": indirizzo
    }

    master_list.append(info)

  df = pd.DataFrame(master_list)
  df.to_csv("info.csv", index=False)
  print("File Created.")

# page_number = 50
for page_number in range(1, 6): # The site contain 1474 page, so just make it 'range(1, 1474+1)' to scrape all data
  attestazione_info(page_number)