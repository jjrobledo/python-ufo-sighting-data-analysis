This project aims at examining data gathered by the [National UFO Reporting Center (NUFORC)](http://www.nuforc.org/). 

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

One of the questions I'm interesting in examining is whether or not the release of a UFO themed movie in theaters (like Close Encounters of the Third King, MIB, etc.) affect the number of UFO sightings around the time of release. This script will read a .csv containing a list of UFO themed movies collected from the Wikipedia page on [UFOs in Fiction](https://en.wikipedia.org/wiki/UFOs_in_fiction)(with a few additions of my own) clean up the data a bit, and use the `imdb` library to lookup the the year and day the movie was released. The script will then save the data to disk as ufo_movie_releases.csv.

#### ufo_data_analysis.py

ufo_data_anlysis.py will read in all the data provided by the previous scripts and manipulate that data in various ways. The script has a number of functions that may be called; I will describe them here in order.

##### shape_graph()

shape_graph() is a simple function that, when called, reads a pandas dataframe containing the cleaned sighting data from ufo_scraper.py and counts the total number of sightings for each unique UFO shape. It then uses `matplotlib` to generate a simple bar graph to visualize the data. Several UFO shapes are dropped from the graph; their sighting counts are too low and to include them would make the graph unpleasant to view.



##### sightings_by_shape()

sightings_by_shape() reads the same dataframe of UFO sightings and plots the frequency of UFO sightings by shape per year. I have chosen to display the data from 1974 to present, the reason being the NUFORC was founded in 1974 and I would like to minimize the amount of UFO sightings that were reported years after the event occurred. However, it is easy to change the date range displayed on the graph. All you need to do is change the index value of `x_axis` and `y_axis`  from -45 to the year you're interested in (don't forget to change the `xticks` as well). For example, if you wanted to graph from 1964 to present you should change the index from -45 to -55:

```python
x_axis = df1['Number of Occurances'][:, shape][-45:].index
```

to

```python
x_axis = df1['Number of Occurances'][:, shape][-55:].index
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

### Included CSV files



## Authors

* **Jose Robledo**
