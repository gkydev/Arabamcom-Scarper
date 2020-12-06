import requests
from bs4 import BeautifulSoup
import csv

all_data = []
all_divs = []
#İlk 20 sayfadaki ilanları topla
counter = 0
for page in range(1,11):
    r = requests.get("https://www.arabam.com/ikinci-el/motosiklet?take=50&page=" + str(page))
    bs = BeautifulSoup(r.text,"html.parser")
    divs = bs.find_all("a", class_="listing-text-new")
    #Toplanan ilanları tek tek gez
    for link in divs:
        if counter %2 == 0:
            r = requests.get("https://www.arabam.com/advertDetail/details?id=" + link["href"].split("/")[-1])
            print(r.url)
            bs = BeautifulSoup(r.text,"html.parser")
            #Ürün bilgilerini topla
            first_rows = bs.find_all("span", class_="one-line-overflow font-default-minus")
            second_rows = bs.find_all("span", class_="pl4 one-line-overflow")      
            data = {}
            for row in range(len(first_rows)):
                data[first_rows[row].text] = second_rows[row].text
            r = requests.get("https://www.arabam.com" + link["href"])
            bs = BeautifulSoup(r.text,"html.parser")
            price = bs.find("span", class_="color-red4")
            data["Fiyat"] = price.text.strip(" TL")
            all_data.append(data)
            print(data)
            counter += 1
        else:
            counter += 1
    #Row isimlerini listeye koy
    rows = []
    for rowname in data:
        rows.append(rowname)
    rows.append("Fiyat")
# CSV dosyasına yaz
with open('baskan-data.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(rows)
    for data in all_data:
        row = []
        for key_name in data:
            row.append(data[key_name])
        writer.writerow(row)