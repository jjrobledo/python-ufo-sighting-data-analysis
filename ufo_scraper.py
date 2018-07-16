from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
import pandas as pd


pd.set_option('display.expand_frame_repr', False)


html = urlopen("http://www.nuforc.org/webreports/ndxevent.html")
bsObj = BeautifulSoup(html, 'html.parser')


def get_ufo_links():
    '''
    Finds links at the NUFORC and saves them to a list
    :return: list of url strings
    '''

    ufo_address_list = []
    for link in bsObj.find_all('a', href=re.compile("(ndxe)(\d{6})(\.html)")):
        link_url = "http://www.nuforc.org/webreports/" + (link.attrs['href'])
        ufo_address_list.append(link_url)
    return ufo_address_list


def parse_links(link_list):
    '''
    follows each link and looks for table data. Table data is then appended to a dataframe and saved./csv/
    as a .csv

    Can take up to an hour to run
    :param link_list:
    :return:
    '''

    df1 = pd.DataFrame()
    count = 0
    for page in link_list:
        ufo_soup = BeautifulSoup(urlopen(page), 'html.parser')
        ufo_table = ufo_soup.find_all('table')[0]

        for tr in ufo_table.findAll('tr'):
            sightings_string = re.sub('<[^>]*>', '', str(tr))
            element_list = sightings_string.split('\n')
            df2 = pd.DataFrame(element_list[1:8]).transpose()
            df3 = pd.DataFrame([page[-11:-7], page[-7:-5]]).transpose()  # This pulls a better formatted year from the url
            df2 = pd.concat([df2, df3], axis=1)  # Add the dataframe with the better formatted year to the df2
            df1 = df1.append(df2)  # append df2 to df1 to make the complete dataframe
            count += 1
            print("Scraped %s entries" % (count))


    df1.to_csv('./csv/dataframe.csv')


parse_links(get_ufo_links())
