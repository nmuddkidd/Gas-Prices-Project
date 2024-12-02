from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import URL
from sqlalchemy import create_engine

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'cse335-fall-2024.c924km8o85q2.us-east-1.rds.amazonaws.com'

url_object = URL.create(
    "postgresql+pg8000",
    username="ncmudd01",
    password="54caf60528",
    host="cse335-fall-2024.c924km8o85q2.us-east-1.rds.amazonaws.com",
    database="student_ncmudd01_db",
)

engine = create_engine(url_object)

@app.route("/")
def flaskShit():
    return "<p>hello world</p>"

"""cursor.execute("SELECT * FROM Price_History")
queryResult = cursor.fetchall()
output = ""
for item in queryResult:
    output += "<p>"
    for attribute in item:
        output += " "+str(attribute)+" "
    output += "</p>\n""""