# an example plugin

import tkinter as tk
import requests
import webbrowser

class PluginWindow:
    def __init__(self, root):
        self.root = root
        self.article_title, self.article_url = self.get_random_wikipedia_article()
        self.button = tk.Button(root, text=f"Read today: {self.article_title}", command=self.open_article)

    # json stuff
    def get_random_wikipedia_article(self):
        S = requests.Session()
        URL = "https://pl.wikipedia.org/w/api.php"

        SEARCHPAGE = {
            "action": "query",
            "format": "json",
            "generator": "random",
            "grnnamespace": 0,
            "prop": "info",
            "inprop": "url"
        }

        response = S.get(url=URL, params=SEARCHPAGE)
        data = response.json()

        page = next(iter(data['query']['pages'].values()))
        title = page['title']
        fullurl = page['fullurl']

        return title, fullurl

    def open_article(self):
        webbrowser.open(self.article_url)