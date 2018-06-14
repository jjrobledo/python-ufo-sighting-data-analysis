import pandas as pd
from geopy.geocoders import Nominatim
import ssl

ssl._create_default_https_context = ssl._create_unverified_context

pd.set_option('display.expand_frame_repr', False)

# Read in the CSV and assign it to the variable ufoDf
file = pd.read_csv('dataframe.csv')
ufoDf = pd.DataFrame(file)

# Drop an unused column
ufoDf = ufoDf.drop(['Unnamed: 0'], axis=1)

# Rename columns
ufoDf.columns = ['Date', 'City', 'State', 'Shape', 'Duration', 'Summary', 'Posted', 'Year', 'Month']

# Separate date and time
ufoDf = ufoDf[ufoDf.Date.str.contains('Date / Time') == False]
ufoDfCopy = ufoDf['Date'].str[:].str.split(' ', expand=True) # ufoDfCopy contains two columns - the date has been seperated from time
ufoDf = ufoDfCopy.join(ufoDf) # join the new dataframe to the old dataframe as new columsn
ufoDf = ufoDf.drop(['Date'], axis=1) # Drop the old column that we don't need any longer
ufoDf.columns = ['Date', 'Time', 'City', 'State', 'Shape', 'Duration', 'Summary', 'Posted', 'Year', 'Month']
ufoDf['Date'] = ufoDf['Date'].str.split('/').str[-2] # Remove month an year from date column

# Get the lat and long for each city/state reported

latLongDf = pd.DataFrame(columns = ['Lat', 'Long'])
count = 0
condition = True
while condition == True:
    geolocator = Nominatim()

    for index, row in ufoDf.iterrows():
        try:
            location = geolocator.geocode(str(row.City) + ' ' + str(row.State))
            latLongDf.append({'Lat': str(location.latitude), 'Long': str(location.longitude)}, ignore_index=True)
        except AttributeError:
            condition = False
        print count

# Save the modified dataframe to a new CSV
#ufoDf.to_csv('ufo_reports.csv')
