#!/usr/bin/env python
# coding: utf-8

# # Importing libraries needed for this assigment

# In[27]:


import requests
import lxml.html as lh
import bs4 as bs
import urllib.request
import numpy as np 
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import folium
from geopy.geocoders import Nominatim


# # Scraping the data from the Wikipedia Page

# In[28]:


url = "https://en.wikipedia.org/wiki/List_of_postal_codes_of_Canada:_M"
res = requests.get(url)
soup = bs.BeautifulSoup(res.content,'lxml')
table = soup.find_all('table')[0]
df = pd.read_html(str(table))
data = pd.read_json(df[0].to_json(orient='records'))
data.head()


# # Filtering dataset for boroughs with 'Not Assigned'

# In[30]:


data1=data.loc[data['Borough']!="Not assigned"]
data1.reset_index(inplace = True)
data1.drop(columns=['index'], inplace = True)
data1.head()


# # Importing Latitude and Longitude Data

# In[32]:


geourl="http://cocl.us/Geospatial_data"
geodata=pd.read_csv(geourl)
geodata.head()


# # Merging the datasets

# In[34]:


data2 = data1.merge(geodata,on='Postal Code')
data2.head()


# # Getting Longitudes and Lattitudes of Toronto

# In[35]:


address = 'Toronto, CA'
geolocator = Nominatim(user_agent="ny_explorer")
location = geolocator.geocode(address)
latitude = location.latitude
longitude = location.longitude
print('The geograpical coordinate of Toronto City are {}, {}.'.format(latitude, longitude))


# # Creating Neighbourhood Maps

# In[39]:


map_toronto = folium.Map(location=[latitude, longitude], zoom_start=10)

# add markers to map
for lat, lng, borough, neighbourhood in zip(data2['Latitude'], data2['Longitude'], data2['Borough'], data2['Neighbourhood']):
    label = '{}, {}'.format(neighbourhood, borough)
    label = folium.Popup(label, parse_html=True)
    folium.CircleMarker(
        [lat, lng],
        radius=5,
        popup=label,
        color='blue',
        fill=True,
        fill_color='#3186cc',
        fill_opacity=0.7,
        parse_html=False).add_to(map_toronto)  
    
map_toronto


# In[40]:


data2.shape


# In[ ]:




