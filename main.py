from time import sleep
import requests
import selectorlib
from backend import send_email
import sqlite3

URL = "http://programmer100.pythonanywhere.com/tours/"

# Optional - Adding a header to the requests payload, just so the server
# we are getting the response from thinks that we are a web browser.
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

""" Connecting to the database """
connection = sqlite3.connect("data.db")

def scrape(url):
    """Scrape page info from url"""
    response = requests.get(url, headers=HEADERS)
    page_data = response.text
    return page_data

def extract(page_data):
    extractor = selectorlib.Extractor.from_yaml_file("extract.yaml")
    value = extractor.extract(page_data)["tours"]
    return value

def store(extracted):
    row = extracted.split(",")
    row = [item.strip() for item in row]
    cursor = connection.cursor()
    cursor.execute("INSERT INTO events VALUES(?,?,?)", row)
    connection.commit()

def read(extracted):
    row = extracted.split(",")
    row = [item.strip() for item in row]
    band, city, date = row
    cursor =  connection.cursor()
    cursor.execute("SELECT * FROM events WHERE band=? AND city=? and date=?", (band, city, date))
    rows = cursor.fetchall()
    return rows


if __name__ == "__main__":
    while True:
        sleep(1)
        scraped = scrape(URL)
        extracted = extract(scraped)
        print(extracted)
        if extracted != "No upcoming tours":
            row = read(extracted)
            if not row:
                store(extracted)
                send_email(message="New event found!")
