# -*- coding: utf-8 -*-
"""
Created on Thu Apr 22 10:35:14 2021

@author: kasia
"""
from tkinter import ttk
import requests, json
import io
import base64
import tkinter as tk
from urllib.request import urlopen
    
class Weather:
    def __init__(self,city_name="Valkeakoski"):
        self.city_name = city_name
       
    def Info(self):
        city = self.city_name
        API="dea8606011466582c84e077dca3eb13d"
        base_url = "http://api.openweathermap.org/data/2.5/weather?"
        url=base_url +"&q="+city+"&units=metric&mode=json&appid="+API
        response = requests.get(url)
        data=response.json()
        return data
    
    def Location(self):
        loc = self.Info()["name"]
        country = self.Info()["sys"]["country"]
        coordinates_lat = self.Info()["coord"]["lon"]
        coordinates_lon = self.Info()["coord"]["lat"]
        location = loc+", "+country+" ( "+ "longitude: "+ str(coordinates_lon)+" & latitude "+str(coordinates_lat) +" )"
        return location
        
#weather - icon, type, desctibiton      
    def Icon(self):
        icon_id = self.Info()["weather"][0]['icon']
        url_icon = "http://openweathermap.org/img/wn/"+icon_id+"@2x.png"
        image_byt = urlopen(url_icon).read()
        image_b64 = base64.encodestring(image_byt)
        icon = tk.PhotoImage(data=image_b64)    
        return icon

    def Describtion(self):   
        weather=self.Info()["weather"]
        weather_describtion = weather[0]['description']
        #print(weather_describtion)#scattered claouds
        return weather_describtion
    
    def Type(self):
        weather =self.Info()["weather"]
        weather_type = weather[0]['main']
        #print(weather_type)#Clouds
        return weather_type
        
#main - temp, fells like, min, max        
    def Temperature(self):
        main =self.Info()["main"]
        temperature = main['temp']
        #print(tempreture)
        return str(temperature)
    
    def WindSpeed(self):
        wind = self.Info()["wind"]["speed"]
        windSpeed = str(wind)+" km/h"
        return windSpeed
    
    def Pressure(self):
        pressure = self.Info()["main"]['pressure']
        pressure_value = str(pressure)+ ' hPa'
        return pressure_value
    
    def TempMin(self):
        tempMin = self.Info()['main']['temp_min']
        temp = str(tempMin)+' *C'
        return temp
    
    def TempMax(self):
        tempMax = self.Info()['main']['temp_max']
        temp = str(tempMax)+' *C'   
        return temp
    
    def Humidity(self):
        hum = self.Info()['main']['humidity']
        humidity = str(hum)+' %'
        return humidity
  
#Weather("Valkeakoski").Pressure()     
'''
tempreture_info = data["main"]
    weather_type = weather[0]['main'] #rain
     #light rain
    icon_id = weather[0]['icon']
    #city = input("enter city:")
# create a white canvas
cv = tk.Canvas(bg='white')
cv.pack(side='top', fill='both', expand='yes')

# put the image on the canvas with
# create_image(xpos, ypos, image, anchor)
cv.create_image(10, 10, image=photo, anchor='nw')
'''
