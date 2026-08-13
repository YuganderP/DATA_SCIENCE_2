import requests
from bs4 import BeautifulSoup

def get_page(url):
    response=requests.get(url)
    soup=BeautifulSoup(response.content,'html.parser')
    # print(soup)
    sample=(soup.find_all(class_="quote"))
    print()
    # print(soup.find('a'))
    print()
    # print(soup.find(id="copyright"))
    print()
    quote_span=sample[0].find("span",class_="text")
    print(quote_span.text)

get_page("https://quotes.toscrape.com/tag/inspirational/")
