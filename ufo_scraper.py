from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
import pandas as pd


pd.set_option('display.expand_frame_repr', False)


html = urlopen("http://www.nuforc.org/webreports/ndxevent.html")
bsObj = BeautifulSoup(html, 'html.parser')

def getUfoLinks():
    ufoAddressList = []
    for link in bsObj.find_all('a', href=re.compile("(ndxe)(\d{6})(\.html)")):
        linkUrl = "http://www.nuforc.org/webreports/" + (link.attrs['href'])
        ufoAddressList.append(linkUrl)
    return ufoAddressList

def parseLinks(list):
    """"Takes 40-45 minutes to run"""
    df1 = pd.DataFrame()
    count = 0
    for page in list:
        ufoSoup = BeautifulSoup(urlopen(page), 'html.parser')
        ufoTable = ufoSoup.find_all('table')[0]

        for tr in ufoTable.findAll('tr'):
            sightingString = re.sub('<[^>]*>', '', str(tr))
            elementList = sightingString.split('\n')
            df2 = pd.DataFrame(elementList[1:8]).transpose()
            df3 = pd.DataFrame([page[-11:-7], page[-7:-5]]).transpose() # This pulls a better formatted year from the url
            df2 = pd.concat([df2, df3], axis=1) # Add the dataframe with the better formatted year to the df2
            df1 = df1.append(df2) # append df2 to df1 to make the complete dataframe
            count += 1
            print("Scraped %s entries" % (count))




    df1.to_csv('dataframe.csv')




parseLinks(getUfoLinks())
