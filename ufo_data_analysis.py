import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
#import datetime as datetime
from datetime import datetime
from datetime import timedelta
#from matplotlib import dates
from mapsplotlib import mapsplot as mplt
import folium
from folium.plugins import HeatMap, HeatMapWithTime
from dateutil.relativedelta import relativedelta


pd.set_option('display.expand_frame_repr', False)


ufo_df = pd.read_csv('ufo_reports.csv')
ufo_df.Date = pd.to_datetime(ufo_df[['Year', 'Month', 'Day']], errors='coerce')
ll_df = pd.read_csv('ll.csv')
ufo_df2 =  pd.merge(ufo_df, ll_df, left_index=True, right_index=True) # ufo_df2 contains lat long data
ufo_df2['Lat'] = ufo_df2['Lat'].fillna(0)
ufo_df2['Long'] = ufo_df2['Long'].replace({'Nan': '0'})
ufo_df2['Long'] = pd.to_numeric(ufo_df2['Long'])


def shape_graph():
    """
    Generates a bar graph with a list of shapes on the y-axis and their frequency of the x-axis.

    :return: bar graph plot
    """
    ufo_shape_array = []
    for i in ufo_df.Shape.str.upper().unique():
        ufo_shape_array.append(i)

    shape_counts = pd.DataFrame(ufo_df.Shape.value_counts())
    shape_counts = shape_counts.drop(['EMPTY', 'HEXAGON', 'CRESCENT', 'PYRAMID', 'DOME'])  # Remove values that are of little value
    shape_counts.columns = ['Count']

    ax = plt.subplots()

    ax = shape_counts.plot.barh()
    ax.set_xlabel('Number of Reports')
    ax.set_ylabel('Shape of Reported UFO')
    ax.set_title('Most Commonly Reported UFO Shapes')
    plt.show()


def sightings_by_shape():
    """
    This function will show how the frequency UFO sightings by shape has changed over time.

    :return: line plot
    """
    df = ufo_df[~ufo_df['Shape'].isin(['EMPTY'])]
    df1 = df.groupby(['Year', 'Shape']).agg(len)  # use .loc[xxxx] to call for a specific year
    df1 = df1.drop(['Unnamed: 0', 'Date', 'Duration', 'Summary', 'Month', 'Time', 'State', 'Posted'], axis=1)
    df1.columns = ['Number of Occurances', 'Untitled']
    df1 = df1.unstack(fill_value=0)
    df1 = df1.stack()
    mask = (df['Shape'] != 'DOME') & (df['Shape'] != 'CROSS') & (df['Shape'] != 'CONE') & (df['Shape'] != 'HEXAGON') & (df['Shape'] != 'PYRAMID') & (df['Shape'] != 'CRESCENT')
    df2 = df[mask]

    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    for shape in df2.Shape.unique():
        x_axis = df1['Number of Occurances'][:, shape][-45:].index
        y_axis = df1['Number of Occurances'][:, shape][-45:].values
        ax.set_title('Number of UFO Sightings by Shape (1974-present)')
        ax.set_xticks(np.arange(1974, 2019, 4))
        plt.plot(x_axis, y_axis, label=shape)
    ax.legend(loc=2, fontsize='x-small')
    ax.set_xlabel('Year')
    ax.set_ylabel('Number of Sightings')
    plt.show()


def heatmap():
    start_time = '1974-01-01'
    end_time = '20180531'
    df = ufo_df.groupby('Date')
    df = ufo_df.groupby('Date').agg(len)
    df = df.resample('D').sum().fillna(0)
    df = df.drop(['Time', 'City', 'State', 'Shape', 'Duration', 'Summary', 'Posted', 'Year', 'Month', 'Day'], axis=1)
    df = df.reset_index()
    mask = (df.Date > start_time) & (df.Date <= end_time)
    sightings = pd.DataFrame(df.loc[mask])
    sightings.columns = ['Date', 'Count']
    sightings = sightings.set_index('Date')
    sightings['Year'] = sightings.index.year
    sightings['Month'] = sightings.index.month
    sightings['Day'] = sightings.index.day
    x = sightings.groupby(['Year', 'Month', 'Day']).sum()
