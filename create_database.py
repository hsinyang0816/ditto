import mysql.connector
import csv

'''
    This program is used to create three necessary databases by reading csv file.
'''

# ---------- Arugment Setup ----------
# Database Account
''' Online '''
hostname = "192.168.0.10"
username = "guest"
db_root_password = "sqlfinalproject"

''' Local
hostname = "localhost"
username = "root"
db_root_password = "123456"
'''
# Input Data File Path
filePath_tableA = "blocking/input/tableA.csv"
filePath_tableB = "blocking/input/tableB.csv"
# -----------------------------------

def createDatabase():
    global filePath_tableA, filePath_tableB
    global hostname, username, db_root_password
    # ===== Database Initialization =====
    # Create Database / naming => (left_DB, right_DB, result_DB)
    mydb = mysql.connector.connect(
        host=hostname, 
        user=username, 
        passwd=db_root_password)

    cursor = mydb.cursor()
    try:
        print("\n\nTrying to delete existing database...\n")
        cursor.execute("DROP DATABASE left_DB")
        cursor.execute("DROP DATABASE right_DB")
        cursor.execute("DROP DATABASE result_DB")
    except mysql.connector.Error as err:
        print("Database does not Exist!\n")
    
    print("Trying to create database......")
    cursor.execute("CREATE DATABASE left_DB")
    cursor.execute("CREATE DATABASE right_DB")
    cursor.execute("CREATE DATABASE result_DB")
    print("\nDatabase construction complete!")

    # Finish creating database, shutting down connection
    cursor.close()
    mydb.close()

    # ===== Inserting Data into Database separately =====
    # ----- Insert data into left_DB -----
    mydb = mysql.connector.connect(
        host=hostname, 
        user=username, 
        passwd=db_root_password, 
        database="left_DB")

    if not mydb.is_connected():
        print("Connecting to left_DB failed! Please check your connection!")
        return
    
    # Print database version if connected to database
    db_info = mydb.get_server_info()
    print("\nDatabase Version:", db_info, "\n")

    cursor = mydb.cursor()

    # Create table "Citation"
    # id | title | authors | venue | year
    sql = "CREATE TABLE Citation (id INT PRIMARY KEY, title TEXT, authors VARCHAR(1024), venue VARCHAR(255), year VARCHAR(20));"
    cursor.execute(sql)
    print("CREATE TABLE Citation in left_DB......\n")
    # Read csv file
    csv_fileA = open(filePath_tableA, encoding='utf-8', newline='')
    csv_data = csv.reader(csv_fileA, quotechar='"', delimiter=',', quoting=csv.QUOTE_ALL, skipinitialspace=True)
    # Skip the first column
    next(csv_data)

    print("Trying to insert data from csv file!")
    # Insert from csv file
    sql = "INSERT INTO Citation (id, title, authors, venue, year) VALUES (%s, %s, %s, %s, %s)"
    count = 0
    for row in csv_data:
        for i in range(len(row)):
            if row[i] == '':
                row[i] = None
        val = tuple(row)
        cursor.execute(sql, val)
        mydb.commit()
        count += 1
    csv_fileA.close()
    print("All Data(In total : %s rows) in csv file was inserted. \n" %count)

    # Finish all task, shutting down connection
    cursor.close()
    mydb.close()
    print("left_DB Closed!", "\n\n")
    
    # -------------------------------------
    # ----- Insert data into right_DB -----
    mydb = mysql.connector.connect(
        host=hostname, 
        user=username, 
        passwd=db_root_password, 
        database="right_DB")

    if not mydb.is_connected():
        print("Connecting to right_DB failed! Please check your connection!")
        return
    
    # Print database version if connected to database
    db_info = mydb.get_server_info()
    print("Database Version:", db_info, "\n\n")

    cursor = mydb.cursor()

    # Create table "Citation"
    # id | title | authors | venue | year
    sql = "CREATE TABLE Citation (id INT PRIMARY KEY, title TEXT, authors VARCHAR(1024), venue VARCHAR(255), year VARCHAR(20));"
    cursor.execute(sql)
    print("CREATE TABLE Citation in right_DB......\n")

    # Read csv file
    csv_fileB = open(filePath_tableB, encoding='utf-8', newline='')
    csv_data = csv.reader(csv_fileB, quotechar='"', delimiter=',', quoting=csv.QUOTE_ALL, skipinitialspace=True)
    # Skip the first column
    next(csv_data)

    print("Trying to insert data from csv file!")
    # Insert from csv file
    sql = "INSERT INTO Citation (id, title, authors, venue, year) VALUES (%s, %s, %s, %s, %s)"
    count = 0
    for row in csv_data:
        for i in range(len(row)):
            if row[i] == '':
                row[i] = None
        val = tuple(row)
        cursor.execute(sql, val)
        mydb.commit()
        count += 1
    csv_fileB.close()
    print("All Data(In total : %s rows) in csv file was inserted. \n" %count)

    # Finish all task, shutting down connection
    cursor.close()
    mydb.close()
    print("right_DB Closed!", "\n\n")

    # --------------------------------------    
    # ----- Create Table for result_DB -----
    mydb = mysql.connector.connect(
        host=hostname, 
        user=username, 
        passwd=db_root_password, 
        database="result_DB")

    if not mydb.is_connected():
        print("Connecting to result_DB failed! Please check your connection!")
        return
    
    # Print database version if connected to database
    db_info = mydb.get_server_info()
    print("Database Version:", db_info, "\n\n")

    cursor = mydb.cursor()

    # Create table "Citation"
    # id | title | authors | venue | year
    sql = "CREATE TABLE Citation (id INT PRIMARY KEY AUTO_INCREMENT, title TEXT, authors VARCHAR(2048), venue VARCHAR(255), year VARCHAR(20));"
    cursor.execute(sql)
    print("Creat TABLE Citation in result_DB")

    cursor.close()
    mydb.close()
    print("result_DB Closed!", "\n\n")
    # -------------------------------------

    print("\n\nAll Database Creation Complete!!\n\n")

if __name__ == '__main__':
    createDatabase()
