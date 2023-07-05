import tkinter as tk
from tkinter import filedialog
from tkinter import simpledialog
import requests
from PIL import Image, ImageTk
import io
import os
import subprocess
import json
import time
from time import strftime
import importlib
import sys

# getting all the necessary info
username = os.getlogin()
plugin_windows = []
plugins_folder = f'C:/Users/{username}/quickstart/plugins'
if not os.path.exists(plugins_folder):
    os.makedirs(plugins_folder)
if not os.path.exists(f'C:/Users/{username}/quickstart/'):
    os.makedirs(f'C:/Users/{username}/quickstart/')

# plugin support
def load_plugins(y_start):
    plugin_folder = f"C:/Users/{username}/quickstart/plugins"
    sys.path.append(plugin_folder)
    plugin_files = [f for f in os.listdir(plugin_folder) if f.endswith(".py")]

    def place_plugin_buttons(y_start):
        highest_y = y_start

        for plugin_file in plugin_files:
            plugin_module = plugin_file[:-3] 
            try:
                plugin = importlib.import_module(plugin_module)
                plugin_class = getattr(plugin, "PluginWindow")
                plugin_window = plugin_class(root)
                plugin_window.button.place(x=15, y=highest_y)
                plugin_windows.append(plugin_window)

                root.update_idletasks()

                highest_y = plugin_window.button.winfo_y() + plugin_window.button.winfo_height() + 5
            except Exception as e:
                print(f"Wystąpił błąd podczas wczytywania pluginu '{plugin_module}': {e}")

    place_plugin_buttons(y_start)

# dumping data for the app launcher into a .json
def save_app_path_and_name(path, name):
    with open(f'C:/Users/{username}/quickstart/app_path.json', 'w') as f:
        json.dump({'path': path, 'name': name}, f)

# loading the dumped info
def load_app_path_and_name():
    try:
        with open(f'C:/Users/{username}/quickstart/app_path.json', 'r') as f:
            data = json.load(f)
            return data['path'], data['name']
    except:
        return None, None
def load_app_name():
    try:
        with open(f'C:/Users/{username}/quickstart/app_path.json', 'r') as f:
            data = json.load(f)
            return data['name']
    except:
        return None, None

# launching user apps
def open_app():
    app_path = load_app_path_and_name()
    if app_path:
        subprocess.Popen(app_path)

# choosing apps to launch
def app_path_and_name():
    app_path = filedialog.askopenfilename()
    if app_path:
        app_name = simpledialog.askstring("Dodaj Aplikację", "Wprowadź nazwę aplikacji:")
        save_app_path_and_name(app_path, app_name)
        app_name_label.config(text=app_name)
        open_app()

# getting weather data using openweathermap api
def get_weather():
    api_key = '15e7a67f2c8b6dc6096d5a8afced4210'
    city = 'REPLACE WITH YOUR CITY (or the closest large town if you live in bumfuck nowhere, no special symbols)'
    country_code = 'REPLACE WITH YOUR COUNTRY CODE (eg. PL, US, GB)'
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city},{country_code}&appid={api_key}&units=metric&lang=pl'

    response = requests.get(url)

    global icon_data

    try:
        data = response.json()

        temperature = data['main']['temp']
        description = data['weather'][0]['description']
        icon_url = data['weather'][0]['icon']
        icon_response = requests.get(f'http://openweathermap.org/img/w/{icon_url}.png')
        icon_data = icon_response.content
        image = Image.open(io.BytesIO(icon_data))

        image = image.resize((64, 64))

        photo = ImageTk.PhotoImage(image)

        image_label.config(image=photo)
        image_label.image = photo  # making sure the photo doesn't get deleted by tkinter's optimalization or something

        weather_text = f'Temperature: {temperature:.1f}°C\nWeather: {description}'

    except KeyError:
        weather_text = f'Weather data unavailable. \nTry again later.'
        icon_data = None

    weather_label.config(text=weather_text)

# display current time
def time():
    czas = strftime('%H:%M:%S')
    tekst.config(text=f"Witaj, {username}. Jest {czas}.", font=("Arial", 24))
    tekst.after(1000, time)

def open_app():
    # checking what should be displayed at the launcher button
    nazwa_aplk = load_app_name()
    if nazwa_aplk and nazwa_aplk !=(None, None):
        open_button.place(x=140, y=0)
        open_button.config(text=f"Otwórz {nazwa_aplk}")

# all the spaghetti responsible for displaying stuff

root = tk.Tk()
root.title("Quickstart")
root.geometry("512x512")
root.resizable(0, 0)

app_name_label = tk.Label(root, text="No app chosen.")

rama_guziki = tk.Frame(root, width=512, height=255)
open_button = tk.Button(rama_guziki, text=f"Open", command=open_app)
choose_button = tk.Button(rama_guziki, text="Choose a new app", command=app_path_and_name)

rama_pogoda = tk.Frame(root, width=512, height=200)
rama_pogoda.place(x=0, y=25)

weather_label = tk.Label(rama_pogoda, font=('Arial', 16))
button = tk.Button(rama_pogoda, text="Refresh", font=('Arial', 16), command=get_weather)

image_label = tk.Label(rama_pogoda)
tekst = tk.Label(root, text="", font=("Arial", 24))
tekst.place(x=15, y=15)

weather_label.place(x=15, y=50 + tekst.winfo_height() + 5)
button.place(x=15, y=weather_label.winfo_height() + 120)

tekst2 = tk.Label(root, text="Your apps:", font=("Arial", 18))
tekst2.place(x=15, y=210)

choose_button.place(x=0, y=0)
rama_guziki.place(x=15, y=255)

tekst_plugin = tk.Label(root, text="Your plug-ins:", font=("Arial", 18))
if len(os.listdir(plugins_folder)) > 0:
    tekst_plugin.place(x=15, y=300)

open_app()

get_weather()

# making sure the icon actually exists
if icon_data is not None:
    image_label.place(x=weather_label.winfo_width() + 230, y=50 + tekst.winfo_height())

time()

# plugin stuff
root.update_idletasks()
last_widget = tekst_plugin
y_start = last_widget.winfo_y() + last_widget.winfo_height() + 5
load_plugins(y_start)

root.mainloop()
