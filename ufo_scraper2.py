from urllib.request import urlopen
from bs4 import BeautifulSoup
import pandas as pd

url = "http://www.nuforc.org/webreports/ndxe201805.html"

html = urlopen(url)

soup = BeautifulSoup(html)

print(soup.findAll('tr', limit=2)[1].findAll('a'))