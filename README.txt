This project aims at gathering, manipulating and examining data gathered by the [National UFO Reporting Center (NUFORC)](http://www.nuforc.org/). 

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

The following Python libraries are required:

```python
seaborn geopy folium matplotlib numpy pandas bs4
```

### Included Python Scripts

There are a number of Python scripts included in this repository.  And there is a general sequence in which they should be ran is as follows:

#### ufo_scraper.py

To begin collecting the data run ufo_scraper.py. This will collect all available sightings from the [National UFO Reporting Center (NUFORC)](http://www.nuforc.org/) and save them as a .csv file. But, be warned it will take a while to collect the data. 

#### dataframe_cleaner.py

The NUFORC collects a lot of interesting data for individual UFO sightings. However, some of the data is poorly formatted. The dataframe_cleaner script will better format the data we will be interested in analyzing. Aside from correcting case errors and renaming data columns, the script will take the date of each sighting and format it as datetime object - very useful for what we will be doing later. 

One of the concerns I had regarding the data concerned the way shapes of UFO sightings were collected. For example, Is there really a difference between a delta shaped UFO and a triangle shaped UFO? I don't think so. Thus, the script also aggregates specific UFO shapes in order to reduce "noise".  I attempted to contact the director of the NUFORC for guidance. However, he never responded to my communication, so the shape aggregations are my own educated guesses.

Finally, I was interested in plotting the UFO sighting data geographically. After a bit of experimentation I decided to use the Python library `geopy` to do reverse geocoding. dataframe_cleaner.py uses the google geocoding API through `geopy` to look up latitude and longitude data for each city, state element in the UFO report data. You will need to provide your own API key to run the script and you can get one from the [Google Cloud Platform](https://cloud.google.com). Google offers a free trial of 150,000 look-ups or two weeks free - not too shabby! (just don't go over your limits and forget to cancel)

dataframe_cleaner.py will write the following two files to disk:

```
ufo_reports.csv and ll.csv
```

ufo_reports.csv contains all of the UFO report data along with the corrections and ll.csv contains all the latitude and longitude data.

#### move_list_cleanup.py

One of the questions I'm interesting in examining is whether or not the release of a UFO themed movie in theaters (like Close Encounters of the Third King, MIB, etc.) affect the number of UFO sightings around the time of release. This script will read a .csv containing a list of UFO themed movies collected from the Wikipedia page on [UFOs in Fiction](https://en.wikipedia.org/wiki/UFOs_in_fiction) (with a few additions of my own) clean up the data a bit, and use the `imdb` library to lookup the the year and day the movie was released. The script will then save the data to disk as ufo_movie_releases.csv.

#### ufo_data_analysis.py

ufo_data_anlysis.py will read in all the data provided by the previous scripts and manipulate that data in various ways. The script has a number of functions that may be called; I will describe them here in order.

##### shape_graph()

shape_graph() is a simple function that, when called, reads a pandas dataframe containing the cleaned sighting data from ufo_scraper.py and counts the total number of sightings for each unique UFO shape. It then uses `matplotlib` to generate a simple bar graph to visualize the data. Several UFO shapes are dropped from the graph; their sighting counts are too low and to include them would make the graph unpleasant to view.



##### sightings_by_shape()

sightings_by_shape() reads the same dataframe of UFO sightings and plots the frequency of UFO sightings by shape per year. I have chosen to display the data from 1974 to present, the reason being the NUFORC was founded in 1974 and I would like to minimize the amount of UFO sightings that were reported years after the event occurred. However, it is easy to change the date range displayed on the graph. All you need to do is change the index value of `x_axis` and `y_axis`  from -45 to the year you're interested in (don't forget to change the `xticks` as well). For example, if you wanted to graph from 1964 to present you should change the index from -45 to -55:

```python
x_axis = df1['Number of Occurances'][:, shape][-45:].index
y_axis = df1['Number of Occurances'][:, shape][-45:].values
```

to

```python
x_axis = df1['Number of Occurances'][:, shape][-55:].index
y_axis = df1['Number of Occurances'][:, shape][-55:].values
```



##### heatmap()

heatmap() reads the UFO sighting dataframe and manipulates the data to show the average number of UFO sightings for each day of the year based on the date range specified. The data is then visualized as a `seaborn` heatmap. You can change the date range yourself by changing the variables `start_time` and `end_time` to the date of your choosing (they must be kept as strings in the format of YYYYMMDD).

##### get_date_range()

This function is not meant to be called on its own. Although you could if you really wanted to.

get_date_range() takes a movie release date as a datetime object and calculates a range of days before and after the release. The function returns a tuple, a list of days and the release date of the chosen movie.

##### movie_sightings()

Again, this function should not be called on its own. 

movie_sightings() takes an integer corresponding to and index value corresponding to the desired movie in ufo_movie_releases.csv. It then calls get_date_range() to get a release window for the movie. Then number of UFO sightings for the release year are calculated and then a masked based on the release window. The function then returns a pandas dataframe contining a time series of sighting data, the first and last day of the release window, and the release date.

##### movie_window_plot()

movie_window_plot() will return a graph showing the average number of sigithings two weeks before and two weeks after a movie release date. The function should be called by passing movie_sightings(int) as the argument:

```python
movie_window_plot(movie_sightings(66)) 
```

##### year_graph()

year_graph() takes two dates (a start date and end date) as strings in the format of YYYMMDD:

```python
year_graph('19981231', '20121231')
```

It uses the user provided dates to generate a mask to filter the UFO sighting dataframe. The result is a time series of UFO sightings for each day of the date range. If the date range specified happens to overlap with the original run of the TV series The X-Files you will also see a line graph of the number of viewers per episode (in millions).

##### annotated_bestseller()

The release of the book "Communion" by Whitley Strieber was one of the most important events in the pop culture history of UFOs. With its striking cover, the book cemented the image of the pallid, almond eyed, extraterrestrial in the public consciousness. The book, which Strieber claims is a true account, is also the source for the well known trope of alien anal probes as parodied in the first episode of the popular television show South Park.
This function seeks to explore if the release of the book and its 1987 climb to the top of the NYT Bestseller list had an effect on the frequency of UFO sightings during the year. Like previous functions, it uses a date mask to specify relevant time series data.

##### mapping()

mapping() reads the .csv containing the latitude and longitude data. It then cleans then cleans the columns in preparation for plotting in `folium`. I explored a number of mapping libraries for Python before settling on `folium`.  It was chosen primarily for ease of use and the ability of the user to interact with the data in a web browser.

After the data is cleaned, mapping() will take the latitude and longitude of each row, combine them into a tuple and add them to a master list of coordinates. `folium` will then take the list of coordinates and generate a heat map of all UFO sightings collected by the NUFORC.

It also generates a really cool heat map with time by passing a list of lists to `HeatMapWithTime()`. In this case the list of lists is a list of years of sightings by month e.g. `[[JAN, FEB, MAR, APR, MAY, JUN, JUL, AUG, SEP, OCT, NOV, DEC ], [JAN, FEB, ...]]` . 

Both heat maps are saved as .html files. Users can open them as web pages, pan the map and zoom in/out on specific areas. The heat map with time add the ability to play the data frame by frame (month by month).

It should be noted that the during the geocoding some location lookups returned the wrong latitudes/longitudes. I'm not exactly sure how many, but it shouldn't affect the final map too much and they probably represent the heat spots in unusual places, like the middle of the ocean.

**IMPORTANT**  In order to see the heat map data on the map you may need to turn off your ad blocker.

### Included CSV files

# Visualizations

## What UFO shapes are most common?

One of th first questions we can ask is if you were to see an unusual object in the sky, in other words a UFO, what shape is is most likely to be? We can answer that question by calling `shape_graph`.

![](./images/shape_graph.png)



It turns out that about 21 percent of the 111742 sightings tallied by `shape_counts()` are reports of lights in the sky. The iconic disk shaped UFOs make up about 17 percent of sighting reports. And rounding out the top three, triangle shaped UFOs make up 9.6 percent of sightings.



## How have UFO reports changed over time?

The next thing we should ask is how UFO sighting reports have changed over time by calling `year_graph()`. 

![](./images/yearly_sighting_reports.png)

The graph above gives us a 6 month rolling average of daily UFO sightings from 1974 to May 31 2018. The first thing to notice is the dramatic increase in sightings beginning around 1995. Sightings continue to rise from the mid 90s till they peak around 2014. One other interesting thing to look at is the seasonality of the data; we'll look at this more closely in a bit, but for now we can say that there is a correlation between the time of the year and the number of reported UFO sightings.

Why the  rolling average? Well, without doing some interpolation its difficult to see the over all trend of the data. It also allows us to see the seasonality on a line graph. Heres a look at the the data without the rolling average: 

![](./images/no_roll.png)



We can also see how the shapes of reported UFOs have changed over time by calling `year_graph()`:![](./images/sightings_by_shape.png)

By looking at the graph we can see that same dramatic increase in sightings that began in the mid 90s as well as the peak in 2014. This graph also shows us just how steeply UFO sighting reports have decline since 2016. This is because this graph plots only the number of sightings reported and doesn't take into account the days where no reports were filed (this also accounts for the dramatic difference between the two previous graphs. 

Unfortunately, this graph is difficult to look at since there are so many lines plotted. But, it does allow us to quickly spot some interesting trends.

By changing the mask in `year_graph()` we can isolate some of the more interesting shape trends:

![](./images/light_disk_tri.png)

Here we have only 4 shapes to deal with. We can more clearly see that prior to 1986 disk shaped UFOs were the most commonly reported shape before a decline in the mid 80s. When Sightings jumped around 1995 we see that light reports see the biggest increase and continue to be the most commonly reported UFO. One of the stranger observations is the two peaks on the line depicting sightings of fireball UFOs sightings. It shows a small peak around 1999 before leveling out; and then it rises dramatically from 2010 to 2012. Disk and light shaped UFOs do as well, but triangle shapes, along with many others from the previous graph, show a much less dramatic increase.

When I think about UFOs being reported as fireballs I immediately think that there must be some correlation with bolide and meteor observations. It turns out that the International Meteor Organization (IMO) collects meteor report [data](https://www.imo.net/members/imo_vmdb). If you look a the data they're collected you will see a spike in meteor reports right around 1998. However the conspicuous spike in fireball shaped UFOs around 2010 is absent in the meteor data.

The IMO data also shows a decline in reports *and* observers around  the same time we see the dramatic decline in UFO reports to the NUFORC. Perhaps the decline in meteor observations and the decline in UFO reports have a similar cause - a decline in the number of people looking up to the sky.

## Heat Mapping

One of the most interesting visualization tools we can use to look at the NUFORC data is the `seaborn` heatmap. It turns out that there are a number of calendrical event that affect the number of sightings reported to the NUFORC. Have a look:

![](./images/annual_heatmap.png)

Looking at the graph, we can clearly see the bi-annual rise and fall of UFO sightings. That is to say sightings are more common in the late spring and early  than they are in winter months. One of the most surprising things I found is the high frequency of sightings that occur on the 1st and 15th of every month. At first I thought I had done something wrong with the data I was graphing, but then I thought for a minute and remembered that the most common pay schedule in the U.S. is bi-monthly. Thus, there must be some correlation between pay days and UFO sightings. I have to admit that the first conclusion that I drew was that people must be going out and spending their paychecks on alcohol, but that seemed a bit glib. It could be that people are more likely to be out and about after they have been paid (thus, more likely to see something in the sky).  It turns out that 13.3 percent of reports fall on the 1st or 15th of the month.

But, we can't completely discount the first conclusion, in reading the NUFORC blog its clear that they receive prank calls, and it isn't too much of a stretch to wonder if some of these payday reports are the results of revelers having some fun at the expense of the NUFORC. It also reminds us to be wary of witness reported data, its one of the reasons I've chosen to leave out pre-1974 UFO reports. The reason being, the NUFORC was founded in 1974 - any reports prior to that are entirely witness recollections. 

#### Fireworks and Holidays

There also seems to be a correlation between fireworks and UFO sightings. look closely at January 1st and the week of July 4th and you will notice a hotspot on the map. Again we must be careful about attributing fireworks as the cause of the UFO reports. It could be just as likely that people are seeing more UFOs because they are going outside and looking up at the sky. In total 7.5 percent of UFO sightings occur on New Years eve/day and another 4.97 percent on Independence Day. 

But fireworks still seem like a major contributor to UFO reports. We can look at other holidays where Americans typically spend the day outside, namely Memorial Day (last week of May) and Labor Day (first week of September) and we don't see the same increase in the frequency of UFO sightings during those weeks. The week of Memorial Day (May 25-31) accounts for 1.5 percent of reports and Labor Day 2.2 percent of all reports.

#### Historic Events

One correlation most wouldn't have guessed has to do with U.S. presidential elections. If you look at November 8th (U.S. election day) you'll see that there is a spike in sightings on that day. It seems as though stressful or highly emotional national events might be connected to a rise in UFO sightings. To illustrate let's look at a heat map of 2001:

![](/home/jrobledo/Projects/ufo-scraper/images/heatmap_2001.png) 

You may notice that there is a increase in the number of UFO sightings leading up to September 11 before peaking on 9/11. Thus, like the correlation we saw with election day, there seems to be some correlation with emotional events and UFO sightings.

#### Meteor Showers

In looking at the heat map from 2001 you will also notice that there is a correlation between peak days of meteor showers and UFO sightings. For instance, in 2001 [November 18](https://www.imo.net/leonids-2001-updated-profile/) was the peak of the Leonid meteor shower (you can also see a slight increase around this date on the aggregated heat map - but, its not as obvious since peak days for meteor showers can drift on the calendar, not to mention being obscured by weather).  You can also make out the peak of the Perseids on both heat maps. In fact, when we add up the number of UFO sightings on the dates of three major meteor showers (1974 - present) - Perseids (17 July - 24 August), Leonids (6 November - 17 November) and Geminids (4 December - 17 December) - we find that 23 percent of all UFO sightings occurred on those dates. We may also ask what kind of UFOs are seen during meteor showers our first instinct being that sightings of fireballs must be higher. It turns out that around 7.6 percent of all UFO reports are of fireballs, and on the days of the sampled meteor showers fireballs  account for 8.6 percent of reports. If we look at a bar graph of UFO shapes during meteor showers we see that the frequency of each shape is roughly the same - again, light being the most commonly reported shape at 21.1 percent.

![](/home/jrobledo/Projects/ufo-scraper/images/meteor_shapes.png)

## Movie Releases and UFO Sighting Reports

Can the Release of UFO themed movies affect the number of UFO reports? To investigate this question I used a list of [UFOs in Fiction](https://en.wikipedia.org/wiki/UFOs_in_fiction) that seemed appropriate for my purposes. Each movie is assigned a release window. Here are a few examples.



```
 <iframe src="./images/heatmap.html" height="315" width="560" frameborder="0">
```

## Authors

* **Jose Robledo**
