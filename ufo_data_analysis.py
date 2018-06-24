import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from datetime import timedelta
from datetime import datetime
import datetime as datetime

# TODO Combine shapeSightingsYear and shapeSightingsMonth by adding shapes to shapeSightingsMonth.
# TODO move lines 14-16 to dataframe_cleaner.py

pd.set_option('display.expand_frame_repr', False)

ufoDf = pd.read_csv('ufo_reports.csv')
ufoDf.Date = pd.to_datetime(ufoDf[['Year', 'Month', 'Day']], errors='coerce')

#ufoDf['Month'] = ufoDf['Month'].apply(lambda x: calendar.month_name[x])


def shapeGraph():
    """
    Generates a bar graph with a list of shapes on the y-axis and their frequency of the x-axis.

    :return: graph
    """
    ufoShapeArray = []
    for i in ufoDf.Shape.str.upper().unique():
        ufoShapeArray.append(i)

    shapeCounts = pd.DataFrame(index=[ufoShapeArray], columns=['Count'])
    for i in ufoShapeArray:
        shapeCounts.loc[i] = ufoDf.Shape.str.contains(i).sum()
    shapeCounts = shapeCounts.drop(['EMPTY', 'HEXAGON', 'CRESCENT','PYRAMID', 'DOME']) # Remove useless values
    shapeCounts = shapeCounts.reset_index()
    shapeCounts.columns = ['Shape', 'Count']
    shapes = shapeCounts.Shape

    fig, ax = plt.subplots()
    ypos = np.arange(len(shapeCounts.index.values))
    num_reports = shapeCounts.Count.values

    ax.barh(ypos, num_reports, align='center', color='green')
    ax.set_yticks(ypos)
    ax.set_yticklabels(shapes)
    ax.invert_yaxis()

    plt.show()

def sightigsByYear():
    """
    Plot the frequency of UFO sightings by year

    :return: line plot of ufo sightings by year
    """
    yearDf = ufoDf.Year.value_counts()
    yearDf = yearDf.sort_index(ascending=False)
    yearDf = yearDf.iloc[:-75]
    yearDf = yearDf.reset_index()
    yearDf.columns = ['Year', 'Number of Sightings']

    plt_x = yearDf.Year
    plt_y = yearDf['Number of Sightings']

    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    ax.set_title('Number of Sightings by Year')
    ax.set_xlabel('Year')
    ax.set_ylabel('Number of Sightings')

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


