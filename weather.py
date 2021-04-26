# -*- coding: utf-8 -*-
"""
Created on Thu Apr 22 10:35:14 2021

@author: kasia
"""
import requests, json
city = input("enter city:")
API="dea8606011466582c84e077dca3eb13d"
base_url = "http://api.openweathermap.org/data/2.5/weather?"
url=base_url +"&q="+city+"&units=metric&mode=json&appid="+API
response = requests.get(url)
x=response.json()

y = x["main"]
current_temperature = str(y["temp"])
z = x["weather"]
weather_description = str(z[0]["description"])

def get_temperature():
    print("temperature:"+current_temperature)
get_temperature()
def get_describtion():
    print("descr:"+weather_description)
get_describtion()
    
try:
    import tkinter as tk
    from tkinter import ttk
except ImportError:
    import Tkinter as tk
    import ttk


root = tk.Tk()
lab=tk.Label(root,text=weather_description+current_temperature)
lab.pack()

root.mainloop()