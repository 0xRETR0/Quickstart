# bardzo krótki plugin demonstracyjny

import tkinter as tk
import webbrowser

class PluginWindow:
    def __init__(self, root):
        self.root = root
        self.button = tk.Button(root, text="Otwórz przykładową stronę internetową", command=self.open_example)

    def open_example(self):
        webbrowser.open("http://example.com")

