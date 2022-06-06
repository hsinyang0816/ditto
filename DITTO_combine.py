'''
    This program is used to combined all data in the two databases (left_DB/right_DB) according to DITTO result.
    If no database is created, please execute "create_database.py" first.
'''
import mysql.connector
import jsonlines

# ---------- Arugment Setup ----------
# Input jsonline file
filePath = "output/output.jsonl"
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
# Database Name
database_ori_left = "left_DB"
database_ori_right = "right_DB"
database_result = "result_DB"
# -----------------------------------

def readJsonlFile(file):
    result = []
    try:
        with jsonlines.open(file) as reader:
            for line in reader:
                matching = line['match']
                # Check if the line is matched
                # Not Matched => not recorded
                if matching == 0:
                    continue
                # Matched => record left/right id
                left_match_id = line['left_id']
                right_match_id = line['fight_id']
                result.append((left_match_id, right_match_id))
    except EnvironmentError:
        print("No file can be opened! Please check if your file exists in => " + str(file))

    return result


def DITTO_combine_database():
    global filePath, db_root_password, hostname, username, db_root_password
    global database_ori_left, database_ori_right, database_result
    
    # Database Connection
    resultdb = mysql.connector.connect(
        host=hostname, 
        user=username, 
        passwd=db_root_password, 
        database=database_result)

    # Check database connection
    if not resultdb.is_connected():
        print("Connecting to \"result\" database failed! Please check your connection!")
        return
    
    print("All database is connected!\n\n")
    cursor = resultdb.cursor(buffered=True)

    matching_list = readJsonlFile(filePath)
    
    # sql_insert = "INSERT INTO result_DB.Citation (title, authors, venue, year)\
    #                 SELECT\
    #                 GROUP_CONCAT(L.title, ' ', R.title) as title,\
    #                 GROUP_CONCAT(L.authors, ' ', R.authors) as author,\
    #                 GROUP_CONCAT(L.venue, ' ', R.venue) as venue,\
    #                 GROUP_CONCAT(L.year, ' ', R.year) as year\
    #                 FROM left_DB.Citation as L, right_DB.Citation as R\
    #                 WHERE L.id=%s AND R.id=%s;"
    
    sql_insert = "INSERT result_DB.Citation(title, authors, venue, year)\
                    VALUES (%s, %s, %s, %s)"

    sql_findLeft = "SELECT left_DB.Citation.title, left_DB.Citation.authors, left_DB.Citation.venue, left_DB.Citation.year FROM left_DB.Citation\
                    WHERE left_DB.Citation.id = %s;"

    sql_findRight = "SELECT right_DB.Citation.title, right_DB.Citation.authors, right_DB.Citation.venue, right_DB.Citation.year FROM right_DB.Citation\
                    WHERE right_DB.Citation.id = %s;"
    

    sql_deleteLeft= "DELETE FROM left_DB.Citation\
                    WHERE left_DB.Citation.id=%s;"
    
    sql_deleteRight= "DELETE FROM right_DB.Citation\
                    WHERE right_DB.Citation.id=%s;"
    
    print("Trying to insert data that matches...")
    modified_count = 0
    for data in matching_list:
        # val = tuple(data)
        list_L = [data[0]]
        list_R = [data[1]]
        val_l = tuple(list_L)
        val_r = tuple(list_R)
        
        cursor.execute(sql_findLeft, val_l)
        Left_result = cursor.fetchone()
        if Left_result is None:
            continue
        Left_result = [i for i in Left_result]
        cursor.execute(sql_findRight, val_r)
        Right_result = cursor.fetchone()
        if Right_result is None:
            continue
        Right_result = [i for i in Right_result]

        matched = []

        for idx in range(len(Left_result)):
            if Left_result[idx] == "":
                matched.append(Right_result[idx])
            else:
                matched.append(Left_result[idx])
        
        matched = tuple(matched)
        cursor.execute(sql_insert, matched)

        cursor.close()
        cursor = resultdb.cursor(buffered=True)

        cursor.execute(sql_deleteLeft, val_l)

        cursor.close()
        cursor = resultdb.cursor(buffered=True)

        cursor.execute(sql_deleteRight, val_r)

        cursor.close()
        cursor = resultdb.cursor(buffered=True)
        
        resultdb.commit()
        modified_count += 1
    print("All Matching Data(In total : %s) in output file has inserted into result_DB.\n" %modified_count)
    
    cursor.close()
    cursor = resultdb.cursor(buffered=True)

    sql_insertLeft = "INSERT INTO result_DB.Citation (title, authors, venue, year)\
                    SELECT L.title, L.authors, L.venue, L.year\
                    FROM left_DB.Citation as L;"
    sql_insertRight = "INSERT INTO result_DB.Citation (title, authors, venue, year)\
                    SELECT R.title, R.authors, R.venue, R.year\
                    FROM right_DB.Citation as R;"
    cursor.execute(sql_insertLeft)
    cursor.execute(sql_insertRight)
    cursor.execute("Truncate TABLE left_DB.Citation")
    cursor.execute("Truncate TABLE right_DB.Citation")
    print("\nAll Remaining Data(In left_DB/right_DB) has combined into result_DB. \n\n")

    # Close all connection
    cursor.close()
    resultdb.close()

    print("[ ===== Task Complete! Shutting down all connection! ===== ]\n\n")

if __name__ == '__main__':
    DITTO_combine_database()
