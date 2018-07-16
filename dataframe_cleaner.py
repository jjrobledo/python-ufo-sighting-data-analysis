import pandas as pd
from datetime import datetime
from geopy.geocoders import GoogleV3
from geopy.exc import GeocoderTimedOut
import ssl

#ssl._create_default_https_context = ssl._create_unverified_context #  need to configure ssl, uncomment for the program to run correctly in the mean time.

pd.set_option('display.expand_frame_repr', False)

# Read in the CSV and assign it to the variable ufoDf
filename = pd.read_csv('./csv/dataframe.csv')
ufoDf = pd.DataFrame(filename)

# Drop an unused column
ufoDf = ufoDf.drop(['Unnamed: 0'], axis=1)

# Rename columns
ufoDf.columns = ['Date', 'City', 'State', 'Shape', 'Duration', 'Summary', 'Posted', 'Year', 'Month']

# Separate date and time and do some cleanup
ufoDf = ufoDf[ufoDf.Date.str.contains('Date / Time') == False]
ufoDfCopy = ufoDf['Date'].str[:].str.split(' ', expand=True) # ufoDfCopy contains two columns - the date has been seperated from time
ufoDf = ufoDfCopy.join(ufoDf) # join the new dataframe to the old dataframe as new columsn
ufoDf = ufoDf.drop(['Date'], axis=1) # Drop the old column that we don't need any longer
ufoDf.columns = ['Date', 'Time', 'City', 'State', 'Shape', 'Duration', 'Summary', 'Posted', 'Year', 'Month']
ufoDf['Day'] = ufoDf['Date'].str.split('/').str[-2] # Remove month an year from date column
ufoDf['Shape'] = ufoDf['Shape'].fillna(value='EMPTY')
ufoDf['Shape'] = ufoDf['Shape'].str.upper()
# ufoDf.Date = pd.to_datetime(ufoDf[['Day', 'Month', 'Year', 'Time']], format='%d%m%y', errors='ignore')
ufoDf.Date = pd.to_datetime(ufoDf[['Year', 'Month', 'Day']], errors='coerce')
# replacements will be used to aggregate shapes that are essentially the same, assuming they are all 3 dimensional objects. e.g. triangle/delta or teardrop/egg
replacements = {'Shape': {'TRIANGULAR': 'TRIANGLE', 'DELTA': 'TRIANGLE', 'TEARDROP': 'OVAL', 'EGG': 'OVAL', 'CIGAR': 'CYLINDER', 'FLASH': 'FLARE', 'CHANGED': 'CHANGING', 'CIRCLE': 'DISK', 'ROUND': 'DISK'}}
ufoDf = ufoDf.replace(replacements)


# Get the lat and long for each city/state reported

latLongDf = pd.DataFrame(columns = ['Lat', 'Long'])
geolocator = GoogleV3(api_key="API_KEY")

# for loop gets the lat and long for each city, state and appends to a new dataframe
for index, row in ufoDf.iterrows():
    try:
        location = geolocator.geocode(str(row.City) + ', ' + str(row.State), timeout=None)
        latLongDf = latLongDf.append({'Lat': str(location.latitude), 'Long': str(location.longitude)}, ignore_index=True)

    except (AttributeError, GeocoderTimedOut):
        latLongDf = latLongDf.append({'Lat': 'NaN', 'Long': 'Nan'}, ignore_index=True)

        pass



# Save the modified dataframe to a new CSV
ufoDf.to_csv('./csv/ufo_reports1.csv')

latLongDf.to_csv('./csv/ll.csv')
