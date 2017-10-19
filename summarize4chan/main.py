'''
USAGE:
no arguments = scrape 4chan.org/trash
1 argument = scrape the given url, unless the argument is '-' (in which case, read from stdin)
'''

import re
import sys

import requests
from bs4 import BeautifulSoup

from html.parser import HTMLParser

class MLStripper(HTMLParser):
    def __init__(self):
        self.reset()
        self.strict = False
        self.convert_charrefs= True
        self.fed = []
    def handle_data(self, d):
        self.fed.append(d)
    def get_data(self):
        return ''.join(self.fed)

def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()


post_url = "https://4chan.org/trash"

if len(sys.argv) > 1:
    post_url = sys.argv[1]

if len(sys.argv) > 1 and sys.argv[1] == "-":
    stdinput = ""
    line = sys.stdin.readline()
    while line:
        stdinput += line
        line = sys.stdin.readline()

    data = stdinput
else:
    r = requests.get(post_url)
    data = r.text

soup = BeautifulSoup(data, "html.parser")

theregex = re.compile(r'https?:\/\/.*?(\s|$)|.*?\.(org|com|net).*?\s', flags=re.MULTILINE)

for div in soup.find_all('blockquote', {'class': 'postMessage'}):
    #line = "".join([str(x) for x in strip_tags(str(div.contents))])
    line = [strip_tags(str(x)) for x in list(div.contents)]
    line = " ".join(line)
    line = theregex.subn('', line)[0]
    print(line)
