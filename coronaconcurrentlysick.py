#Number of concurrently sick from data from JHU github
#Computes the difference of detected infected minus recovered minus deaths
#Gerald Schuller, May 2020

import numpy as np
import matplotlib.pyplot as plt


#Read data from github:
import urllib.request
import pandas as pd

Retrievedata=True

#Cases
if Retrievedata:
   url = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv'
   urllib.request.urlretrieve(url, './corona_cases.csv')
#('./corona_cases.csv', <http.client.HTTPMessage object at 0x7fc7d89c0f98>)
   url = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_recovered_global.csv'
   urllib.request.urlretrieve(url, './corona_recovered.csv')
   url = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv'
   urllib.request.urlretrieve(url, './corona_deaths.csv')

countries = ['Italy', 'Germany', 'Spain', 'Brazil', 'US', 'Russia','Korea, South', 'Austria', 'Lebanon', 'Sweden','Chile']#, 'Ukraine']
population=[60.36, 83.02, 46.94, 209.5, 328.2, 144.5, 51.64, 8.859, 6.849, 10.23, 18.73]#, 42]
#countries = ['Germany', 'US']
#population=[60.36, 328.2]

print("countries=", countries)

#detected cases:
df = pd.read_csv('./corona_cases.csv')
#df.head()
df=df.drop(['Lat','Long','Province/State'], axis=1)
df=df.set_index('Country/Region')
datacases=df.loc[countries,: ]

#recovered cases:
df = pd.read_csv('./corona_recovered.csv')
#df.head()
df=df.drop(['Lat','Long','Province/State'], axis=1)
df=df.set_index('Country/Region')
datarecovered=df.loc[countries,: ]

#death cases:
df = pd.read_csv('./corona_deaths.csv')
#df.head()
df=df.drop(['Lat','Long','Province/State'], axis=1)
df=df.set_index('Country/Region')
datadeaths=df.loc[countries,: ]

startdate='3/1/20'

dates=datacases.loc[countries[0],startdate:].index
#print("dates=\n",dates)

countrycases=datacases.loc[countries,startdate:].reset_index(drop=True)
countrycases=np.array(countrycases)
countryrecovered=datarecovered.loc[countries,startdate:].reset_index(drop=True)
countryrecovered=np.array(countryrecovered)
countrydeaths=datadeaths.loc[countries,startdate:].reset_index(drop=True)
countrydeaths=np.array(countrydeaths)
concurrentlysick=countrycases-countryrecovered-countrydeaths #factor of increase f for each country

fig, ax = plt.subplots(1,1) 
ax.plot(dates,concurrentlysick.T)
ax.set_xticks(np.arange(0,len(dates),10))
plt.xticks(rotation=45)
#plt.plot(concurrentlysick.T)
plt.legend(countries)
plt.xlabel('Day since '+startdate)
plt.ylabel('Concurrently sick')
plt.grid()
plt.title('Concurrently sick internationally')
#plt.axis([1,31,0, 2])
#plt.show()
#plt.figure()

#print("concurrentlysick.T.shape", concurrentlysick.T,"population.shape", population)
fig, ax = plt.subplots(1,1) 
ax.plot(dates,concurrentlysick.T/population)
ax.set_xticks(np.arange(0,len(dates),10))
plt.xticks(rotation=45)
#plt.plot(concurrentlysick.T/population)
plt.legend(countries)
plt.xlabel('Day since '+startdate)
plt.ylabel('Concurrently sick')
plt.grid()
plt.title('Concurrently sick per Million Inhabitants internationally')
#plt.axis([1,31,0, 2])
#plt.show()
#plt.figure()

fig, ax = plt.subplots(1,1) 
ax.plot(dates,countrydeaths.T/population)
ax.set_xticks(np.arange(0,len(dates),10))
plt.xticks(rotation=45)
#plt.plot(countrydeaths.T/population)
plt.legend(countries)
plt.xlabel('Day since '+startdate)
plt.ylabel('Death cases')
plt.grid()
plt.title('Death cases per Million Inhabitants internationally')
#plt.axis([1,31,0, 2])
#plt.show()
#plt.figure()

currsickfactorsofincrease=concurrentlysick[:,1:]/concurrentlysick[:,:-1] #factor of increase f for each country
fig, ax = plt.subplots(1,1) 
ax.plot(dates[1:],currsickfactorsofincrease.T)
#ax.set_xticks(np.arange(0,len(dates[1:]),10))
plt.xticks(rotation=45)
plt.plot(currsickfactorsofincrease.T)
plt.legend(countries)
plt.xlabel('Day since '+startdate)
plt.ylabel('Factor of increase')
plt.grid()
plt.title('Factor of increase of concurrently sick')
#plt.axis([1,31,0, 2])
plt.axis([len(dates)-14, len(dates),0.7, 1.2])
plt.show()