#   x = x['Count']rolling(12).sum().dropna()
    x2 = x.groupby(['Month', 'Day']).sum()
    x3 = x2.pivot_table(index='Month', columns='Day', values='Count')
    grid_kws = {"height_ratios": (.9, .05), "hspace": .3}
    f, (ax, cbar_ax) = plt.subplots(2, gridspec_kw=grid_kws)
    cbar_ax.set_title('Number of Sightings')
    ax = sns.heatmap(x3, square=True, vmin=100, vmax=600, center=200, linewidths=.03, ax=ax, cbar_ax=cbar_ax,
                     cbar_kws={"orientation": "horizontal"})
    plt.show()
    '''
    start_time = '19991231'
    end_time = '20001231'
    df = ufo_df.groupby('Date')
    df = ufo_df.groupby('Date').agg(len)
    df = df.resample('D').sum().fillna(0)
    df = df.drop(['Time', 'City', 'State', 'Shape', 'Duration', 'Summary', 'Posted', 'Year', 'Month', 'Day'], axis=1)
    df = df.reset_index()
    mask = (df.Date > start_time) & (df.Date <= end_time)
    sightings = pd.DataFrame(df.loc[mask])
    sightings.columns = ['Date', 'Count']
    sightings = sightings.set_index('Date')
    sightings['Year'] = sightings.index.year
    sightings['Month'] = sightings.index.month
    sightings['Day'] = sightings.index.day
    x = sightings.groupby(['Year', 'Month', 'Day']).sum()
    x = x['Count']rolling(12).sum().dropna()
    x2 = x.groupby(['Month', 'Day']).sum()
    x3 = x2.pivot_table(index='Month', columns='Day', values='Count')
    grid_kws = {"height_ratios": (.9, .05), "hspace": .3}
    f, (ax, cbar_ax) = plt.subplots(2, gridspec_kw=grid_kws)
    cbar_ax.set_title('Number of Sightings')
    ax = sns.heatmap(x3, square=True, vmax=35, linewidths=.03, ax=ax, cbar_ax=cbar_ax,
                     cbar_kws={"orientation": "horizontal"})
    ax.set_title('UFO Sightings for the year ' + end_time[:4])
    plt.show()
    '''




movie_df2 = pd.read_csv('ufo-movie-releases.csv')
movie_df2 = movie_df2.drop(['Unnamed: 0', 'Unnamed: 0.1.1'], axis=1)
movie_df2["Release Date"] = pd.to_datetime(movie_df2['Release Date']) # Change the dtpye of the release date col to type datetime


def get_date_range(movie_release_date):
    '''
    This function will take a datetime object from movie_sightings() and return a range of days before and after
     the datetime.
    :param movie_release_date:
    :return: list of datetime objects
    '''

    release = movie_release_date
    day_list = []
    date_high = movie_release_date + timedelta(days=16)
    date_low = movie_release_date - timedelta(days=14)
    delta = date_high - date_low
    for i in range(delta.days):
        day_list.append(date_low + timedelta(i))

    return day_list, release


def movie_sightings(index_value):
    '''
    This function will take an index value from movie_df2 and calculate a release window
    for the movie.
    :param index_value: int
    :return: Dataframe containing a time series of datetime objects

    '''

    date = movie_df2['Release Date'][index_value]
    release_window = get_date_range(date)
    date_low = release_window[0][0]
    date_high = release_window[0][-1]
    release = release_window[1]
    year_start = datetime.strptime(str(date_low.year) + '0101', '%Y%m%d').date()
    year_end = datetime.strptime(str(date_high.year + 1) + '0101', '%Y%m%d').date()

    year_mask = (ufo_df['Date'] > year_start) & (ufo_df['Date'] <= year_end)
    # mask = (ufo_df['Date'] > date_low) & (ufo_df['Date'] <= date_high)

    time_series = pd.DataFrame(ufo_df.loc[year_mask]['Date'].value_counts())  # it may be worthwhile to reset the index and sort the col
    time_series = time_series.resample('D').sum().fillna(0)
    time_series = time_series.sort_index()
    # time_series = time_series.reindex(pd.date_range(time_series.iloc[0], time_series.iloc[-1]), fill_value=0)
    time_series['pytime'] = time_series.index
    time_series.columns = ['Number of Sightings', movie_df2.iloc[index_value]['Movie']]
    time_series['rolling'] = time_series['Number of Sightings'].rolling('30D').mean()  # rollingmean to correct for seasonal changes

    return [time_series, date_low, date_high, release, release_window[0]]


