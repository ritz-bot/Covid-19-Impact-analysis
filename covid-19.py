from __future__ import print_function

import pandas as pd
import numpy as np

from ipywidgets import interact, interactive, fixed, interact_manual
import ipywidgets as widgets


death = pd.read_csv("https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv")
confirmed = pd.read_csv("https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv")
recovered = pd.read_csv("https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_recovered_global.csv") 
country = pd.read_csv("https://raw.githubusercontent.com/CSSEGISandData/COVID-19/web-data/data/cases_country.csv")

death.head()
confirmed.head()
recovered.head()
country.head()

#data cleaning - renaming
country.columns = map(str.lower, country.columns)
confirmed.columns = map(str.lower, confirmed.columns)
recovered.columns = map(str.lower, recovered.columns)
death.columns = map(str.lower, death.columns)

confirmed = confirmed.rename(columns = {'province/state' : 'state', 'country/region' : 'country'})
country = country.rename(columns = {'country_region' : 'country'})
death = death.rename(columns = {'province/state' : 'state', 'country/region' : 'country'})
recovered = recovered.rename(columns = {'province/state' : 'state', 'country/region' : 'country'})


sorted_country = country.sort_values('confirmed', ascending = False).head(10)

sorted_country

def color(x):
    g = 'background-color : grey'
    y = 'background-color : yellow'
    r = 'background-color : red'
    temp = pd.DataFrame('', index = x.index, columns = x.columns)
    temp.iloc[:,4] = y
    temp.iloc[:,5] = r
    temp.iloc[:,6] = g
    return temp

sorted_country.style.apply(color, axis = None)

import plotly.express as px

fig = px.scatter(sorted_country.head(10), x='country', y='confirmed', size='confirmed', color='country', hover_name="country", size_max=60)

fig.show()

import plotly.graph_objects as go

def plot_country(country):
    labels = ['confirmed', 'deaths']
    colors = ['blue', 'red']
    mode_size = [6,8]
    line_size = [4,5]

    list_l = [confirmed, death]

    fig = go.Figure()
    
    for i, df in enumerate(list_l):
        if country == 'World' or country == 'world':
            x_data = np.array(list(df.iloc[:,5:].columns))
            y_data = np.sum(np.asarray(df.iloc[:, 5:]), axis = 0)
        else:
            x_data = np.array(list(df.iloc[:,5:].columns))
            y_data = np.sum(np.asarray(df[df['country'] == country].iloc[:,5:]), axis = 0)

        fig.add_trace(go.Scatter(x = x_data, y = y_data, mode = 'lines+markers', 
                                 name = labels[i], line = dict(color = colors[i], width = line_size[i]),
                                 connectgaps = True,
                                 text = "TOTAL " + str(labels[i]) + ": " + str(y_data[-1])))
    fig.show()
        
interact(plot_country, country='World');

import folium

world_map = folium.Map(location=[11,0], tiles="cartodbpositron", zoom_start=2, max_zoom = 6, min_zoom = 2)


for i in range(0,len(confirmed)):
    folium.Circle(
        location=[confirmed.iloc[i]['lat'], confirmed.iloc[i]['long']],
        fill=True,
        radius=(int((np.log(confirmed.iloc[i,-1]+1.00001)))+0.2)*50000,
        color='red',
        fill_color='indigo',
        tooltip = "<div style='margin: 0; background-color: black; color: white;'>"+
                    "<h4 style='text-align:center;font-weight: bold'>"+confirmed.iloc[i]['country'] + "</h4>"
                    "<hr style='margin:10px;color: white;'>"+
                    "<ul style='color: white;;list-style-type:circle;align-item:left;padding-left:20px;padding-right:20px'>"+
                        "<li>Confirmed: "+str(confirmed.iloc[i,-1])+"</li>"+
                        "<li>Deaths:   "+str(death.iloc[i,-1])+"</li>"+
                        "<li>Death Rate: "+ str(np.round(death.iloc[i,-1]/(confirmed.iloc[i,-1]+1.00001)*100,2))+ "</li>"+
                    "</ul></div>",
        ).add_to(world_map)

world_map













