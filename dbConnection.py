import pyodbc

def fetch_data_from_test():

    conn = None
    # Connection string
    conn_str = ("Driver={ODBC Driver 17 for SQL Server};"
            "Server=tcp:cs4604server.database.windows.net,1433;"
            "Database=cs4604db;"
            "UID=cs4604;"
            "PWD=Oblong08!;"
            "Encrypt=yes;"
            "TrustServerCertificate=yes;")

    
    try:
        # Establishing the connection
        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()
        
        # Executing the query
        cursor.execute("SELECT * FROM Test")
        rows = cursor.fetchall()

        # Displaying the data (you can also process the data as per your requirements)
        for row in rows:
            print(row)

    except pyodbc.Error as e:
        print(f"Error: {e}")
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    fetch_data_from_test()
