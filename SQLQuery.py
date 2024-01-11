import mysql.connector
import json

db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'NTH23122',
    'database': 'dtb_et'
}

def InsertData(ID, locationID, temp, hud, lux, status):
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    query = "INSERT INTO tbl_tracker VALUES (%s, %s, %s, %s, %s, %s, NOW())"
    values = [(ID, locationID, temp, hud, lux, status)]

    cursor.executemany(query, values)
    conn.commit()
    conn.close()

def QueryData():
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    query = "SELECT * FROM tbl_tracker"
    cursor.execute(query)
    results = cursor.fetchall()
    return results

def JsonReturnData():
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    query = "SELECT * FROM tbl_user"
    cursor.execute(query)
    results = cursor.fetchall()
    data = [dict(zip(cursor.column_names, row)) for row in results]
    jdata = json.dumps(data, indent = 2)
    return jdata

def DropTable():
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    query = "DROP TABLE tbl_tracker"
    cursor.execute(query)

def CreateTable():
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    query = ("CREATE TABLE tbl_tracker("
             "id int,"
             "location varchar(25),"
             "temp float not null,"
             "hud float not null,"
             "lux float not null,"
             "stat varchar(25),"
             "tim datetime"
             ");")
    cursor.execute(query)

# DropTable()
# CreateTable()
# print(JsonReturnData())
# InsertData(1, "BTL", 1.2, 1.3, 1.3, "clouds")