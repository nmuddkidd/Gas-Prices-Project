import mysql.connector
import traceback
import random

def jsonSourcing():
    #TODO: Sourcing data from json and inserting it into Initial_Prices
    return 0

def priceHistoryCreation():
    #Imports existing data and any repeat data is sent to records
    #select matching locations and move the OLDER data to price history
    cursor.execute("INSERT INTO Price_History (location_id, unleaded_price, premium_price, record_time) SELECT location_id, unleaded_price, premium_price, record_time FROM Prices WHERE price_id NOT IN ( SELECT Prices.Price_id FROM Initial_Prices JOIN Prices ON Prices.location_id = Initial_Prices.location_id AND Prices.unleaded_price = Initial_Prices.unleaded_price AND Prices.premium_price = Initial_Prices.premium_price) AND price_id NOT IN ( SELECT Prices.Price_id FROM Price_History JOIN Prices ON Prices.location_id = Price_History.location_id AND Prices.unleaded_price = Price_History.unleaded_price AND Prices.premium_price = Price_History.premium_price);")
    cursor.execute("TRUNCATE Prices;")
    cursor.execute("INSERT INTO Prices SELECT * FROM Initial_Prices;")
    cursor.execute("TRUNCATE Initial_Prices;")

def legacyDataCreation():
    #Demotes data from active history into legacy data by month
    #WARNING: Needs a value to base MAX(Legacy_id) off of however this can be fixed
    #TODO: fix that (easy)
    cursor.execute("INSERT INTO Legacy_Price_History (location_id,month,year,unleaded_price,premium_price) SELECT location_id, MONTH(record_time), YEAR(record_time), AVG(unleaded_price), AVG(premium_price) FROM Price_History WHERE (MONTH(record_time) < MONTH(NOW()) AND YEAR(record_time) = YEAR(NOW())) OR YEAR(Price_History.record_time) < YEAR(NOW()) GROUP BY location_id, YEAR(record_time), MONTH(record_time);")
    cursor.execute("DELETE FROM Price_History WHERE (MONTH(record_time) < MONTH(NOW()) AND YEAR(record_time) = YEAR(NOW())) OR YEAR(record_time) < YEAR(NOW())")

def zeUberFunction():
    jsonSourcing()
    priceHistoryCreation()
    legacyDataCreation()

#TESTING FUNCTIONS
def priceJunk():
    #Throws junk data into prices
    #NOTE: test data is denoted by a NEGATIVE dollar value

    values = "INSERT INTO Prices (location_id,unleaded_price,premium_price,record_time) VALUES "

    for x in range (1, 101):
        if(x==100):
            values += "("+str(-1*random.randint(1,10))+","+str(random.randint(0,9))+'.'+str(random.randint(1,99))+","+str(random.randint(0,9))+'.'+str(random.randint(1,99))+",\""+str(random.randint(1,9999))+'-'+str(random.randint(1,12))+'-'+str(random.randint(1,28))+"\");"
        else:
            values += "("+str(-1*random.randint(1,10))+","+str(random.randint(0,9))+'.'+str(random.randint(1,99))+","+str(random.randint(0,9))+'.'+str(random.randint(1,99))+",\""+str(2024)+'-'+str(random.randint(1,12))+'-'+str(random.randint(1,28))+"\"),\n"
    cursor.execute(values)
    
    return 0

def initPriceJunk():
    #Throws junk data into initial prices
    #NOTE: test data is denoted by a NEGATIVE dollar value

    values = "INSERT INTO Initial_Prices (location_id,unleaded_price,premium_price,record_time) VALUES "

    for x in range (1, 101):
        if(x==100):
            values += "("+str(-1*random.randint(1,10))+","+str(random.randint(0,9))+'.'+str(random.randint(1,99))+","+str(random.randint(0,9))+'.'+str(random.randint(1,99))+",\""+str(random.randint(1,9999))+'-'+str(random.randint(1,12))+'-'+str(random.randint(1,28))+"\");"
        else:
            values += "("+str(-1*random.randint(1,10))+","+str(random.randint(0,9))+'.'+str(random.randint(1,99))+","+str(random.randint(0,9))+'.'+str(random.randint(1,99))+",\""+str(2024)+'-'+str(random.randint(1,12))+'-'+str(random.randint(1,28))+"\"),\n"
    cursor.execute(values)
    
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
        maximum = 0
    for x in range(0,100):
        ID = maximum + x + 1
        if(x==99):
            values += "("+str(ID)+","+str(-1*random.randint(1,10))+","+str(random.randint(0,9))+'.'+str(random.randint(1,99))+","+str(random.randint(0,9))+'.'+str(random.randint(1,99))+",\""+str(random.randint(1,9999))+'-'+str(random.randint(1,12))+'-'+str(random.randint(1,28))+"\");"
        else:
            values += "("+str(ID)+","+str(-1*random.randint(1,10))+","+str(random.randint(0,9))+'.'+str(random.randint(1,99))+","+str(random.randint(0,9))+'.'+str(random.randint(1,99))+",\""+str(2024)+'-'+str(random.randint(1,12))+'-'+str(random.randint(1,28))+"\"),\n"
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
zeUberFunction();

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
