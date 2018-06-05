import pandas as pd
from ufo_scraper import parseLinks
parseLinks(getUfoLinks())

pd.set_option('display.expand_frame_repr', False)

file = pd.read_csv('dataframe.csv')
ufoDf = pd.DataFrame(file)

ufoDf = ufoDf.drop(['Unnamed: 0'], axis=1)
ufoDf.columns = ['Date', 'City', 'State', 'Shape', 'Duration', 'Summary', 'Posted']
ufoDf = ufoDf[ufoDf.Date.str.contains('Date / Time') == False]
x = ufoDf['Date'].str[:].str.split(' ', expand=True)
ufoDf= x.join(ufoDf)
ufoDf = ufoDf.drop(['Date'], axis=1)
ufoDf.columns = ['Date', 'Time', 'City', 'State', 'Shape', 'Duration', 'Summary', 'Posted']
ufoDf.to_csv('ufo_reports.csv')
