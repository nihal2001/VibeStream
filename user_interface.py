import tkinter as tk
import pyodbc

class UserInterface:
    def __init__(self, master, connection):

        self.master = master
        self.create_widgets()
        # pyodbc connection
        conn = connection

    def create_widgets(self):
        # Search bar
        tk.Label(self.master, text="Search:").pack()
        self.search_entry = tk.Entry(self.master)
        self.search_entry.pack()


        # Dropdown for search type
        self.search_category_var = tk.StringVar(self.master)
        self.search_category_var.set("Song")
        self.search_category_menu = tk.OptionMenu(self.master, self.search_category_var, "Song", "Artist", "Album", "Playlist")
        self.search_category_menu.pack()

        # Search button
        self.search_button = tk.Button(self.master, text="Search", command=self.perform_search)
        self.search_button.pack(pady=10)

        self.result_list = tk.Listbox(self.master)
        self.result_list.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

    def perform_search(self):
        # Get the search query from the entry widget
        search_query = self.search_entry.get()

        print(f"Searching for: {search_query}")