# importing libraries
import folium
import pandas as pd
import requests
from pandas import DataFrame
import requests
from bs4 import BeautifulSoup
##from tabulate import tabulate
import os
import numpy as np
import matplotlib.pyplot as plt

def color_producer(acs):
    if acs < 1000:
        return 'green'
    elif acs >= 1000 and acs < 10000:
        return 'orange'
    else:
        return 'red'

extract_contents = lambda row: [x.text.replace('\n', '') for x in row]
URL = 'https://www.mohfw.gov.in/'

SHORT_HEADERS = ['SNo', 'State', 'Active', 'Cured', 'Death','Total']

response = requests.get(URL).content
soup = BeautifulSoup(response, 'html.parser')

header = extract_contents(soup.tr.find_all('th'))

stats = []
all_rows = soup.find_all('tr')

for row in all_rows:
    stat = extract_contents(row.find_all('td'))

    if stat:
        if len(stat) == 5:
            # last row
            stat = ['', *stat]
            stats.append(stat)
        elif len(stat) == 6:
            stats.append(stat)

stats[-1][0] = len(stats)
stats[-5][1] = "Total Cases"

objects = []
for row in stats:
    objects.append(row[1])

y_pos = np.arange(len(objects))

performance = []
for row in stats[:len(stats) - 1]:
    performance.append(int(row[2]))


performance.append(int(stats[- 1][2][:len(stats[-1][2]) - 1]))

df= DataFrame(stats,columns=['SNo', 'State', 'Active', 'Cured', 'Death','Total'])
df= df[0:35]
print(len(df))
df["Latitude"]  = ['11.66702557','14.7504291','27.10039878','26.7499809','25.78541445','30.71999697','22.09042035','20.26657819','28.6699929',
                   '15.491997',
                   '22.309425','28.45000633','31.10002545','34.29995933','23.80039349','12.57038129','8.900372741','34.209515',
                   '21.30039105','19.25023195','24.79997072','25.57049217','23.71039899','25.6669979','19.82042971','11.93499371',
                   '31.51997398','26.44999921','27.3333303','12.92038576','17.123184', '23.83540428','30.316496','27.59998069','22.58039044']

df["Longitude"] = ['92.73598262','78.57002559','93.61660071','94.21666744','87.4799727','76.78000565','82.15998734','73.0166178','77.23000403', '73.81800065',
                   '72.136230','77.01999101','77.16659704','74.46665849','86.41998572','76.91999711','76.56999263','77.615112',
                   '76.13001949','73.16017493','93.95001705','91.8800142','92.72001461','94.11657019','85.90001746','79.83000037',
                   '75.98000281','74.63998124','88.6166475','79.15004187','79.208824','91.27999914','78.032188','78.05000565','88.32994665']

lat  = list(df["Latitude"])
lon  = list(df["Longitude"])
state= list(df["State"])
tcases= list(df["Total"])
acases= list(df["Active"])
dcases= list(df["Death"])
map = folium.Map(location=[27.10039878,93.61660071],tiles="Stamen Terrain")
fg= folium.FeatureGroup("Covid India Map")
for lt , ln, st,tcs,acs,dcs in zip(lat,lon,state,tcases,acases,dcases):
    fg.add_child(folium.CircleMarker(location=[lt,ln],radius=9,popup="State: %s \n Total Cases: %s \n Active Cases: %s \n Death: %s" %(str(st),str(tcs),str(acs),str(dcs)),
    fill_color=color_producer(int(acs)),color='grey',fill_opacity=0.7))

map.add_child(fg)
map.add_child(folium.LayerControl())
map.save("Map2.html")
