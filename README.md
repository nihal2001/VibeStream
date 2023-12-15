# Vibe Stream

Pre-requisites

1) Install  ODBC drivers (Make sure you get the correct version for your operating system)
2) I am using python 3.9.9. I suggest y'all do the same for consistency. It would probably be a good idea to use a python virtual enviroment running that version.
3) Install pyodbc ("pip install pyodbc". However if you are using apple silicon, do "pip install pyodbc --no-binary pyodbc" instead)

*Note*
*You may have different errors. ChatGPT and google tend to be pretty good for debugging these dependency errors*

How To Run: python3 dbConnection.py

Expected output:
(1, 'Test1', 'Description for Test1')
(2, 'Test2', 'Description for Test2')
(3, 'Test3', 'Description for Test3')
(4, 'Test4', 'Description for Test4')
(5, 'Test5', 'Description for Test5')

