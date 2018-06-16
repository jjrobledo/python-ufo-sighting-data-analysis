import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import calendar
# TODO Combine shapeSightingsYear and shapeSightingsMonth by adding shapes to shapeSightingsMonth.
# TODO move lines 14-16 to dataframe_cleaner.py

pd.set_option('display.expand_frame_repr', False)

ufoDf = pd.read_csv('ufo_reports.csv')

#ufoDf['Month'] = ufoDf['Month'].apply(lambda x: calendar.month_name[x])
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
    # TODO fix the formatting of the names.
    """
    Takes countShapes() as the input dataframe.
    Generates a bar graph with a list of shapes on the y-axis and their frequency of the x-axis.

    :param dataframe:
    :return:
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

    :return:
    """
    yearDf = ufoDf.Year.value_counts()
    yearDf = yearDf.sort_index(ascending=False)
    yearDf = yearDf.iloc[:-75]
    yearDf = yearDf.reset_index()
    yearDf.columns = ['Year', 'Number of Sightings']
    return yearDf

def sightigsByYearGraph(dataframe):
    """
    Plot the frequency of UFO sightings by shape

    :param dataframe: years()
    :return:
    """
    plt_x = dataframe.Year
    plt_y = dataframe['Number of Sightings']
    plt.plot(plt_x, plt_y)
    plt.show()

def sightingsByShape():
    # TODO drop empty sightings from the list
    # TODO consolidate some of tha shapes that are obviously the same triangle/triangular
    """
    This function will show how the frequency of ufo sightings has changed of time as a
    function of its shape.

    :return:
    """
    df = ufoDf[~ufoDf['Shape'].isin(['EMPTY'])]
    df1 = df.groupby(['Year', 'Shape']).agg(len)  # use .loc[xxxx] to call for a specific year
    df1 = df1.drop(['Unnamed: 0', 'Date', 'Duration', 'Summary', 'Month', 'Time', 'State',
                                                  'Posted'], axis=1)
    df1.columns = ['Number of Occurances']
    df1 = df1.unstack(fill_value=0)
    df1 = df1.stack()

    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)

    for shape in df.Shape.unique():
        xAxis = df1['Number of Occurances'][:, shape][-45:].index
        yAxis = df1['Number of Occurances'][:, shape][-45:].values
        ax.set_title('Number of UFO Sightings by Shape (1974-present)')
        ax.set_xticks(np.arange(1974, 2019, 4))
        plt.plot(xAxis, yAxis, label=shape)
    ax.legend(loc=2, fontsize='x-small')
    ax.set_xlabel('Year')
    ax.set_ylabel('Number of Sightings')
    plt.show()

    # months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']


def annualHeatmap():
    # TODO change the names on the y axis to month names
    """


    :return:
    """
    df2 = ufoDf.groupby(['Year', 'Month', 'Date', 'Shape']).agg(len)
    df2 = df2.drop(['Duration', 'Summary', 'Time', 'State',
                                                    'City', 'Posted'], axis=1)
    df2.columns = ['Number of Occurances']
    df2 = df2.unstack(fill_value=0)
    df2 = df2.stack()

    df3 = df2.groupby(['Year', 'Month', 'Date']).sum()
    df3 = df3.groupby(['Month', 'Date']).mean()
    df3 = df3.reset_index()
    df3 = df3.pivot('Month', 'Date', 'Number of Occurances')
    grid_kws = {"height_ratios": (.9, .05), "hspace": .3}
    f, (ax, cbar_ax) = plt.subplots(2, gridspec_kw=grid_kws)
    cbar_ax.set_title('Number of Sightings')
    ax = sns.heatmap(df3, vmin=5, vmax=16, square=True, linewidth=0.3, ax=ax, cbar_ax=cbar_ax,
                     cbar_kws={"orientation": "horizontal"})
    plt.show()

def movieSightings(year, month, daterange):
    df2 = ufoDf.groupby(['Year', 'Month', 'Date', 'Shape']).agg(len)
    df2 = df2.drop(['Duration', 'Summary', 'Time', 'State',
                                                    'City', 'Posted'], axis=1)
    df2.columns = ['Number of Occurances']
    df2 = df2.unstack(fill_value=0)
    df2 = df2.stack()

    return df2.loc[year]['Number of Occurances'][month].loc[daterange].sum()