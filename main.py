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

if __name__ == "__main__":
    print(scrape(URL))
