import mysql.connector

def get_connection():
    print("Attempting to connect to database...")
    connection = mysql.connector.connect(
        host='localhost',
        user='root',
        password='root',
        database='dav6100s25'
    )
    if connection.is_connected():
        print("Connection Successful")
    else:
        print("Check Again!")
    return connection
#Calling the get_connection function
if __name__ == "__main__":
    get_connection()