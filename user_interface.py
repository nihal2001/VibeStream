import tkinter as tk
import pyodbc

class UserInterface:
    def __init__(self, master, connection, id):
        self.master = master
        self.conn = connection  # pyodbc connection
        self.user_id = id  # User_Id in Listener table
        self.create_widgets()

    def create_widgets(self):
        # Clear previous content
        for widget in self.master.winfo_children():
            widget.destroy()
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

        # Change Password button
        change_password_button = tk.Button(self.master, text="Change Password", command=self.show_change_password_page)
        change_password_button.pack(pady=10)

        sign_out_button = tk.Button(self.master, text="Sign out") # ADD here
        sign_out_button.pack(pady=10)

    def show_change_password_page(self):
        # Clear previous content
        for widget in self.master.winfo_children():
            widget.destroy()

        # New password field
        tk.Label(self.master, text="New Password:").pack()
        self.new_password_entry = tk.Entry(self.master, show="*")
        self.new_password_entry.pack()

        # Submit button
        submit_button = tk.Button(self.master, text="Submit")
        submit_button.pack(pady=10)

        # Back button
        back_button = tk.Button(self.master, text="Back", command=self.create_widgets)
        back_button.pack(pady=10)

    def perform_search(self):
        search_query = self.search_entry.get()
        search_category = self.search_category_var.get()
        search_query = f"%{search_query}%"

        if search_category == "Song":
            self.song_search(search_query)
        elif search_category == "Album":
            self.album_search(search_query)
        elif search_category == "Artist":
            self.artist_search(search_query)
        elif search_category == "Playlist":
            self.playlist_search(search_query)

    def song_search(self, search_query):
        sql_query = """
            SELECT Song.Song_ID, Song.Name, Artist.Name
            FROM Song
            JOIN Artist ON Song.Artist_ID = Artist.Artist_ID
            WHERE Song.Name LIKE ?
        """
        try:
            cursor = self.conn.cursor()
            cursor.execute(sql_query, (search_query,))
            results = cursor.fetchall()

            self.result_list.delete(0, tk.END)  # Clear existing results
            for row in results:
                display_text = f"{row[1]} by {row[2]}"
                self.result_list.insert(tk.END, display_text)
                self.result_list.bind('<<ListboxSelect>>', lambda e, song_id=row[0]: self.show_song_page(song_id))
        except pyodbc.Error as e:
            print(f"Database error: {e}")

    def album_search(self, search_query):
        sql_query = """
            SELECT Album.Album_ID, Album.Title, Artist.Name
            FROM Album
            JOIN Artist ON Album.Artist_ID = Artist.Artist_ID
            WHERE Album.Title LIKE ?
        """
        self.execute_search_query(sql_query, search_query, self.show_album_page)

    def artist_search(self, search_query):
        sql_query = "SELECT Artist_ID, Name FROM Artist WHERE Name LIKE ?"
        self.execute_search_query(sql_query, search_query, self.show_artist_page)

    def playlist_search(self, search_query):
        sql_query = """
            SELECT Playlist.Playlist_ID, Playlist.Name, Listener.Name
            FROM Playlist
            JOIN Listener ON Playlist.User_ID = Listener.User_ID
            WHERE Playlist.Name LIKE ?
        """
        self.execute_search_query(sql_query, search_query, self.show_playlist_page)

    def execute_search_query(self, sql_query, search_query, callback):
        try:
            cursor = self.conn.cursor()
            cursor.execute(sql_query, (search_query,))
            results = cursor.fetchall()

            self.result_list.delete(0, tk.END)  # Clear existing results
            self.results_data = {}  # Dictionary to store the mapping of list index to data

            for index, row in enumerate(results):
                display_text = " by ".join(filter(None, row[1:]))  # Join non-empty fields with 'by'
                self.result_list.insert(tk.END, display_text)
                self.results_data[index] = row[0]  # Store the id with index as key

            # Bind the selection event directly with the required logic
            self.result_list.bind('<<ListboxSelect>>', lambda event: self.handle_listbox_select(event, callback))

        except pyodbc.Error as e:
            print(f"Database error: {e}")

    def handle_listbox_select(self, event, callback):
        widget = event.widget
        index = int(widget.curselection()[0])
        selected_id = self.results_data[index]
        callback(selected_id)

    def show_album_page(self, album_id):
        # Clear previous content
        for widget in self.master.winfo_children():
            widget.destroy()

        try:
            cursor = self.conn.cursor()

            # Query to get album name and artist
            album_query = """
                SELECT Album.Title, Artist.Name
                FROM Album
                JOIN Artist ON Album.Artist_ID = Artist.Artist_ID
                WHERE Album.Album_ID = ?
            """
            cursor.execute(album_query, (album_id,))
            album_info = cursor.fetchone()

            if album_info:
                album_name, artist_name = album_info
                # Display album name and artist
                tk.Label(self.master, text=f"Album: {album_name}").pack()
                tk.Label(self.master, text=f"Artist: {artist_name}").pack()

                # Query to get songs in the album
                song_query = """
                    SELECT Song.Name
                    FROM AlbumSong
                    JOIN Song ON AlbumSong.Song_ID = Song.Song_ID
                    WHERE AlbumSong.Album_ID = ?
                """
                cursor.execute(song_query, (album_id,))
                songs = cursor.fetchall()

                # Display songs
                tk.Label(self.master, text="Songs:").pack()
                for song in songs:
                    tk.Label(self.master, text=song[0]).pack()

            # back button
            self.back_button = tk.Button(self.master, text="Back", command=self.create_widgets)
            self.back_button.pack(pady=10)

        except pyodbc.Error as e:
            print(f"Database error: {e}")

    def show_artist_page(self, artist_id):
        # Clear previous content
        for widget in self.master.winfo_children():
            widget.destroy()

        try:
            cursor = self.conn.cursor()

            # Query to get artist name
            artist_query = "SELECT Name FROM Artist WHERE Artist_ID = ?"
            cursor.execute(artist_query, (artist_id,))
            artist_info = cursor.fetchone()

            if artist_info:
                artist_name = artist_info[0]
                # Display artist name
                tk.Label(self.master, text=f"Artist: {artist_name}").pack()

                # Query to get songs by the artist
                song_query = "SELECT Name FROM Song WHERE Artist_ID = ?"
                cursor.execute(song_query, (artist_id,))
                songs = cursor.fetchall()

                # Display songs
                tk.Label(self.master, text="Songs:").pack()
                for song in songs:
                    tk.Label(self.master, text=song[0]).pack()
                
            # back button
            self.back_button = tk.Button(self.master, text="Back", command=self.create_widgets)
            self.back_button.pack(pady=10)

        except pyodbc.Error as e:
            print(f"Database error: {e}")

    def show_playlist_page(self, playlist_id):
        # Clear previous content
        for widget in self.master.winfo_children():
            widget.destroy()

        try:
            cursor = self.conn.cursor()

            # Query to get playlist name and creator
            playlist_query = """
                SELECT Playlist.Name, Listener.Name
                FROM Playlist
                JOIN Listener ON Playlist.User_ID = Listener.User_ID
                WHERE Playlist.Playlist_ID = ?
            """
            cursor.execute(playlist_query, (playlist_id,))
            playlist_info = cursor.fetchone()

            if playlist_info:
                playlist_name, creator_name = playlist_info
                # Display playlist name and creator
                tk.Label(self.master, text=f"Playlist: {playlist_name}").pack()
                tk.Label(self.master, text=f"Created by: {creator_name}").pack()

                # Query to get songs in the playlist
                song_query = """
                    SELECT Song.Name
                    FROM PlaylistSongs
                    JOIN Song ON PlaylistSongs.Song_ID = Song.Song_ID
                    WHERE PlaylistSongs.Playlist_ID = ?
                """
                cursor.execute(song_query, (playlist_id,))
                songs = cursor.fetchall()

                # Display songs
                tk.Label(self.master, text="Songs in Playlist:").pack()
                for song in songs:
                    tk.Label(self.master, text=song[0]).pack()

            # back button
            self.back_button = tk.Button(self.master, text="Back", command=self.create_widgets)
            self.back_button.pack(pady=10)

        except pyodbc.Error as e:
            print(f"Database error: {e}")


    def show_song_page(self, song_id):
        # Logic to display song page
        print(f"Song ID: {song_id}")