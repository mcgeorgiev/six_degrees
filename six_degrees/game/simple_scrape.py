
import requests
import re
from bs4 import BeautifulSoup
import csv

def get_more(end):
    url = "https://simple.wikipedia.org" + end
    r = requests.get(url)
    data = r.text
    soup = BeautifulSoup(data, 'html.parser')
    old_file = open('simple.csv', 'a')
    writer = csv.writer(old_file)
    for li_element in soup.ul:
        try:
            writer.writerow([li_element.find('a').getText()])

        except:
            pass
    old_file.close()

    pages = soup.find_all('a', title='Special:AllPages', href=True)
    end = None
    for page in pages:
        if u"Next" in page.get_text():
            end = page["href"]
            break
    if end is not None:
        return get_more(end)
    else:
        return None



def scrape():

    get = "https://simple.wikipedia.org/w/index.php?title=Special:AllPages&from=%21%21%21&hideredirects=1"
    #print get
    r = requests.get(get)
    data = r.text
    soup = BeautifulSoup(data, 'html.parser')

    pages = soup.find_all('a', title='Special:AllPages', href=True)
    for page in pages:
        if u"Next" in page.get_text():
            end = page["href"]
            break

    new_file = open('simple.csv', 'w')
    writer = csv.writer(new_file)
    for li_element in soup.ul:
        try:
            writer.writerow([li_element.find('a').getText()])
        except:
            pass
    new_file.close()
    get_more(end)




if __name__== "__main__":
    scrape()