def movie_window_plot(dataframe):
    '''
    This function will return a graph showing the average number of sightings two weeks before and two weeks after
    a movie release date. The function should be called by passing movie_sightings(int) as the argument. movie_sighings
    will pass the release date of the movie to get_date_range and pass it along with other information to movie window
    plot.
    :param dataframe: This is actually a list dataframe[0] is the time_series dataframe, [1:3] is a series of useful dates
    and [4] is a release window helpful for focusing the plot.
    :return: plot of average sightings during a date range.
    '''

    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    release_date = dataframe[3]

    ax.set_xlim(dataframe[4][0], dataframe[4][-1])

    xaxis = [datetime.strftime(i, '%b %d') for i in dataframe[4]]

    ax.set_xlabel('Days Before and After Release (release day =' + ' ' + str(release_date.strftime("%B %d")) + ')')
    ax.set_ylabel('Number of Sightings')
    ax.set_title('UFO Sightings During the Release of ' + str(dataframe[0].columns.get_values()[1]))
    ax.set_xticks(dataframe[4])
    ax.set_xticklabels(xaxis)

    count = 0
    for i in dataframe[4]:
        if i.weekday() == 5:
            ax.get_xticklabels()[count].set_color("black")

        elif i.weekday() == 6:
            ax.get_xticklabels()[count].set_color("black")

        else:
             ax.get_xticklabels()[count].set_color("dimgray")

        count += 1

    ax.get_xticklabels()[14].set_color("red")
    plt.xticks(rotation=70)

    ax.plot(dataframe[0].index, dataframe[0]['rolling'])

    '''
    red = mpatches.Patch(color='red', label='Release Date')
    black = mpatches.Patch(color='black', label='Weekend')
    plt.legend(handles=[red, black])
    '''

    print('The average number of daily sightings for the release window of ' + str(dataframe[0].columns.get_values()[1]) + ' was ' + str(dataframe[0]['Number of Sightings'].mean()) + ' sightings per day')
    print(dataframe[0]['Number of Sightings'].std(), dataframe[0]['Number of Sightings'].median())
    print('The average number of daily sightings for the year was ')

    plt.show()


def year_graph(start_date, end_date):
    '''
    This function will take two strings in the form of 'YYYYMMDD' and return a graph of the average number of UFO
    sightings for the given date range.

    :param start_date: a string like '19990101' in the format of YYYYMMDD
    :param end_date: a string like '19990101' in the format of YYYYMMDD
    :return: plot
    '''
    mask = (ufo_df['Date'] > start_date) & (ufo_df['Date'] <= end_date)
    time_series = pd.DataFrame(ufo_df.loc[mask]['Date'].value_counts())  # it may be worthwhile to reset the index and sort the col
    time_series2 = pd.DataFrame(ufo_df.loc[mask]['Date'].value_counts())
    time_series2 = time_series2.sort_index()
    time_series = time_series.resample('D').sum().fillna(0) # Resample to return the missing days to the df
    time_series = time_series.sort_index()
    time_series = time_series.reindex(pd.date_range(start_date, end_date), fill_value=0)
    time_series.columns = ['Number of Sightings']
    time_series['rolling'] = time_series['Number of Sightings'].rolling('180D').mean()

    xfiles_df = pd.read_csv('xfiles.csv')
    xfiles_df = xfiles_df.set_index('Air Date')
    xfiles_df.index = pd.to_datetime(xfiles_df.index)
    # xfiles_df = xfiles_df.resample('D').sum().fillna(0)
    xfiles_df = xfiles_df.sort_index()
    xfiles_df['Roll'] = xfiles_df['Viewers (millions)'].rolling('30D').mean()
    # xfiles_df['Roll'] = xfiles_df['Roll'].rolling(12).mean()

    plt_y = time_series['rolling']  # time_series2['Date'].rolling(12).mean()
    plt_x = time_series.index

    plt_x2 = xfiles_df.index
    plt_y2 = xfiles_df['Viewers (millions)'] * .16

    plt.plot(plt_x, plt_y) # ufo sightings
    # plt.plot(plt_x2, plt_y2) # xfiles ratings
    plt.show()

def annotated_bestseller():
    '''
    The release of the book "Communion" by Whitley Strieber was one of the most important events in the pop culture
    history of UFOs. With its striking cover, the book cemented the image of the pallid, almond eyed, extraterrestrial
    in the public consciousness. The book, which Strieber claims is a true account, is also the source for the well
    known trope of alien anal probes as parodied in the first episode of the popular television show South Park.

    This function seeks to explore if the release of the book and its 1987 climb to the top of the NYT Bestseller list
    had an effect on the frequency of UFO sightings during the year.

    :return: plot
    '''
    mask = (ufo_df['Date'] > '1987-1-1') & (ufo_df['Date'] <= '1988-12-31')
    time_series = pd.DataFrame(ufo_df.loc[mask]['Date'].value_counts())  # it may be worthwhile to reset the index and sort the col
    time_series = time_series.resample('D').sum().fillna(0)
    time_series = time_series.sort_index()
    time_series = time_series.reindex(pd.date_range("1987-01-01", "1988-12-31"), fill_value=0)
    # time_series = time_series.set_index('index')

    time_series['rolling'] = time_series['Date'].rolling(12).mean()
    corrections = time_series['rolling']
    raw = time_series['Date']

    fig = plt.figure(figsize=(13,8))
    ax = fig.add_subplot(1, 1, 1)

    ax.set_xlabel('Date')
    ax.set_ylabel('Number of Sightings per Day (corrected)')
    ax.set_title('Increase in Sightings During the Release of Communion')

    corrections.plot(ax=ax, style='k-')
    # plt.plot(time_series['index'], data)
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

