#Modules
import streamlit as st
import requests
from datetime import datetime
import pandas as pd
from streamlit.proto.Markdown_pb2 import Markdown
import logging
from credentials import API_KEY



hide_st_style = """
            <style>
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)


#API KEY - Stored in .WeatherAPP folder
api_key = API_KEY
#API CALL - OPENWEATHER
openweather_api_url = "api.openweathermap.org/data/2.5/weather?q={}&appid={}"
openweather_api_map_url = "https://api.openweathermap.org/data/2.5/onecall/timemachine?lat={}&lon={}&dt={}&appid={}"


#Function to fetch the latest data(Weather data)

def getweather(city):
    try:
        result = requests.get("http://"+ openweather_api_url.format(city,api_key))
        if result: # if we get data back from the request
            json = result.json()
            country = json["sys"]["country"]
            temp = json["main"]["temp"] - 273.35
            temp_feels = json["main"]['feels_like'] - 273.35
            humid = json["main"]["humidity"] - 273.15
            icon = json["weather"][0]["icon"]
            lon = json["coord"]['lon']
            lat = json["coord"]["lat"]
            desc = json["weather"][0]["description"]
            temp_max = json["main"]["temp_max"] - 273.35
            temp_min = json["main"]["temp_min"] - 273.35
            sunrise = json["sys"]["sunrise"]
            sunset = json["sys"]["sunset"]
            res = [country, round(temp,1),round(temp_feels,1),
            humid,lon,lat,icon,desc,round(temp_min,1), round(temp_max,1),sunrise,sunset]

            return res, json
    except ValueError as e:
        logging.warning("City Not Found")
        return None


#getweather(city_id)
@st.cache
def get_hist_data(lat,lon,start):
    res = requests.get("http://" + openweather_api_map_url.format(lat,lon,start,api_key))
    data = res.json()
    temp = []

    for hour in data["hourly"]:
        t = hour["temp"]
        temp.append(t)
    return data, temp




#data_required = getweather(city_id)
#get_hist_data(data_required["lat"],data_required["lon"])

st.title("Weather Web Application")
#make 2 columns

col1, col2 = st.columns(2)
with col1:
    city_name = st.text_input("Please enter the city name")
    with col2:
        if city_name:
            if getweather(city_name) is not None:
            
                res, json = getweather(city_name)
                st.success("Current: " + str(round(res[1],2)))
                st.info("Feels like: " + str(round(res[2],2)))
                st.subheader("Status: " + res[7])
                web_str = "![Alt Text]"+"(http://openweathermap.org/img/wn/"+res[6]+"@2x.png)"
                st.markdown(web_str)
            else:
                st.error("Please enter a valid city name")
    
if city_name:
    show_hist = st.expander(label= "More Information")
    with show_hist:
        if getweather(city_name) is not None:
        #start_date_string = st.date_input(label = "Enter the date")
            temp_min_col, temp_max_col = st.columns(2)
            temp_min_col.metric(label="Temperature min", value=res[8])
            temp_max_col.metric(label="Temperature max", value=res[9])
            sunset, sunrise = st.columns(2)
            sunset.metric(label="Sunrise", value=datetime.utcfromtimestamp(res[10]).strftime('%H:%M:%S'))
            sunrise.metric(label="Sunrise", value=datetime.utcfromtimestamp(res[11]).strftime('%H:%M:%S'))

        #map the location using the lat and loon we got from openweather
            st.map(pd.DataFrame({"lat": [res[5]], "lon": [res[4]]}, columns = ["lat", "lon"]))