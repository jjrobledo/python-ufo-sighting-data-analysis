import urllib2
from bs4 import BeautifulSoup
import re
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

 
# Read the web page and create a beautiful soup object
html = urllib2.urlopen('http://www.homeatlastdogrescue.com/adoptable//index.php')
bsObj = BeautifulSoup(html, 'html5lib')

''' getDogLinks() will search a Beautiful Soup object for "a" elements for links
that match the specified regular expression. The links are then individually appended
to an array. The function will return an array of link addresses.'''
def getDogLinks():
    dogLinks = []
    for link in bsObj.findAll('a', href=re.compile("(dog_desc.)+[a-zA-Z0-9?=]*")):
        dogLinks.append(link.attrs['href'])
    return dogLinks
''' parseDogLinks() will take the link for each dog page in getDogLinks() and search 
thier h3 tag for information relating to their sex and breed and store that data in 
an array. The function will return an array for the sexes of adoptable dogs and an 
array of adoptable dog breeds.'''
def parseDogLinks():
    sex = []
    breed = []
    for link in getDogLinks():
        dogHtml = urllib2.urlopen('http://www.homeatlastdogrescue.com/adoptable/' + link )
        dogSoup = BeautifulSoup(dogHtml, 'html5lib')
        for heading in dogSoup.findAll('h3'):
            if 'Male' in str(heading):
                sex.append('m')
            elif 'Female' in str(heading):
                sex.append('f')
            # Using re.sub here to select to 'inverse' of the regex. This probably isn't kosher by regex standards but it works (I wanted to use a negative look ahead (?!) but it wouldn't work).
            breed.append(re.sub(r'(<\/*h3>|Baby|Young|Adult|Senior|Female|Male)', "",str(heading)))
    # Clean up breed names
    breed = [breed.strip(' ') for breed in breed]
    breed = [breed.rstrip('\n') for breed in breed]
    del breed[0:2]
    return sex, breed
sex, breed = parseDogLinks()  

# Question 2
''' adoptable_breeds creates a pandas dataframe and fills it with breed names as the index
and the number of adoptable dogs per those breeds in the columns. The function will
return a pandas data frame.'''
def adoptable_breeds():
    breeds = np.array(breed)
    adoptable_by_breed = pd.DataFrame(index=np.unique(breeds), columns={'Number of adoptable dogs'})
    for i in adoptable_by_breed.index:
        adoptable_by_breed.loc[i, 'Number of adoptable dogs'] = breed.count(i)
    return adoptable_by_breed

adoptable_by_breed = adoptable_breeds()
# Plot a graph that represents the number of adoptable dogs by breed
yticks = np.arange(0, 12, 2)
adoptable_by_breed.plot(x=adoptable_by_breed.index, y='Number of adoptable dogs', kind='bar',
title='Number of Adoptable Dogs by Breed', yticks=yticks)
plt.xlabel('Breed')
plt.ylabel('Number of adoptable dogs')
#plt.show()

# Question 3
total_adoptable_dogs = float(len(breed)) # The len() of breed should be the total number of dogs
num_lab_mix = np.sum(pd.Series(breed).str.contains('.*(Labrador).*')) # .str.contains will search a pandas series and accepts a regular expression. To make this happen breeds is cast to a series.
percent_lab_mix = num_lab_mix / total_adoptable_dogs
num_nacho_dog = np.sum(pd.Series(breed).str.contains('.*(Chihuahua).*')) # Because who wants to spell Chihuahua every time...
percent_nacho = num_nacho_dog / total_adoptable_dogs
# There are 13 Labrador or Labrador Mixes up for adoption. This represents 13.8% of the total adoptable dogs.
# There are 15 Chihuahuas or Chihuahua Mixes up for adoption. This represents 15.9% of the total adoptable dogs.