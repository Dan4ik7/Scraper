import requests
from bs4 import BeautifulSoup
import psycopg2

# Establish a connection to the PostgreSQL database
conn = psycopg2.connect(
    host="localhost",
    database="your_database_name",
    user="your_username",
    password="your_password",
    port="5432"
)

# Create a cursor object to interact with the database
cur = conn.cursor()

# URL of the website to scrape
url = "https://999.md/ro/list/real-estate/apartments-and-rooms?o_33_1=912&applied=1&eo=12900&eo=12912&eo=12885&eo=13859&ef=32&ef=33"

# Send a GET request to the website
response = requests.get(url)

# Parse the HTML content using BeautifulSoup
soup = BeautifulSoup(response.content, "html.parser")

# Find all the apartment posts on the page
apartment_posts = soup.find_all("div", class_="ads-list-photo-item")

# Iterate over each apartment post
for post in apartment_posts:
    # Extract the necessary information from the post
    location = post.find("span", class_="ads-list-location").text.strip()
    currency = post.find("span", class_="price-currency").text.strip()
    price_per_month = post.find("span", class_="price-value").text.strip()
    rooms = post.find("span", class_="ads-list-rooms").text.strip()
    surface = post.find("span", class_="ads-list-surface").text.strip()

    # Insert the apartment information into the database
    cur.execute(
        "INSERT INTO apartments (location, currency, price_per_month, rooms, surface) "
        "VALUES (%s, %s, %s, %s, %s)",
        (location, currency, price_per_month, rooms, surface)
    )

# Commit the changes and close the database connection
conn.commit()
cur.close()
conn.close()
