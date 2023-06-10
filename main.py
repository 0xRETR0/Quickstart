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

# zbieramy informacje wstępne
username = os.getlogin()
plugin_windows = []
plugins_folder = f'C:/Users/{username}/SzybkiStart/plugins'
if not os.path.exists(plugins_folder):
    os.makedirs(plugins_folder)
if not os.path.exists(f'C:/Users/{username}/SzybkiStart/'):
    os.makedirs(f'C:/Users/{username}/SzybkiStart/')

# wszyskie funkcje odpowiedzialne za działanie programu
# wsparcie dla wtyczek, wczytujemy i ustalamy położenie pluginów
def load_plugins(y_start):
    plugin_folder = f"C:/Users/{username}/SzybkiStart/plugins"
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

# zrzucamy informacje o aplikacji użytkownika do pliku .json w folderze utworzonym w katalogu użytkownika
def save_app_path_and_name(path, name):
    with open(f'C:/Users/{username}/SzybkiStart/app_path.json', 'w') as f:
        json.dump({'path': path, 'name': name}, f)

# wczytujemy wcześniej zrzucone informacje
def load_app_path_and_name():
    try:
        with open(f'C:/Users/{username}/SzybkiStart/app_path.json', 'r') as f:
            data = json.load(f)
            return data['path'], data['name']
    except:
        return None, None
def load_app_name():
    try:
        with open(f'C:/Users/{username}/SzybkiStart/app_path.json', 'r') as f:
            data = json.load(f)
            return data['name']
    except:
        return None, None

# otwieramy aplikację wybraną przez użytkownika
def open_app():
    app_path = load_app_path_and_name()
    if app_path:
        subprocess.Popen(app_path)

# wybór aplikacji do otworzenia z programu
def app_path_and_name():
    app_path = filedialog.askopenfilename()
    if app_path:
        app_name = simpledialog.askstring("Dodaj Aplikację", "Wprowadź nazwę aplikacji:")
        save_app_path_and_name(app_path, app_name)
        app_name_label.config(text=app_name)
        open_app()

# zbieramy dane pogodowe używając API OpenWeatherMap 
def get_weather():
    api_key = '15e7a67f2c8b6dc6096d5a8afced4210'
    city = 'Wroclaw'
    country_code = 'PL'
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
        image_label.image = photo  # zapobiegamy usunięciu zdjęcia

        weather_text = f'Temperatura: {temperature:.1f}°C\nPogoda: {description}'

    except KeyError:
        weather_text = f'Nie udało się uzyskać danych pogodowych. \nSpróbuj ponownie później.'
        icon_data = None

    weather_label.config(text=weather_text)

# wyświetlamy aktualną godzinę
def time():
    czas = strftime('%H:%M:%S')
    tekst.config(text=f"Witaj, {username}. Jest {czas}.", font=("Arial", 24))
    tekst.after(1000, time)

def open_app():
    # sprawdzamy czy istnieje już nazwa i ścieżka aplikacji i wyświetla odpowiedni napis na przycisku
    nazwa_aplk = load_app_name()
    if nazwa_aplk and nazwa_aplk !=(None, None):
        open_button.place(x=140, y=0)
        open_button.config(text=f"Otwórz {nazwa_aplk}")

# wszystko co odpowiedzialne za ustawienie widgetów i wygląd okna

root = tk.Tk()
root.title("Szybki Start")
root.geometry("512x512")
root.resizable(0, 0)

app_name_label = tk.Label(root, text="Nie wybrano aplikacji.")

rama_guziki = tk.Frame(root, width=512, height=255)
open_button = tk.Button(rama_guziki, text=f"Otwórz", command=open_app)
choose_button = tk.Button(rama_guziki, text="Wybierz nową aplikację", command=app_path_and_name)

rama_pogoda = tk.Frame(root, width=512, height=200)
rama_pogoda.place(x=0, y=25)

weather_label = tk.Label(rama_pogoda, font=('Arial', 16))
button = tk.Button(rama_pogoda, text="Odśwież", font=('Arial', 16), command=get_weather)

image_label = tk.Label(rama_pogoda)
tekst = tk.Label(root, text="", font=("Arial", 24))
tekst.place(x=15, y=15)

weather_label.place(x=15, y=50 + tekst.winfo_height() + 5)
button.place(x=15, y=weather_label.winfo_height() + 120)

tekst2 = tk.Label(root, text="Twoje aplikacje:", font=("Arial", 18))
tekst2.place(x=15, y=210)

choose_button.place(x=0, y=0)
rama_guziki.place(x=15, y=255)

tekst_plugin = tk.Label(root, text="Twoje pluginy:", font=("Arial", 18))
if len(os.listdir(plugins_folder)) > 0:
    tekst_plugin.place(x=15, y=300)

open_app()

get_weather()

# sprawdzamy czy istnieje obrazek pogody i jeśli tak, to go wyświetlamy
if icon_data is not None:
    image_label.place(x=weather_label.winfo_width() + 230, y=50 + tekst.winfo_height())

time()

# kilka procesów odpowiedzialnych za poprawne wyświetlenie widgetów pluginów
root.update_idletasks()
last_widget = tekst_plugin
y_start = last_widget.winfo_y() + last_widget.winfo_height() + 5
load_plugins(y_start)

root.mainloop()
