import requests
import selectorlib

URL = "http://programmer100.pythonanywhere.com/tours/"

# Optional - Adding a header to the requests payload, just so the server
# we are getting the response from thinks that we are a web browser.
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

def scrape(url):
    """Scrape page info from url"""
    response = requests.get(url, headers=HEADERS)
    page_data = response.text
    return page_data

def extract(page_data):
    extractor = selectorlib.Extractor.from_yaml_file("extract.yaml")
    value = extractor.extract(page_data)["tours"]
    return value

def send_email():
    print("Email was sent!")

def store(extracted):
    with open("data.txt", "a", encoding="utf-8") as file:
        file.write(extracted + "\n")

def read(extracted):
    with open("data.txt", "r") as file:
        return file.read()

if __name__ == "__main__":
    while True:
        scraped = scrape(URL)
        extracted = extract(scraped)
        file_content = read(extracted)
        print(extracted)
        if extracted != "No upcoming tours":
            if extracted not in file_content:
                store(extracted)
                send_email()
                break
