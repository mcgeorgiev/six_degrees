# unicode could become a problem

import requests
import re
from bs4 import BeautifulSoup


def get_shortest_path(source, dest):

    get = "http://degreesofwikipedia.com/?a1={0}&linktype=1&a2={1}&skips=&submit=1487686818&currentlang=en".format(
        source, dest)

    r = requests.get(get)
    data = r.text
    soup = BeautifulSoup(data, 'html.parser')
    php_array = soup.pre.get_text()
    print php_array

    regex = "(?<==> )(.*?)(?=\s+)"
    raw_list = re.findall(regex, php_array)
    clean_list = [link.replace("_", " ") for link in raw_list]
    print clean_list
    return clean_list


if __name__== "__main__":
    get_shortest_path("hong kong", "kangaroo")
