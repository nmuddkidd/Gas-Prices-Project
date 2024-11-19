import mysql.connector;
import traceback;

cnx = mysql.connector.connect();
print("attempting connection to server");

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

print("connection established");
print(cnx)
cursor = cnx.cursor()
"""cursor.execute("SHOW DATABASES")

for x in cursor:
    print(x)"""

cursor.execute("INSERT INTO Test VALUES (-1)")
cnx.commit();
cnx.close();


















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
