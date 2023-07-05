# very short demo plugin

import tkinter as tk
import webbrowser

class PluginWindow:
    def __init__(self, root):
        self.root = root
        self.button = tk.Button(root, text="Open an example website", command=self.open_example)

    def open_example(self):
        webbrowser.open("http://example.com")

