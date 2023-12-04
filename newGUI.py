# NOTE: 'user' and 'listener' are used interchangebly in reference to the code and database

import tkinter as tk
import pyodbc
import hashlib
from dbConnection import get_db_connection
# user_interface is only in charge of 'User' a.k.a 'Listener' in the DB
from user_interface import UserInterface


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Login System")
        self.geometry("600x400")
        self.role_menu = None
        # Connection to db
        self.open_B()

        # Initial screen setup
        self.create_initial_widgets()

    def create_initial_widgets(self):
        # Create a "Sign In" button
        sign_in_button = tk.Button(self, text="Sign In", command=self.show_sign_in_form)
        sign_in_button.pack(pady=10)

        # Create a "Sign Up" button (functionality not implemented yet)
        sign_up_button = tk.Button(self, text="Sign Up", command=self.show_sign_up_form)
        sign_up_button.pack(pady=10)

    def show_sign_in_form(self):
        # Clear the initial widgets
        for widget in self.winfo_children():
            widget.destroy()

        # Create username field
        tk.Label(self, text="Username").pack()
        self.username_entry = tk.Entry(self)
        self.username_entry.pack()

        # Create password field
        tk.Label(self, text="Password").pack()
        self.password_entry = tk.Entry(self, show="*")
        self.password_entry.pack()

        # Create selection field for user role
        tk.Label(self, text="Select Role").pack()
        self.role_var = tk.StringVar(self)
        self.role_var.set("user")  # default value
        self.role_menu = tk.OptionMenu(self, self.role_var, "user", "moderator", "artist")
        self.role_menu.pack()

        # Create a "Sign In" button
        sign_in_btn = tk.Button(self, text="Sign In", command=self.on_sign_in)
        sign_in_btn.pack(pady=10)

    def show_sign_up_form(self):
        # Clear the initial widgets
        for widget in self.winfo_children():
            widget.destroy()

        # Create username field
        tk.Label(self, text="Username").pack()
        self.username_entry = tk.Entry(self)
        self.username_entry.pack()

        # Create password field
        tk.Label(self, text="Password").pack()
        self.password_entry = tk.Entry(self, show="*")
        self.password_entry.pack()

        # Create Re-enter password field
        tk.Label(self, text="Re-enter Password").pack()
        self.password_re_entry = tk.Entry(self, show="*")
        self.password_re_entry.pack()

        # Create a "Sign Up" button
        sign_up_btn = tk.Button(self, text="Sign Up", command=self.on_sign_up)
        sign_up_btn.pack(pady=10)

    def on_sign_in(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        role = self.role_var.get()

        if role == "user":
            if self.authenticate_user(username, password):
                self.show_user_interface()
            else:
                print("Invalid username or password")
        elif role == "artist":
            if self.authenticate_artist(username, password):
                self.show_main_interface_artist()
            else:
                print("Invalid artist login")
        elif role == "moderator":
            if self.authenticate_moderator(username, password):
                self.show_main_interface()
            else:
                print("Invalid moderator login")
        else:
            print("Invalid role selected")


    def on_sign_up(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        password_re = self.password_re_entry.get()

        if password != password_re:
            print("Passwords do not match")
            return

        if self.register_user(username, password):
            print("User registered successfully")
            self.show_main_interface()
            
        else:
            print("Registration failed")

    # For moderators
    def show_main_interface(self):
        for widget in self.winfo_children():
            widget.destroy()
        self.title("Database Connection")

        self.button_frame = tk.Frame(self)
        self.button_frame.pack(padx=10, pady=10)

        # Management Frames (Initially Hidden)
        self.album_frame = AlbumManagementFrame(self)
        self.song_frame = SongManagementFrame(self)
        self.artist_frame = ArtistManagementFrame(self)
        self.listener_frame = ListenerManagementFrame(self)
        self.moderator_frame = ModeratorManagementFrame(self)
        self.playlist_frame = PlaylistManagementFrame(self)

        for frame in [
            self.album_frame,
            self.song_frame,
            self.artist_frame,
            self.listener_frame,
            self.moderator_frame,
            self.playlist_frame,
        ]:
            frame.pack(fill="both", expand=True)
            frame.pack_forget()  # Hide all initially

        # Management Buttons
        self.manage_album_btn = tk.Button(
            self, text="Manage Album", command=self.show_frame(self.album_frame)
        )
        self.manage_album_btn.pack(pady=10)

        self.manage_song_btn = tk.Button(
            self, text="Manage Song", command=self.show_frame(self.song_frame)
        )
        self.manage_song_btn.pack(pady=10)

        self.manage_artist_btn = tk.Button(
            self, text="Manage Artist", command=self.show_frame(self.artist_frame)
        )
        self.manage_artist_btn.pack(pady=10)

        self.manage_listener_btn = tk.Button(
            self, text="Manage Listener", command=self.show_frame(self.listener_frame)
        )
        self.manage_listener_btn.pack(pady=10)

        self.manage_moderator_btn = tk.Button(
            self, text="Manage Moderator", command=self.show_frame(self.moderator_frame)
        )
        self.manage_moderator_btn.pack(pady=10)

        self.manage_playlist_btn = tk.Button(
            self, text="Manage Playlist", command=self.show_frame(self.playlist_frame)
        )
        self.manage_playlist_btn.pack(pady=10)

        # Create 'Print Report' button
        self.print_report_btn = tk.Button(
            self.button_frame, text="Print Report", command=self.generate_report
        )
        self.print_report_btn.pack(side=tk.RIGHT, padx=10)

    def show_main_interface_artist(self):
        for widget in self.winfo_children():
            widget.destroy()
        self.title("Artist Connection")

        self.button_frame = tk.Frame(self)
        self.button_frame.pack(padx=10, pady=10)

        # Management Frames (Initially Hidden)
        self.album_frame = AlbumManagementFrame(self)
        self.song_frame = SongManagementFrame(self)
        

        for frame in [
            self.album_frame,
            self.song_frame,
            
        ]:
            frame.pack(fill="both", expand=True)
            frame.pack_forget()  # Hide all initially

        # Management Buttons
        self.manage_album_btn = tk.Button(
            self, text="Manage Album", command=self.show_frame(self.album_frame)
        )
        self.manage_album_btn.pack(pady=10)

        self.manage_song_btn = tk.Button(
            self, text="Manage Song", command=self.show_frame(self.song_frame)
        )
        self.manage_song_btn.pack(pady=10)

        # Change Password button
        change_password_button = tk.Button(self.master, text="Change Password") # TODO Hash then update db. Page can be taken from user_interface
        change_password_button.pack(pady=10)

        sign_out_button = tk.Button(self.master, text="Sign out") # TODO Page and functionality. 
        sign_out_button.pack(pady=10)

    def show_user_interface(self):
        for widget in self.winfo_children():
            widget.destroy()

        self.user_interface = UserInterface(self, self.conn, self.user_id)

    def show_frame(self, frame):
        def _show():
            # Hide main interface
            self.button_frame.pack_forget()
            for btn in [
                self.manage_album_btn,
                self.manage_song_btn,
                
            ]:
                btn.pack_forget()

            if(self.role_var.get() != 'artist'):
                for btn in [
                    self.manage_artist_btn,
                    self.manage_listener_btn,
                    self.manage_moderator_btn,
                    self.manage_playlist_btn,
                
                ]:
                    btn.pack_forget()
                

            # Show selected frame
            frame.pack(fill="both", expand=True)

        return _show

    def open_B(self):
        conn_str = (
            "Driver={ODBC Driver 17 for SQL Server};"
            "Server=tcp:cs4604server.database.windows.net,1433;"
            "Database=cs4604db;"
            "UID=cs4604;"
            "PWD=Oblong08!;"
            "Encrypt=yes;"
            "TrustServerCertificate=yes;"
        )
        try:
            pyodbc.drivers()
            self.conn = pyodbc.connect(conn_str)
            self.update_connection_status(True)
        except pyodbc.Error as e:
            print(f"Error: {e}")
            self.update_connection_status(False)

    def close_B(self):
        if self.conn:
            self.conn.close()
            self.update_connection_status(False)

    def generate_report(self):
        # Check if the database connection is open
        if not hasattr(self, "conn") or not self.conn:
            print("Connection is not open.")
            return

        report_window = tk.Toplevel(self)
        report_window.title("Report")
        report_window.geometry("300x700")

        try:
            cursor = self.conn.cursor()
            # Fetch data from database
            total_listeners = cursor.execute(
                "SELECT COUNT(*) FROM Listener"
            ).fetchone()[0]
            total_artists = cursor.execute("SELECT COUNT(*) FROM Artist").fetchone()[0]
            total_mods = cursor.execute("SELECT COUNT(*) FROM Moderator").fetchone()[0]
            total_songs = cursor.execute("SELECT COUNT(*) FROM Song").fetchone()[0]
            total_albums = cursor.execute("SELECT COUNT(*) FROM Album").fetchone()[0]

            total_users = total_artists + total_artists + total_mods

            # Display data in report window
            tk.Label(
                report_window, text=f"Total number of users: {total_users}\n\n"
            ).pack()
            tk.Label(
                report_window, text=f"Number of listeners: {total_listeners}"
            ).pack()
            tk.Label(report_window, text=f"Number of artists: {total_artists}").pack()
            tk.Label(report_window, text=f"Number of mods: {total_mods}\n\n").pack()
            tk.Label(report_window, text=f"Number of songs: {total_songs}").pack()
            tk.Label(report_window, text=f"Number of albums: {total_albums}\n\n").pack()

            # Fetch and display number of albums for each year
            cursor.execute(
                "SELECT YEAR(Release_date), COUNT(*) FROM Album GROUP BY YEAR(Release_date)"
            )
            for year, count in cursor.fetchall():
                tk.Label(report_window, text=f"Albums in {year}: {count}").pack()

        except pyodbc.Error as e:
            print(f"Error: {e}")

    def test_data(self):
        if not self.conn:
            print("Connection is not open.")
            self.update_connection_status(False)
            return
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM Song")
        rows = cursor.fetchall()
        # Process or display data as needed
        for row in rows:
            print(row)

    def update_connection_status(self, connected):
        if connected:
            print("connected")
        else:
            print("Not connected")

    def show_manage_album(self):
        # Hide main interface
        self.button_frame.pack_forget()
        self.manage_album_btn.pack_forget()
        # ... [Hide other elements] ...

        # Show Album management interface
        self.album_frame.pack(fill="both", expand=True)

    def hash_password(self, password):
        # Hash a password for storing.
        return hashlib.sha256(password.encode()).hexdigest()

    def register_user(self, username, password):
        hashed_password = self.hash_password(password)
        try:
            cursor = self.conn.cursor()
            cursor.execute(
                "INSERT INTO Listener (Name, Password) VALUES (?, ?)",
                (username, hashed_password),
            )
            self.conn.commit()
            return True
        except pyodbc.Error as e:
            print(f"Database error: {e}")
            return False

    def authenticate_user(self, username, password):
        hashed_password = self.hash_password(password)
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT password, User_ID FROM Listener WHERE Name = ?", (username,))
            result = cursor.fetchone()
            if result and result[0] == hashed_password:
                self.user_id = result[1]
                return True
            return False
        except pyodbc.Error as e:
            print(f"Database error: {e}")
            return False
 
    def authenticate_artist(self, username, password):
        hashed_password = self.hash_password(password)
        try:
            cursor = self.conn.cursor()

            # First, check if the username and password are correct in the Listener table
            cursor.execute(
                "SELECT User_Id, password FROM Listener WHERE Name = ?", (username,)
            )
            listener_result = cursor.fetchone()

            if listener_result and listener_result[1] == hashed_password:
                # User is a valid listener, now check if they are an artist
                user_id = listener_result[0]
                cursor.execute(
                    "SELECT Artist_ID, Name FROM Artist WHERE User_Id = ?", (user_id,)
                )
                artist_result = cursor.fetchone()

                if artist_result:
                    # User is also an artist, return the Artist_ID and Name
                    return artist_result
                else:
                    # User is not an artist
                    print("User is not an artist")
                    return False
            else:
                # Invalid username or password
                return False

        except pyodbc.Error as e:
            print(f"Database error: {e}")
            return False

    def authenticate_moderator(self, username, password):
        hashed_password = self.hash_password(password)
        try:
            cursor = self.conn.cursor()

            # First, check if the username and password are correct in the Listener table
            cursor.execute(
                "SELECT User_Id, password FROM Listener WHERE Name = ?", (username,)
            )
            listener_result = cursor.fetchone()

            if listener_result and listener_result[1] == hashed_password:
                # User is a valid listener, now check if they are an artist
                user_id = listener_result[0]
                cursor.execute(
                    "SELECT Mod_ID FROM Moderator WHERE User_ID = ?", (user_id,)
                )
                mod_result = cursor.fetchone()

                if mod_result:
                    # User is also an artist, return the Artist_ID and Name
                    return mod_result
                else:
                    # User is not an artist
                    print("User is not a moderator")
                    return False
            else:
                # Invalid username or password
                return False

        except pyodbc.Error as e:
            print(f"Database error: {e}")
            return False
         
class BaseManagementFrame(tk.Frame):
    def create_ui(self, name):
        label = tk.Label(self, text=f"{name} Management")
        label.pack(pady=10)

        # Common Back Button for all frames
        back_button = tk.Button(self, text="Back", command=self.go_back)
        back_button.pack(pady=10)

    def go_back(self):
        self.pack_forget()
        # Show the main interface
        
        #print(self.role_var.get())
        
        self.master.button_frame.pack(padx=10, pady=10)
        for btn in [
            self.master.manage_album_btn,
            self.master.manage_song_btn,
            
        ]:
            btn.pack(pady=10)

        #try catch is basically if statement for if role_var exists
        try:
            self.role_var 

        except:
            dummy = 0
        else:
            if self.role_var.get() != 'artist':
                for btn in [
                self.master.manage_artist_btn,
                self.master.manage_listener_btn,
                self.master.manage_moderator_btn,
                self.master.manage_playlist_btn
            
                ]:
                    btn.pack(pady=10)

class AlbumManagementFrame(BaseManagementFrame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.create_ui("Album")

        # Album UI components
        self.album_id_var = tk.StringVar()
        self.album_title_var = tk.StringVar()
        self.album_release_date_var = tk.StringVar()
        self.album_artist_id_var = tk.StringVar()

        self.create_widgets()

    def create_widgets(self):
        tk.Label(self, text="Album ID:").pack(padx=5, pady=5)
        album_id_entry = tk.Entry(self, textvariable=self.album_id_var)
        album_id_entry.pack(padx=5, pady=5)

        tk.Label(self, text="Title:").pack(padx=5, pady=5)
        album_title_entry = tk.Entry(self, textvariable=self.album_title_var)
        album_title_entry.pack(padx=5, pady=5)

        tk.Label(self, text="Release Date (YYYY-MM-DD):").pack(padx=5, pady=5)
        album_release_date_entry = tk.Entry(
            self, textvariable=self.album_release_date_var
        )
        album_release_date_entry.pack(padx=5, pady=5)

        tk.Label(self, text="Artist ID:").pack(padx=5, pady=5)
        album_artist_id_entry = tk.Entry(self, textvariable=self.album_artist_id_var)
        album_artist_id_entry.pack(padx=5, pady=5)

        button_frame = tk.Frame(self)
        button_frame.pack(padx=5, pady=5)

        insert_album_button = tk.Button(
            button_frame, text="Insert", command=self.insert_album
        )
        insert_album_button.pack(side=tk.LEFT, padx=5)

        delete_album_button = tk.Button(
            button_frame, text="Delete", command=self.delete_album
        )
        delete_album_button.pack(side=tk.LEFT, padx=5)

        update_album_button = tk.Button(
            button_frame, text="Update", command=self.update_album
        )
        update_album_button.pack(side=tk.LEFT, padx=5)

    def insert_album(self):
        album_id = (
            self.album_id_var.get()
        )  # Add this line to get the album ID from the user input
        album_title = self.album_title_var.get()
        album_release_date = self.album_release_date_var.get()
        album_artist_id = self.album_artist_id_var.get()

        if (
            not album_id
            or not album_title
            or not album_release_date
            or not album_artist_id
        ):
            print("Please provide all the album details.")
            return

        if not self.master.conn:
            print("Connection is not open.")
            return

        cursor = self.master.conn.cursor()
        try:
            cursor.execute("SET IDENTITY_INSERT Album ON")
            cursor.execute(
                "INSERT INTO Album (Album_ID, Title, Release_date, Artist_ID) VALUES (?, ?, ?, ?)",
                album_id,
                album_title,
                album_release_date,
                album_artist_id,
            )
            self.master.conn.commit()
            cursor.execute("SET IDENTITY_INSERT Album OFF")

            print(f"Album '{album_title}' added successfully with ID {album_id}.")
        except pyodbc.Error as e:
            print(f"Error: {e}")

    def delete_album(self):
        album_id = self.album_id_var.get()
        if not album_id:
            print("Please provide the album ID.")
            return

        if not self.master.conn:
            print("Connection is not open.")
            return

        cursor = self.master.conn.cursor()
        try:
            cursor.execute("DELETE FROM Album WHERE Album_ID = ?", album_id)
            self.master.conn.commit()
            print(f"Album with ID {album_id} deleted successfully.")
        except pyodbc.Error as e:
            print(f"Error: {e}")

    def update_album(self):
        album_id = self.album_id_var.get()
        album_title = self.album_title_var.get()
        album_release_date = self.album_release_date_var.get()
        album_artist_id = self.album_artist_id_var.get()

        if (
            not album_id
            or not album_title
            or not album_release_date
            or not album_artist_id
        ):
            print("Please provide all the album details.")
            return

        if not self.master.conn:
            print("Connection is not open.")
            return

        cursor = self.master.conn.cursor()
        try:
            cursor.execute(
                "UPDATE Album SET Title = ?, Release_date = ?, Artist_ID = ? WHERE Album_ID = ?",
                album_title,
                album_release_date,
                album_artist_id,
                album_id,
            )
            self.master.conn.commit()
            print(f"Album with ID {album_id} updated successfully.")
        except pyodbc.Error as e:
            print(f"Error: {e}")


class SongManagementFrame(BaseManagementFrame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.db_connection = get_db_connection()
        self.create_ui("Song")

        # Song UI components
        self.song_id_var = tk.StringVar()
        self.song_name_var = tk.StringVar()
        self.song_rating_var = tk.StringVar()
        self.song_duration_var = tk.StringVar()
        self.song_release_date_var = tk.StringVar()
        self.song_artist_id_var = tk.StringVar()

        self.create_widgets()

    def create_widgets(self):
        tk.Label(self, text="Song Details").pack(pady=10)

        self.add_labeled_entry("Song ID (For Update/Delete Only):", self.song_id_var)
        self.add_labeled_entry("Name:", self.song_name_var)
        self.add_labeled_entry("Rating (0-10):", self.song_rating_var)
        self.add_labeled_entry("Duration (HH:MM:SS):", self.song_duration_var)
        self.add_labeled_entry("Release Date (YYYY-MM-DD):", self.song_release_date_var)
        self.add_labeled_entry("Artist ID:", self.song_artist_id_var)

        # Buttons
        tk.Button(self, text="Insert Song", command=self.insert_song).pack(pady=5)
        tk.Button(self, text="Update Song", command=self.update_song).pack(pady=5)
        tk.Button(self, text="Delete Song", command=self.delete_song).pack(pady=5)

        # Associate Song with Album UI
        associate_frame = tk.Frame(self)
        associate_frame.pack(pady=20)

        self.song_album_associate_album_id_var = tk.StringVar()
        self.song_album_associate_song_id_var = tk.StringVar()

        tk.Label(associate_frame, text="Associate Song with Album").pack(pady=10)
        self.add_labeled_entry(
            "Album ID:", self.song_album_associate_album_id_var, parent=associate_frame
        )
        self.add_labeled_entry(
            "Song ID:", self.song_album_associate_song_id_var, parent=associate_frame
        )

        tk.Button(
            associate_frame,
            text="Associate Song",
            command=self.associate_song_with_album,
        ).pack(pady=10)

    def add_labeled_entry(self, label, var, parent=None):
        """Utility function to pack a label and its associated entry."""
        frame = tk.Frame(parent if parent else self)
        frame.pack(pady=5)
        tk.Label(frame, text=label).pack(side=tk.LEFT, padx=5)
        tk.Entry(frame, textvariable=var).pack(side=tk.LEFT, padx=5)

    def get_cursor(self):
        if not self.db_connection:
            print("Database connection not available.")
            return None
        return self.db_connection.cursor()

    def insert_song(self):
        # Fetching the values from the entries
        song_name = self.song_name_var.get()
        rating = self.song_rating_var.get()
        duration = self.song_duration_var.get()
        release_date = self.song_release_date_var.get()
        artist_id = self.song_artist_id_var.get()

        # Data validation can be added here
        if not song_name:
            print("Song name is required!")
            return

        if self.db_connection:
            try:
                cursor = self.db_connection.cursor()  # Correctly obtaining the cursor
                cursor.execute(
                    "INSERT INTO [dbo].[Song] (Name, Rating, Duration, Release_date, Artist_ID) VALUES (?, ?, ?, ?, ?)",
                    song_name,
                    rating,
                    duration,
                    release_date,
                    artist_id,
                )
                self.db_connection.commit()
                print("Song inserted successfully!")
            except pyodbc.Error as e:
                print(f"Error: {e}")
        else:
            print("Database connection is not available.")

    def update_song(self):
        # Fetching the values from the entries
        song_id = self.song_id_var.get()
        song_name = self.song_name_var.get()
        rating = self.song_rating_var.get()
        duration = self.song_duration_var.get()
        release_date = self.song_release_date_var.get()
        artist_id = self.song_artist_id_var.get()

        # Data validation
        if not song_id:
            print("Song ID is required for update!")
            return

        if self.db_connection:
            try:
                cursor = self.db_connection.cursor()  # Correctly obtaining the cursor
                cursor.execute(
                    "UPDATE [dbo].[Song] SET Name = ?, Rating = ?, Duration = ?, Release_date = ?, Artist_ID = ? WHERE Song_ID = ?",
                    song_name,
                    rating,
                    duration,
                    release_date,
                    artist_id,
                    song_id,
                )
                self.db_connection.commit()
                print("Song updated successfully!")
            except pyodbc.Error as e:
                print(f"Error: {e}")
        else:
            print("Database connection is not available.")

    def delete_song(self):
        # Fetching the value from the entry
        song_id = self.song_id_var.get()

        # Data validation
        if not song_id:
            print("Song ID is required for deletion!")
            return

        if self.db_connection:
            try:
                cursor = self.db_connection.cursor()  # Correctly obtaining the cursor
                cursor.execute("DELETE FROM [dbo].[Song] WHERE Song_ID = ?", song_id)
                self.db_connection.commit()
                print("Song deleted successfully!")
            except pyodbc.Error as e:
                print(f"Error: {e}")
        else:
            print("Database connection is not available.")

    def associate_song_with_album(self):
        album_id = self.song_album_associate_album_id_var.get()
        song_id = self.song_album_associate_song_id_var.get()

        if not album_id or not song_id:
            print("Both Album ID and Song ID are required!")
            return

        if self.db_connection:
            try:
                cursor = self.db_connection.cursor()
                cursor.execute("SELECT 1 FROM Album WHERE Album_ID = ?", album_id)
                if not cursor.fetchone():
                    print("Album ID does not exist.")
                    return
                cursor.execute("SELECT 1 FROM Song WHERE Song_ID = ?", song_id)
                if not cursor.fetchone():
                    print("Song ID does not exist.")
                    return
                cursor.execute(
                    "INSERT INTO [dbo].[AlbumSong] (Album_ID, Song_ID) VALUES (?, ?)",
                    album_id,
                    song_id,
                )
                self.db_connection.commit()
                print("Song associated with album successfully!")
            except pyodbc.Error as e:
                print(f"Error: {e}")
        else:
            print("Database connection is not available.")


class ArtistManagementFrame(BaseManagementFrame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.create_ui("Artist")

        # Artist UI components
        self.artist_frame = tk.Frame(self, bd=2, relief=tk.RIDGE, padx=10, pady=10)
        self.artist_frame.pack(pady=20)

        tk.Label(self.artist_frame, text="Artist ID:").grid(
            row=0, column=0, padx=5, pady=5
        )
        self.artist_id_var = tk.StringVar()
        artist_id_entry = tk.Entry(self.artist_frame, textvariable=self.artist_id_var)
        artist_id_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(self.artist_frame, text="Artist Name:").grid(
            row=1, column=0, padx=5, pady=5
        )
        self.artist_name_var = tk.StringVar()
        artist_name_entry = tk.Entry(
            self.artist_frame, textvariable=self.artist_name_var
        )
        artist_name_entry.grid(row=1, column=1, padx=5, pady=5)

        insert_button = tk.Button(
            self.artist_frame, text="Insert", command=self.insert_artist
        )
        insert_button.grid(row=2, column=0, padx=5, pady=5)

        delete_button = tk.Button(
            self.artist_frame, text="Delete", command=self.delete_artist
        )
        delete_button.grid(row=2, column=1, padx=5, pady=5)

        update_button = tk.Button(
            self.artist_frame, text="Update", command=self.update_artist
        )
        update_button.grid(row=2, column=2, padx=5, pady=5)

    # Artist Functions as Class Methods
    def insert_artist(self):
        artist_name = self.artist_name_var.get()
        if not artist_name:
            print("Please provide the artist name.")
            return

        if not self.master.conn:
            print("Connection is not open.")
            return

        cursor = self.master.conn.cursor()
        try:
            cursor.execute("INSERT INTO Artist (Name) VALUES (?)", artist_name)
            self.master.conn.commit()
            print(f"Artist {artist_name} added successfully.")
        except pyodbc.Error as e:
            print(f"Error: {e}")

    def delete_artist(self):
        artist_id = self.artist_id_var.get()
        if not artist_id:
            print("Please provide the artist ID.")
            return

        if not self.master.conn:
            print("Connection is not open.")
            return

        cursor = self.master.conn.cursor()
        try:
            cursor.execute("DELETE FROM Artist WHERE Artist_ID = ?", artist_id)
            self.master.conn.commit()
            print(f"Artist with ID {artist_id} deleted successfully.")
        except pyodbc.Error as e:
            print(f"Error: {e}")

    def update_artist(self):
        artist_id = self.artist_id_var.get()
        artist_name = self.artist_name_var.get()
        if not artist_id or not artist_name:
            print("Please provide both the artist ID and name.")
            return

        if not self.master.conn:
            print("Connection is not open.")
            return

        cursor = self.master.conn.cursor()
        try:
            cursor.execute(
                "UPDATE Artist SET Name = ? WHERE Artist_ID = ?", artist_name, artist_id
            )
            self.master.conn.commit()
            print(f"Artist with ID {artist_id} updated successfully.")
        except pyodbc.Error as e:
            print(f"Error: {e}")


class ListenerManagementFrame(BaseManagementFrame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.create_ui("Listener")

        # Listener UI components
        self.listener_frame = tk.Frame(self, bd=2, relief=tk.RIDGE, padx=10, pady=10)
        self.listener_frame.pack(pady=20)

        tk.Label(self.listener_frame, text="User ID:").grid(
            row=0, column=0, padx=5, pady=5
        )
        self.user_id_var = tk.StringVar()
        user_id_entry = tk.Entry(self.listener_frame, textvariable=self.user_id_var)
        user_id_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(self.listener_frame, text="Listener Name:").grid(
            row=1, column=0, padx=5, pady=5
        )
        self.listener_name_var = tk.StringVar()
        listener_name_entry = tk.Entry(
            self.listener_frame, textvariable=self.listener_name_var
        )
        listener_name_entry.grid(row=1, column=1, padx=5, pady=5)

        insert_button = tk.Button(
            self.listener_frame, text="Insert", command=self.insert_listener
        )
        insert_button.grid(row=2, column=0, padx=5, pady=5)

        delete_button = tk.Button(
            self.listener_frame, text="Delete", command=self.delete_listener
        )
        delete_button.grid(row=2, column=1, padx=5, pady=5)

        update_button = tk.Button(
            self.listener_frame, text="Update", command=self.update_listener
        )
        update_button.grid(row=2, column=2, padx=5, pady=5)

    # Listener Functions as Class Methods
    def insert_listener(self):
        listener_name = self.listener_name_var.get()
        if not listener_name:
            print("Please provide the listener name.")
            return

        if not self.master.conn:
            print("Connection is not open.")
            return

        cursor = self.master.conn.cursor()
        try:
            cursor.execute(
                "INSERT INTO [dbo].[Listener] (Name) VALUES (?)", listener_name
            )
            self.master.conn.commit()
            print(f"Listener {listener_name} added successfully.")
        except pyodbc.Error as e:
            print(f"Error: {e}")

    def delete_listener(self):
        user_id = self.user_id_var.get()
        if not user_id:
            print("Please provide the user ID.")
            return

        if not self.master.conn:
            print("Connection is not open.")
            return

        cursor = self.master.conn.cursor()
        try:
            cursor.execute("DELETE FROM [dbo].[Listener] WHERE User_ID = ?", user_id)
            self.master.conn.commit()
            print(f"Listener with User ID {user_id} deleted successfully.")
        except pyodbc.Error as e:
            print(f"Error: {e}")

    def update_listener(self):
        user_id = self.user_id_var.get()
        listener_name = self.listener_name_var.get()
        if not user_id or not listener_name:
            print("Please provide both the user ID and listener name.")
            return

        if not self.master.conn:
            print("Connection is not open.")
            return

        cursor = self.master.conn.cursor()
        try:
            cursor.execute(
                "UPDATE [dbo].[Listener] SET Name = ? WHERE User_ID = ?",
                listener_name,
                user_id,
            )
            self.master.conn.commit()
            print(f"Listener with User ID {user_id} updated successfully.")
        except pyodbc.Error as e:
            print(f"Error: {e}")


class ModeratorManagementFrame(BaseManagementFrame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.create_ui("Moderator")

        # Moderator UI components
        self.moderator_frame = tk.Frame(self, bd=2, relief=tk.RIDGE, padx=10, pady=10)
        self.moderator_frame.pack(pady=20)

        tk.Label(self.moderator_frame, text="Mod ID:").grid(
            row=0, column=0, padx=5, pady=5
        )
        self.mod_id_var = tk.StringVar()
        mod_id_entry = tk.Entry(self.moderator_frame, textvariable=self.mod_id_var)
        mod_id_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(self.moderator_frame, text="User ID:").grid(
            row=1, column=0, padx=5, pady=5
        )
        self.user_id_var = tk.StringVar()
        user_id_entry = tk.Entry(self.moderator_frame, textvariable=self.user_id_var)
        user_id_entry.grid(row=1, column=1, padx=5, pady=5)

        insert_button = tk.Button(
            self.moderator_frame, text="Insert", command=self.insert_moderator
        )
        insert_button.grid(row=2, column=0, padx=5, pady=5)

        delete_button = tk.Button(
            self.moderator_frame, text="Delete", command=self.delete_moderator
        )
        delete_button.grid(row=2, column=1, padx=5, pady=5)

    # Moderator Functions as Class Methods
    def insert_moderator(self):
        user_id = self.user_id_var.get()
        if not user_id:
            print("Please provide the User ID.")
            return

        if not self.master.conn:
            print("Connection is not open.")
            return

        cursor = self.master.conn.cursor()
        try:
            cursor.execute(
                "INSERT INTO [dbo].[Moderator] (User_ID) VALUES (?)", user_id
            )
            self.master.conn.commit()
            print(f"Moderator with User ID {user_id} added successfully.")
        except pyodbc.Error as e:
            print(f"Error: {e}")

    def delete_moderator(self):
        mod_id = self.mod_id_var.get()
        if not mod_id:
            print("Please provide the Mod ID.")
            return

        if not self.master.conn:
            print("Connection is not open.")
            return

        cursor = self.master.conn.cursor()
        try:
            cursor.execute("DELETE FROM [dbo].[Moderator] WHERE Mod_ID = ?", mod_id)
            self.master.conn.commit()
            print(f"Moderator with Mod ID {mod_id} deleted successfully.")
        except pyodbc.Error as e:
            print(f"Error: {e}")


class PlaylistManagementFrame(BaseManagementFrame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.create_ui("Playlist")

        # Playlist UI components
        self.playlist_id_var = tk.StringVar()
        self.playlist_name_var = tk.StringVar()
        self.playlist_creation_date_var = tk.StringVar()
        self.playlist_user_id_var = tk.StringVar()

        self.create_widgets()

    def create_widgets(self):
        tk.Label(self, text="Playlist Details").pack(pady=10)

        self.add_labeled_entry(
            "Playlist ID (For Update/Delete Only):", self.playlist_id_var
        )
        self.add_labeled_entry("Name:", self.playlist_name_var)
        self.add_labeled_entry(
            "Creation Date (YYYY-MM-DD):", self.playlist_creation_date_var
        )
        self.add_labeled_entry("User ID:", self.playlist_user_id_var)

        # Buttons
        tk.Button(self, text="Insert Playlist", command=self.insert_playlist).pack(
            pady=5
        )
        tk.Button(self, text="Update Playlist", command=self.update_playlist).pack(
            pady=5
        )
        tk.Button(self, text="Delete Playlist", command=self.delete_playlist).pack(
            pady=5
        )

        # Associate Song with Playlist UI
        associate_frame = tk.Frame(self)
        associate_frame.pack(pady=20)

        self.playlist_song_associate_playlist_id_var = tk.StringVar()
        self.playlist_song_associate_song_id_var = tk.StringVar()

        tk.Label(associate_frame, text="Associate Song with Playlist").pack(pady=10)
        self.add_labeled_entry(
            "Playlist ID:",
            self.playlist_song_associate_playlist_id_var,
            parent=associate_frame,
        )
        self.add_labeled_entry(
            "Song ID:", self.playlist_song_associate_song_id_var, parent=associate_frame
        )

        tk.Button(
            associate_frame,
            text="Associate Song",
            command=self.associate_song_with_playlist,
        ).pack(pady=10)

    def add_labeled_entry(self, label, var, parent=None):
        """Utility function to pack a label and its associated entry."""
        frame = tk.Frame(parent if parent else self)
        frame.pack(pady=5)
        tk.Label(frame, text=label).pack(side=tk.LEFT, padx=5)
        tk.Entry(frame, textvariable=var).pack(side=tk.LEFT, padx=5)

    def insert_playlist(self):
        name = self.playlist_name_var.get()
        creation_date = self.playlist_creation_date_var.get()
        user_id = self.playlist_user_id_var.get()

        if not name or not creation_date:
            print("Playlist name and creation date are required!")
            return

        try:
            cursor = self.master.conn.cursor()
            cursor.execute(
                "INSERT INTO [dbo].[Playlist] (Name, Creation_Date, User_ID) VALUES (?, ?, ?)",
                name,
                creation_date,
                user_id,
            )
            self.master.conn.commit()
            print("Playlist inserted successfully!")
        except pyodbc.Error as e:
            print(f"Error: {e}")

    def update_playlist(self):
        playlist_id = self.playlist_id_var.get()
        name = self.playlist_name_var.get()
        creation_date = self.playlist_creation_date_var.get()
        user_id = self.playlist_user_id_var.get()

        if not playlist_id:
            print("Playlist ID is required for update!")
            return

        try:
            cursor = self.master.conn.cursor()
            cursor.execute(
                "UPDATE [dbo].[Playlist] SET Name = ?, Creation_Date = ?, User_ID = ? WHERE Playlist_ID = ?",
                name,
                creation_date,
                user_id,
                playlist_id,
            )
            self.master.conn.commit()
            print("Playlist updated successfully!")
        except pyodbc.Error as e:
            print(f"Error: {e}")

    def delete_playlist(self):
        playlist_id = self.playlist_id_var.get()

        if not playlist_id:
            print("Playlist ID is required for deletion!")
            return

        try:
            cursor = self.master.conn.cursor()
            cursor.execute(
                "DELETE FROM [dbo].[Playlist] WHERE Playlist_ID = ?", playlist_id
            )
            self.master.conn.commit()
            print("Playlist deleted successfully!")
        except pyodbc.Error as e:
            print(f"Error: {e}")

    def associate_song_with_playlist(self):
        playlist_id = self.playlist_song_associate_playlist_id_var.get()
        song_id = self.playlist_song_associate_song_id_var.get()

        if not playlist_id or not song_id:
            print("Both Playlist ID and Song ID are required!")
            return

        try:
            cursor = self.master.conn.cursor()
            cursor.execute(
                "INSERT INTO [dbo].[PlaylistSongs] (Playlist_ID, Song_ID) VALUES (?, ?)",
                playlist_id,
                song_id,
            )
            self.master.conn.commit()
            print("Song associated with playlist successfully!")
        except pyodbc.Error as e:
            print(f"Error: {e}")


# Instantiate and run the app
app = App()
app.mainloop()
