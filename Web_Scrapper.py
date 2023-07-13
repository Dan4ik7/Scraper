#This project will scrap the data from the website 999.md and will store the data in PgAdmin database.
#The data will be about rent apartments and will include the following db columns: Location, monthly_Price, Currency, Rooms,
#The code will include regex to filter on 999 website to find only apartments located in Chisinau, rascanovca or Centru.
import requests
from bs4 import BeautifulSoup
import re
import psycopg2



url = 'https://999.md/ro/list/real-estate/apartments-and-rooms?o_33_1=912&applied=1&eo=12900&eo=12912&eo=12885&eo=13859&ef=32&ef=33'


db = psycopg2.connect(
        host="localhost",
        user="cars_999",
        password="password",
        database="999",
        port=5432

    )

table = "apartamente"


response = requests.get(url)
html_content = response.text

#This pattern is for the links of the products, and regex allows us to find all the links that match the pattern
pattern = r"/ro/\d{8}"
links = re.findall(pattern, html_content)

unique_links = set(links)
final_links = ["https://999.md" + link for link in unique_links]


for link in final_links:
    print(link)
    url = link
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')


    def ParentClass(element, parent_class, child_class):
        content = []
        parent_element = element.find(class_=parent_class)
        for child_element in parent_element.find_all(class_=child_class):
            content.append(child_element.get_text().replace("  ", "").rsplit('/n'))
        return content


    deleted = soup.find(class_='adPage__archive-alert')
    name = soup.find(class_='adPage__header')
    price = soup.find(class_='adPage__content__price-feature__prices__price__value')
    curency = soup.find(class_='adPage__content__price-feature__prices__price__currency')
    rulaj = soup.find(class_='adPage__content__features__col grid_7 suffix_1')
    parent = 'adPage__content__features__col grid_7 suffix_1'
    child = 'adPage__content__features__value'

    try:
        rulaj = ParentClass(soup, parent, child)[6][0]
    except IndexError:
        rulaj = 0

    try:
        anul_fabricari = ParentClass(soup, parent, child)[1][0]
    except IndexError:
        anul_fabricari = 0

    try:
        caroserie = ParentClass(soup, parent, child)[4][0]
    except IndexError:
        caroserie = 0



    if deleted is None:
        content = {

            'url': url,
            'name': name.get_text(),
            'price': price.get_text().replace(" ", ''),
            'curency': curency.get_text().replace(" ", ''),
            'rulaj': rulaj,
            'anul_fabricari': anul_fabricari,
            'caroserie': caroserie,
        }
    else:
        content = {

            'url': 'Produsul nu mai este valabil',
            'name': 'Produsul nu mai este valabil',
            'price': 'Produsul nu mai este valabil',
            'curency': 'Produsul nu mai este valabil',
            'rulaj': 'Produsul nu mai este valabil',
            'anul_fabricari': 'Produsul nu mai este valabil',
            'caroserie': 'Produsul nu mai este valabil',
        }

    cursor = db.cursor()

    # Execute SQL command to create the table (if it doesn't exist)
    cursor.execute(
        f"CREATE TABLE IF NOT EXISTS {table} (url VARCHAR(255), name VARCHAR(255), price VARCHAR(10),curency VARCHAR(255), rulaj VARCHAR(255), anul_fabricari VARCHAR(10),caroserie VARCHAR(10))")

    # Execute SQL command to insert data into the table
    query = f"INSERT INTO {table} (url,name,price,curency,rulaj,anul_fabricari,caroserie) VALUES (%s, %s, %s, %s, %s, %s, %s)"
    values = (f"{content['url']}",f"{content['name']}", f"{content['price']}", f"{content['curency']}", f"{content['rulaj']}",
              f"{content['anul_fabricari']}", f"{content['caroserie']}")
    cursor.execute(query, values)

    # Commit changes to the database
db.commit()

    # Close database connection
db.close()