def annualHeatmap():
    # TODO change the names on the y axis to month names
    """
    plots a heatmap using seaborn

    :return: plot
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


movieDf2 = pd.read_csv('ufo-movie-releases.csv')
movieDf2 = movieDf2.drop(['Unnamed: 0', 'Unnamed: 0.1.1'], axis=1)
movieDf2["Release Date"] = pd.to_datetime(movieDf2['Release Date']) # Change the dtpye of the release date col to type datetime

def getDateRange(movieReleaseDate):
    '''
    This function should probably go above the movieSightings function
    This function will take a datetime object and return a range of days - 10 before and after the datetime entered.


    :param movieReleaseDate:
    :return: list of datetime objects
    '''
    day_list = []
    dateHigh = movieReleaseDate + timedelta(days=8)
    dateLow = movieReleaseDate - timedelta(days=7)
    delta = dateHigh - dateLow
    for i in range(delta.days):
        day_list.append(dateLow + timedelta(i))




    return day_list

def movieSightings(indexvalue):
    '''
    This function will find the number of dates for a given day
    :param date: datetime object
    :return: the number of sightings for a give day

    '''
    df2 = ufoDf.groupby(['Year', 'Month', 'Date', 'Shape']).agg(len)
    df2 = df2.drop(['Duration', 'Summary', 'Time', 'State',
                                                    'City', 'Posted'], axis=1)
    df2.columns = ['Number of Occurances']
    df2 = df2.unstack(fill_value=0)
    df2 = df2.stack()
    list = []
    date = movieDf2.iloc[indexvalue]['Release Date']

    for i in getDateRange(date):

        try:
            list.append(df2.loc[i.year].loc[i.month]['Number of Occurances'].loc[i.day].sum())
        except KeyError:
            list.append(0)

    npList = np.array(list)

    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    xaxis = np.arange(-7, 8, 1)
    ax.set_xlabel('Days Before and After Release (0 = Release Day)')
    ax.set_ylabel('Number of Sightings')
    ax.set_title('Number of UFO Sightings During the Release of ' + str(movieDf2.iloc[indexvalue]['Movie']))

    plt.xticks(np.arange(-7, 8, 1))
    plt.plot(xaxis, npList)

    print('The average number of daily sightings for the release window of ' + str(movieDf2.iloc[indexvalue]['Movie']) + ' was ' + str(npList.mean()) + ' sightings per day')
    print('The average number of daily sightings for the year was ' + str(df2.loc[date.year].values.mean()))
    plt.show()

    plt.plot(df2.loc[date.year])
    plt.show()
    df2.loc[movieDf2.iloc[indexvalue]['Release Date'].year].unstack(fill_value=0).stack().groupby(['Month', 'Date']).sum().groupby(['Month', 'Date']).mean()
    df2.loc[movieDf2.iloc[indexvalue]['Release Date'].year].unstack(fill_value=0).stack().groupby(
        ['Month', 'Date']).sum()['Number of Occurances'].unstack(fill_value=0).stack()[1]


def yearGraph():
    mask = (ufoDf['Date'] > '1987-1-1') & (ufoDf['Date'] <= '1987-12-31')
    time_series = pd.DataFrame(ufoDf.loc[mask]['Date'].value_counts())  # it may be worthwhile to reset the index and sort the col
    time_series = time_series.resample('D').sum().fillna(0)
    time_series = time_series.sort_index()
    time_series = time_series.reindex(pd.date_range("1987-01-01", "1987-12-31"), fill_value=0)

    plt.plot(time_series.index, time_series['Date'])
    plt.show()

def yearGraphSeasonal():
    mask = (ufoDf['Date'] > '1987-1-1') & (ufoDf['Date'] <= '1987-12-31')
    time_series = pd.DataFrame(ufoDf.loc[mask]['Date'].value_counts())  # it may be worthwhile to reset the index and sort the col
    time_series = time_series.resample('D').sum().fillna(0)
    time_series = time_series.sort_index()
    time_series = time_series.reindex(pd.date_range("1987-01-01", "1987-12-31"), fill_value=0)
    #time_series = time_series.set_index('index')

    time_series['rolling'] = time_series['Date'].rolling(12).mean()
    corrections = time_series['rolling']
    raw = time_series['Date']

    fig = plt.figure(figsize=(13,8))
    ax = fig.add_subplot(1, 1, 1)

    ax.set_xlabel('Date')
    ax.set_ylabel('Number of Sightings per Day (corrected)')
    ax.set_title('Increase in Sightings During the Release of Communion')

    corrections.plot(ax=ax, style='k-')
    #plt.plot(time_series['index'], data)
    nyt_data = dict([(datetime.datetime(1987, 3, 1), 'Communion\nenters NYT\nBestseller List\nat #12'),
                (datetime.datetime(1987, 3, 25), 'Communion\nreaches #3'),
                (datetime.datetime(1987, 5, 10), 'Communion is the\n#1 Bestseller'),
                (datetime.datetime(1987, 7, 2), 'Communion falls out of top 3'),
                (datetime.datetime(1987, 8, 9), 'Falls to #11'),
                (datetime.datetime(1987, 8, 30), 'Rises to #8'),
                (datetime.datetime(1987, 9, 20), 'Last week on\nlist as #15')])

    ax.annotate(nyt_data.values()[0], xy=(nyt_data.keys()[0], corrections.asof(nyt_data.keys()[0]) + .2),
                xytext=(nyt_data.keys()[0], corrections.asof(nyt_data.keys()[0]) + 1.33),
                arrowprops=dict(facecolor='red', shrink=0.05, headwidth=4, width=2, headlength=4),
                horizontalalignment='right', verticalalignment='top')

    ax.annotate(nyt_data.values()[3], xy=(nyt_data.keys()[3], corrections.asof(nyt_data.keys()[3]) + .2),
                xytext=(nyt_data.keys()[3], corrections.asof(nyt_data.keys()[3]) + 1.25),
                arrowprops=dict(facecolor='red', shrink=0.05, headwidth=4, width=2, headlength=4),
                horizontalalignment='right', verticalalignment='top')

    ax.annotate(nyt_data.values()[4], xy=(nyt_data.keys()[4], corrections.asof(nyt_data.keys()[4]) + .2),
                xytext=(nyt_data.keys()[4], corrections.asof(nyt_data.keys()[4]) + .75),
                arrowprops=dict(facecolor='red', shrink=0.05, headwidth=4, width=2, headlength=4),
                horizontalalignment='left', verticalalignment='top')

#    ax.annotate(nyt_data.values()[5], xy=(nyt_data.keys()[5], corrections.asof(nyt_data.keys()[5]) + .2),
#                xytext=(nyt_data.keys()[5], corrections.asof(nyt_data.keys()[5]) + .75),
#                arrowprops=dict(facecolor='red', shrink=0.05, headwidth=4, width=2, headlength=4),
#                horizontalalignment='left', verticalalignment='top')

    ax.annotate(nyt_data.values()[6], xy=(nyt_data.keys()[6], corrections.asof(nyt_data.keys()[6]) + .2),
                xytext=(nyt_data.keys()[6], corrections.asof(nyt_data.keys()[6]) + 1.08),
                arrowprops=dict(facecolor='red', shrink=0.05, headwidth=4, width=2, headlength=4),
                horizontalalignment='right', verticalalignment='top')

    ax.annotate(nyt_data.values()[1], xy=(nyt_data.keys()[1], corrections.asof(nyt_data.keys()[1]) + .2),
                xytext=(nyt_data.keys()[1], corrections.asof(nyt_data.keys()[1]) + 1),
                arrowprops=dict(facecolor='red', shrink=0.05, headwidth=4, width=2, headlength=4),
                horizontalalignment='left', verticalalignment='top')

    plt.savefig('figpath.png', dpi=300)

    plt.show()
    #data = time_series['Date'].rolling(12).mean()

def yearGraphSeasonal2():
    mask = (ufoDf['Date'] > '2014-1-1') & (ufoDf['Date'] <= '2015-12-31')
    time_series = pd.DataFrame(ufoDf.loc[mask]['Date'].value_counts())  # it may be worthwhile to reset the index and sort the col
    time_series = time_series.resample('D').sum().fillna(0)
    time_series = time_series.sort_index()
    time_series = time_series.reindex(pd.date_range("2014-01-01", "2014-12-31"), fill_value=0)
    #time_series = time_series.set_index('index')

    time_series['rolling'] = time_series['Date'].rolling(12).mean()
    time_series['diff'] = time_series['Date'].diff(4)
    corrections = time_series['rolling']
    raw = time_series['Date']
    diff = time_series['diff']
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    plt.plot(time_series.index, diff)
    plt.show()