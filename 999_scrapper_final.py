import requests
from bs4 import BeautifulSoup
import re
import psycopg2

# URL of the website to scrape
url = 'https://999.md/ro/list/real-estate/apartments-and-rooms'

# Database connection details
db_host = "localhost"
db_user = "cars_999"
db_password = "password"
db_name = "999"
db_port = 5432

# Table name in the database
table = "apartamente"

# Connect to the database
db = psycopg2.connect(
    host=db_host,
    user=db_user,
    password=db_password,
    database=db_name,
    port=db_port
)

# Create a cursor to execute SQL commands
cursor = db.cursor()

# Execute SQL command to create the table (if it doesn't exist)
cursor.execute(f"CREATE TABLE IF NOT EXISTS {table} (url VARCHAR(255), name VARCHAR(255), price VARCHAR(255), currency VARCHAR(255), surface VARCHAR(255), Phone VARCHAR(255))")

# Send a request to the URL and retrieve the HTML content
response = requests.get(url)
html_content = response.text

# This pattern is for the links of the products, and regex allows us to find all the links that match the pattern
pattern = r"/ro/\d{8}"
links = re.findall(pattern, html_content)

unique_links = set(links)
final_links = ["https://999.md" + link for link in unique_links]


def ParentClass(element, parent_class, child_class):
    content = {}
    parent_element = element.find(class_=parent_class)
    for child_element in parent_element.find_all(class_=child_class):
        text = child_element.get_text().strip()
        if "m²" in text:
            surface = text.replace("m²", "").strip()
            content['Surface'] = surface
    return content


for link in final_links:
    print(link)
    url = link
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    deleted = soup.find(class_='adPage__archive-alert')
    name = soup.find(class_='adPage__header')
    price = soup.find(class_='adPage__content__price-feature__prices__price__value')
    currency = soup.find(class_='adPage__content__price-feature__prices__price__currency')
    Phone = soup.find(class_='js-phone-number-format number-format')

    content = ParentClass(soup, 'adPage__content__features__col', 'adPage__content__features__value')

    if deleted is None:
        content['url'] = url
        content['name'] = name.get_text().strip()
        content['price'] = price.get_text().replace(" ", '').strip() if price else '0'
        content['currency'] = currency.get_text().replace(" ", '').strip() if currency else '0'
        content['Phone'] = Phone.get_text().strip() if Phone else '0'

        # Check if the record with the same URL already exists
        cursor.execute(f"SELECT url FROM {table} WHERE url = %s", (content['url'],))
        existing_record = cursor.fetchone()

        if existing_record:
            # Update the existing record with the new values
            query = f"UPDATE {table} SET name = %s, price = %s, currency = %s, surface = %s, Phone = %s, WHERE url = %s"
            values = (
                content.get('name', ''),
                content.get('price', ''),
                content.get('currency', ''),
                content.get('Surface', '0'),
                content.get('Phone', '0'),
                content.get('url', '')
            )
        else:
            # Insert a new record into the table
            query = f"INSERT INTO {table} (url, name, price, currency, surface, Phone) VALUES (%s, %s, %s, %s, %s, %s)"
            values = (
                content.get('url', ''),
                content.get('name', ''),
                content.get('price', ''),
                content.get('currency', ''),
                content.get('Surface', '0'),
                content.get('Phone', '0')
            )

        # Execute the SQL query with the corresponding values
        cursor.execute(query, values)

# Commit changes to the database
db.commit()

# Close database connection
db.close()
