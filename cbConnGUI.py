import tkinter as tk
import pyodbc

conn = None

def close_B():
    if conn:
        conn.close()
        update_connection_status(False)

def open_B():
    global conn  # Use the global 'conn' variable
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
        conn = pyodbc.connect(conn_str)
        update_connection_status(True)
    except pyodbc.Error as e:
        print(f"Error: {e}")
        update_connection_status(False)

def test_data():
    if not conn:
        print("Connection is not open.")
        update_connection_status(False)
        return

    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Song")
    rows = cursor.fetchall()
    # You can process or display the data as needed
    for row in rows:
        print(row)

def update_connection_status(connected):
    if connected:
        status_label.config(text="Connected", bg="green")
    else:
        status_label.config(text="Not Connected", bg="red")

def on_connect_button_click():
    test_data()

# Create the main window
root = tk.Tk()
root.title("Database Connection")

# Create a frame for button layout
button_frame = tk.Frame(root)
button_frame.pack(padx=10, pady=10)

# Button to open the connection
open_button = tk.Button(button_frame, text="Open Connection", command=open_B)
open_button.pack(side=tk.LEFT, padx=10)

# Button to close the connection
close_button = tk.Button(button_frame, text="Close Connection", command=close_B)
close_button.pack(side=tk.LEFT, padx=10)

# Button to test the connection
test_button = tk.Button(button_frame, text="Test Connection", command=on_connect_button_click)
test_button.pack(side=tk.LEFT, padx=10)

# Label to indicate connection status
status_label = tk.Label(root, text="Not Connected", bg="red", padx=10, pady=5)
status_label.pack()

root.mainloop()
