import mysql.connector
import traceback
import random

def flaskShit():
    #TODO: Flask implementation
    return 0

def jsonSourcing():
    #TODO: Sourcing data from json and inserting it into Prices then demoting overwritten data
    return 0

def priceHistoryCreation():
    #TODO: Transfer data from prices to price history AND deleting data from active prices table
    #select matching locations and move the OLDER data to price history
    return 0

def legacyDataCreation():
    #Demotes data from active history into legacy data by month
    #WARNING: Needs a value to base MAX(Legacy_id) off of however this can be fixed
    #TODO: fix that (easy)
    cursor.execute("INSERT INTO Legacy_Price_History (legacy_price_history_id,location_id,week,year,price,fuel_type) SELECT ROW_NUMBER() OVER (ORDER BY history_id) + (SELECT MAX(legacy_price_history_id) FROM Legacy_Price_History), location_id, MONTH(date_recorded), YEAR(date_recorded), AVG(price), fuel_type FROM Price_History WHERE (MONTH(date_recorded) < MONTH(NOW()) AND YEAR(date_recorded) = YEAR(NOW())) OR YEAR(Price_History.date_recorded) < YEAR(NOW()) GROUP BY location_id, fuel_type, YEAR(date_recorded), MONTH(date_recorded);")
    cursor.execute("DELETE FROM Price_History WHERE (MONTH(date_recorded) < MONTH(NOW()) AND YEAR(date_recorded) = YEAR(NOW())) OR YEAR(Price_History.date_recorded) < YEAR(NOW())")

def priceJunk():
    #TODO: Throw junk values into price table - not sure if needed (easy)
    #NOTE: test data is denoted by a NEGATIVE dollar value
    return 0

def historyJunk():
    #Throws junk into the History table
    #WARNING: PKs added are greater than the highest value
    #NOTE: test data is denoted by a NEGATIVE dollar value
    cursor.execute("SELECT MAX(history_id) FROM Price_History")
    values = "INSERT INTO Price_History VALUES "
    data = cursor.fetchall()
    maximum = data[0][0]
    if(maximum == None):
        maximum = 0;
    for x in range(0,100):
        ID = maximum + x + 1
        dollars = -1*random.randint(0,9)
        cents = -1*random.randint(1,99)
        if(x==99):
            values += "("+str(ID)+","+str(-1*random.randint(1,100))+",\"unleaded\","+str(dollars)+'.'+str(cents)+",\""+str(random.randint(1,9999))+'-'+str(random.randint(1,12))+'-'+str(random.randint(1,28))+"\");"
        else:
            values += "("+str(ID)+","+str(-1*random.randint(1,10))+",\"unleaded\","+str(dollars)+'.'+str(cents)+",\""+str(2024)+'-'+str(10)+'-'+str(random.randint(1,30))+"\"),\n"
    cursor.execute(values)

cnx = mysql.connector.connect()
print("attempting connection to server")

try:
    cnx = mysql.connector.connect(user='ncmudd01', 
                                password='54caf60528',
                                host='cse335-fall-2024.c924km8o85q2.us-east-1.rds.amazonaws.com',
                                database="student_ncmudd01_db"
                                )
except:
    print(traceback.format_exc())
    print("Connection could not be established")
    exit;

print("connection established")
print(cnx)
cursor = cnx.cursor()

#put functions you want here
historyJunk()
legacyDataCreation()

cnx.commit()
cnx.close()


















"""from sshtunnel import SSHTunnelForwarder
import MySQLdb as db
import pandas as pd

with SSHTunnelForwarder(
    'premium143.web-hosting.com',
    ssh_port=21098,
    ssh_username="andypbbo",
    ssh_password="H#3W2&1S4X4JD3l7",
    remote_bind_address=('162.0.232.237', 21098)
) as server:
    print("Connection to server established");
    conn = db.connect(host="127.0.0.1",
    port=server.local_bind_port,
    user="andypbbo_nathan",
    passwd="database_password1")
    pd.read_sql_query("INSERT INTO Testing VALUES (-1)", conn)"""
