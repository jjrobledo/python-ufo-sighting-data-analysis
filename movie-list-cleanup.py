import pandas as pd
from imdb import IMDb
import time
from datetime import datetime, date, time, timedelta

pd.set_option('display.expand_frame_repr', False)

# Read in the CSV and assign it to the variable ufoDf
filename = pd.read_csv('ufo movies.csv')
movieDf = pd.DataFrame(filename)
ia = IMDb()



df2 = movieDf['Movie'].str[:].str.split(' - ', expand=True) # Split the single column at the - and expand the resulting split strings into their own df column
df2[1] = df2[1].str[:4]  # Strip everything but the first four characters assuming that is the release year and discard everything else.
df2 = df2.dropna(how='all') # drop rows that contain NaN
df2.columns = ['Movie', 'Year', 'Release Date'] # rename the columns
#df2.to_csv('clean-movie-list.csv')

movieList = []
for index, row in df2.iterrows():
    i = str(row.Movie) + ' (' + str(row.Year) + ')'
    movieList.append(i)


def movieLookup():

    df3 = pd.DataFrame(columns=['Movie', 'Release Date'])
    count = 0
    for movie in movieList:

        try:
            movie_search = ia.search_movie(movie)
            movie_id = movie_search[0].movieID
            movie = ia.get_movie(movie_id)
            df3 = df3.append({'Movie': str(movie), 'Release Date': str(movie['original air date'])}, ignore_index=True)
            count += 1
            print(count)
        except (KeyError, IndexError):
            pass
    print('Done!')
    df3.to_csv('ufo-movie-releases.csv')


#df3 = movieLookup()
filename2 = pd.read_csv('ufo-movie-releases.csv')
df3 = pd.DataFrame(filename2)


df3['Release Date'] = df3['Release Date'].map(lambda x: str(x)[:11]) # strip the date out of the column
df3['Release Date'] = pd.to_datetime(df3['Release Date']) # Change the dtype of the column

df3.to_csv('ufo-movie-releases.csv')


