import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import calendar
# TODO rename shapeSightingsMonth to something more appropriate.
# TODO Combine shapeSightingsYear and shapeSightingsMonth by adding shapes to shapeSightingsMonth.
# TODO It looks like the Function year() is not used -- delete it
# TODO move lines 14-16 to dataframe_cleaner.py
# TODO shapeGraph needs axis lables and needs the y-lables cleaned.

pd.set_option('display.expand_frame_repr', False)

ufoDf = pd.read_csv('ufo_reports.csv')

ufoDf['Month'] = ufoDf['Month'].apply(lambda x: calendar.month_name[x])
ufoDf['Shape'] = ufoDf['Shape'].fillna(value='EMPTY')
ufoDf['Shape'] = ufoDf['Shape'].str.upper()

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
    """
    Takes countShapes() as the input dataframe.
    Generates a bar graph with a list of shapes on the y-axis and their frequency of the x-axis.
    """
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
    """
    The national UFO reporting center opened in 1974. I assume that only the data from 1974
    will be comprehensive enough to be useful. Only collect the years starting then.
    """
    yearDf = ufoDf.Year.value_counts()
    yearDf = yearDf.sort_index(ascending=False)
    yearDf = yearDf.iloc[:-75]
    yearDf = yearDf.reset_index()
    yearDf.columns = ['Year', 'Number of Sightings']
    return yearDf

def sightigsByYearGraph(dataframe):
    plt_x = dataframe.Year
    plt_y = dataframe['Number of Sightings']
    plt.plot(plt_x, plt_y)
    plt.show()

shapeSightingsYear = ufoDf.groupby(['Year', 'Shape']).agg(len) # use .loc[xxxx] to call for a specific year
shapeSightingsYear = shapeSightingsYear.drop(['Unnamed: 0', 'Date', 'Duration', 'Summary', 'Month', 'Time', 'State',
                                              'Posted'], axis=1)
shapeSightingsYear.columns = ['Number of Occurances']
shapeSightingsYear = shapeSightingsYear .unstack(fill_value=0)
shapeSightingsYear = shapeSightingsYear.stack()

shapeSightingsMonth = ufoDf.groupby(['Year', 'Month', 'Date']).agg(len)
shapeSightingsMonth = shapeSightingsMonth.drop(['Duration', 'Summary','Time', 'State',
                                                'City', 'Shape', 'Posted'], axis=1)
shapeSightingsMonth.columns = ['Number of Occurances']
shapeSightingsMonth = shapeSightingsMonth.unstack(fill_value=0)
shapeSightingsMonth = shapeSightingsMonth.stack()
#shapeSightingsMonth['Number of Occurances'][2017, "August"]

def makeUfoGraphYear():
    """
    This function will show how the frequency of ufo sightings has changed of time as a
    function of its shape.
    """

    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)

    for shape in ufoDf.Shape.unique():
        xAxis = shapeSightingsYear['Number of Occurances'][:, shape][-45:].index
        yAxis = shapeSightingsYear['Number of Occurances'][:, shape][-45:].values
        ax.set_title('Number of UFO Sightings by Shape (1974-present)')
        ax.set_xticks(np.arange(1974, 2019, 4))
        plt.plot(xAxis, yAxis, label=shape)
    ax.legend(loc=2, fontsize='x-small')
    ax.set_xlabel('Year')
    ax.set_ylabel('Number of Sightings')
    plt.show()