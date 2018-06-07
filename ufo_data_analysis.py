import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


pd.set_option('display.expand_frame_repr', False)

ufoDf = pd.read_csv('ufo_reports.csv')

ufoDf['Shape'] = ufoDf['Shape'].fillna(value='EMPTY')
ufoDf['Shape'] = ufoDf['Shape'].str.upper()
#ufoDf.Shape.str.upper().unique() # I need to drop NaN from the column values


ufoShapeArray = []
for i in ufoDf.Shape.str.upper().unique():
    ufoShapeArray.append(i)

def countShapes():
    shapeCounts = pd.DataFrame(index=[ufoShapeArray], columns=['Count'])
    for i in ufoShapeArray:
        shapeCounts.loc[i] = ufoDf.Shape.str.contains(i).sum()
    shapeCounts = shapeCounts.drop(['EMPTY', 'TRIANGULAR', 'HEXAGON', 'FLARE', 'CRESCENT', 'DELTA', 'PYRAMID', 'ROUND', 'DOME', 'CHANGED'])
    return shapeCounts

def shapeGraph(dataframe):

    fig, ax = plt.subplots()
    shapes = dataframe.index.values
    ypos = np.arange(len(dataframe.index.values))
    num_reports = dataframe.Count.values

    ax.barh(ypos, num_reports, align='center', color='green')
    ax.set_yticks(ypos)
    ax.set_yticklabels(shapes)
    ax.invert_yaxis()

    plt.show()


def years():
    yearDf = ufoDf.Year.value_counts()
    yearDf = yearDf.sort_index(ascending=False)
    yearDf = yearDf.iloc[:-75] # The national UFO reporting center opened in 1974 only collect the years starting then
    yearDf = yearDf.reset_index()
    yearDf.columns = ['Year', 'Number of Sightings']
    return yearDf

def sightigsByYearGraph(dataframe):
    plt_x = dataframe.Year
    plt_y = dataframe['Number of Sightings']
    plt.plot(plt_x, plt_y)
    plt.show()


#test
#sightigsByYearGraph(years())
#shapeGraph(countShapes())

shapeSightingsYear = ufoDf.groupby(['Year', 'Shape']).agg(len) # use .loc[xxxx] to call for a specific year
shapeSightingsYear = shapeSightingsYear.drop(['Unnamed: 0', 'Date', 'Duration', 'Summary', 'Month', 'Time', 'State', 'Posted'], axis=1)
shapeSightingsYear.columns = ['Number of Occurances']
# find the number of light sightings in 1998
#shapeSightingsYear.loc[1998, 'LIGHT'].values

def findSightingsPerYear():
    for year in years().Year:
        for item in ufoShapeArray:
                print(shapeSightingsYear.loc[year,item])