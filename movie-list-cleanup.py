import pandas as pd
pd.set_option('display.expand_frame_repr', False)

# Read in the CSV and assign it to the variable ufoDf
file = pd.read_csv('ufo movies.csv')
movieDf = pd.DataFrame(file)


df2 = movieDf['Movie'].str[:].str.split(' - ', expand=True) # Split the single column at the - and expand the resulting split strings into their own df column
df2[1] = df2[1].str[:4]  # Strip everything but the first four characters assuming that is the release year and discard everything else.
df2 = df2.dropna(how='all') # drop rows that contain NaN
df2.columns = ['Movie', 'Year', 'Release Date'] # rename the columns

df2.to_csv('clean-movie-list.csv')