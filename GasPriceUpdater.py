import mysql.connector
import traceback
import random

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
cursor.execute("SELECT MIN(history_id) FROM Price_History")

minimum = 1
values = "INSERT INTO Price_History VALUES "
data = cursor.fetchall()
minimum = data[0][0]
for x in range(0,100):
    ID = minimum - x - 1
    dollars = random.randint(0,9)
    cents = random.randint(1,99)
    if(x==99):
        values += "("+str(ID)+","+str(-1*random.randint(1,100))+",\"unleaded\","+str(dollars)+'.'+str(cents)+",\""+str(random.randint(1,9999))+'-'+str(random.randint(1,12))+'-'+str(random.randint(1,28))+"\");"
    else:
        values += "("+str(ID)+","+str(-42)+",\"unleaded\","+str(dollars)+'.'+str(cents)+",\""+str(2024)+'-'+str(11)+'-'+str(random.randint(1,30))+"\"),\n"

cursor.execute(values)
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
