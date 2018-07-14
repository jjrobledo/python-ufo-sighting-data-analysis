One Paragraph of project description goes here

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

The following Python plugins are required

```python
seaborn geopy folium matplotlib numpy pandas bs4
```

### Included Python Scripts

There are a number of Python scripts included in this repository.  And there is a general sequence in which they should be ran.

#### ufo_scraper.py

To begin collecting the data run ufo_scraper.py. This will collect all available sightings from the [National UFO Reporting Center (NUFORC)](http://www.nuforc.org/) and save them as a .csv file. But, be warned it will take a while to collect the data. 

#### dataframe_cleaner.py

The NUFORC collects a lot of interesting data for individual UFO sightings. However, some of the data is poorly formatted. The dataframe_cleaner script will better format the data we will be interested in analyzing. Aside from correcting case errors and renaming data columns, the script will take the date of each sighting and format it as datetime object - very useful for what we will be doing later. 

One of the concerns I had regarding the data concerned the way shapes of UFO sightings were collected. For example, Is there really a difference between a delta shaped UFO and a triangle shaped UFO? I don't think so. Thus, the script also aggregates specific UFO shapes in order to reduce "noise".  I attempted to contact the director of the NUFORC for guidance. However, he never responded to my communication, so the shape aggregations are my own educated guesses.

Finally, I was interested in plotting the UFO sighting data geographically. After a bit of experimentation I decided to use the Python plugin geopy to do reverse geocoding. dataframe_cleaner.py uses the google geocoding API through geopy to look up latitude and longitude data for each city, state element in the UFO report data. You will need to provide your own API key to run the script and you can get one from the [Google Cloud Platform](https://cloud.google.com). Google offers a free trial of 150,000 look-ups or two weeks free - not too shabby! (just don't go over your limits and forget to cancel)

dataframe_cleaner.py will write the following two files to disk:

```
ufo_reports.csv and ll.csv
```

ufo_reports.csv contains all of the UFO report data along with the corrections and ll.csv contains all the latitude and longitude data.

#### move_list_cleanup.py

### And coding style tests

Explain what these tests test and why

```
Give an example
```

## Deployment

Add additional notes about how to deploy this on a live system

## Built With

* [Dropwizard](http://www.dropwizard.io/1.0.2/docs/) - The web framework used
* [Maven](https://maven.apache.org/) - Dependency Management
* [ROME](https://rometools.github.io/rome/) - Used to generate RSS Feeds

## Contributing

Please read [CONTRIBUTING.md](https://gist.github.com/PurpleBooth/b24679402957c63ec426) for details on our code of conduct, and the process for submitting pull requests to us.

## Versioning

We use [SemVer](http://semver.org/) for versioning. For the versions available, see the [tags on this repository](https://github.com/your/project/tags). 

## Authors

* **Billie Thompson** - *Initial work* - [PurpleBooth](https://github.com/PurpleBooth)

See also the list of [contributors](https://github.com/your/project/contributors) who participated in this project.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* Hat tip to anyone whose code was used
* Inspiration
* etc