# The following functions are no longer working and are being kept for reference.


def sightings_by_year():
    """
    Not working. Use year_graph() instead.

    :return: line plot of ufo sightings by year
    """
    year_df = ufo_df.Year.value_counts()
    year_df = year_df.sort_index(ascending=False)
    year_df = year_df.iloc[:-75]
    year_df = year_df.reset_index()
    year_df.columns = ['Year', 'Number of Sightings']

    xfiles_df = pd.read_csv('xfiles.csv')
    xfiles_df = xfiles_df.set_index('Air Date')
    xfiles_df.index = pd.to_datetime(xfiles_df.index)

    plt_x = year_df.Year
    plt_y = year_df['Number of Sightings']

    plt_x2 = xfiles_df.index
    plt_y2 = xfiles_df['Viewers (millions)']

    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    ax.set_title('Number of Sightings by Year (1974-Present)')
    ax.set_xlabel('Year')
    ax.set_ylabel('Number of Sightings')

    plt.plot(plt_x, plt_y)
    #plt.plot(plt_x2, plt_y2 * 1000)
    plt.show()




def mapping():

    csv_name = pd.read_csv('ll.csv') # Read in the list of lat/longs

    df = pd.DataFrame(csv_name) # convert the csv to dataframe

    df['Long'] = df['Long'].str[:7] 
    df['Long'] = df['Long'].replace({'Nan': '0'}) # remove Nan values
    df['Long'] = pd.to_numeric(df.Long) # convert the column to numeric values
    df['Lat'] = df['Lat'].fillna(0) # fill any Nan values with 0s
    df.Lat = df.Lat.round(3) # round the columns for compatability with folium
    df.Long = df.Long.round(3)
    df = df.drop(['Unnamed: 0'], axis=1) # drop unused axis
    df.columns = ['latitude', 'longitude'] # rename columns

    map = folium.Map(tiles='stamentoner') # create a folium map for all UFO sightings

    coords = [] # init list of lat/long coords for folium map

    for index, row in df.iterrows(): # fill the list of coords
        coords.append(tuple([row.latitude, row.longitude]))

    hm = HeatMap(coords, min_opacity=.25, radius=15, max_zoom=13) # create the heatmap 
    hm.add_to(map) # add the heatmap to the folium map

    map.save('heatmap.html') # save the map to disk


    ####################################################
    #
    # This section will generate a folium HeatMapWithTime
    # HeatMapWithTime() takes a list of lists to generate the map
    #
    #
    ####################################################

    list_list = [] # list of lists. It contains monthly sighting data for each month of each year between start_date and end_date.
    date_list = [] # list of formatted dates to use as the HeatMapWithTime() index
    start_date = datetime.strptime('20150101', '%Y%m%d') # heat map start date
    end_date = datetime.strptime('20171231', '%Y%m%d') # heat map end date
    date = start_date # date list will help us calculate the timedelta()
    month_delta = relativedelta(months=+1) # the timedelta() to iterate months

    # While loop to fill date_list
    while date <= end_date:
        date_list.append(date.strftime('%B %Y'))
        date += month_delta

    # Nested for loop to create list_list 
    for i in range(start_date.year, (end_date.year + 1)):
        list_list1 = []
        year_list = []
        list_list1 = list_list.extend(year_list)
        for j in range(1, 13):
            month_list = []
            list_list.append(month_list)
            for index, row in ufo_df2.iterrows():
                if row['Date'].year == i and row['Date'].month == j:
                    lt_lon = [row['Lat'], row['Long']]
                    month_list.append(lt_lon)


    # map2 will be the folium map for the HeatMapWithTime()
    map2 = folium.Map(tiles='stamentoner')
    # hmt will be the folium HeatMapWithTime() 
    hmt = HeatMapWithTime(list_list, index=date_list)
    # add the HeatMapWithTime to map2
    hmt.add_to(map2)
    # save map2 to disk
    map2.save('heatmap_with_time.html')
   

#######################################################################################################################
#
# None of the functions below this line are working. They are being kept for refrence purposes.
#
#
########################################################################################################################
def annual_heatmap():
    """
    No longer working. Use heatmap() instead.
    :return: plot
    """
    df2 = ufo_df.groupby(['Year', 'Month', 'Date', 'Shape']).agg(len)
    df2 = df2.drop(['Duration', 'Summary', 'Time', 'State', 'City', 'Posted'], axis=1)
    df2.columns = ['Number of Occurances', 'untitled']
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

