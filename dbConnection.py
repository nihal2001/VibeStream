import pyodbc




def get_db_connection():
    conn_str = ("Driver={ODBC Driver 17 for SQL Server};"
                "Server=tcp:cs4604server.database.windows.net,1433;"
                "Database=cs4604db;"
                "UID=cs4604;"
                "PWD=Oblong08!;"
                "Encrypt=yes;"
                "TrustServerCertificate=yes;")
    try:
        return pyodbc.connect(conn_str)
    except pyodbc.Error as e:
        print(f"Error: {e}")
        return None

def fetch_data_from_test():
    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM Song")
            rows = cursor.fetchall()
            for row in rows:
                print(row)
        except pyodbc.Error as e:
            print(f"Error: {e}")
        finally:
            conn.close()

if __name__ == "__main__":
    fetch_data_from_test()
