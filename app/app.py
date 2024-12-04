from queue import Full
from flask import Flask, render_template, send_from_directory
from flask_caching import Cache
import requests
import random
import pymysql

db = pymysql.connections.Connection (
	host='cse335-fall-2024.c924km8o85q2.us-east-1.rds.amazonaws.com',
	user='ncmudd01',
	password='54caf60528',
	database='student_ncmudd01_db'
)

app = Flask(__name__)
app.config['CACHE_TYPE'] = 'SimpleCache'
app.config['CACHE_DEFAULT_TIMEOUT'] = 1#1800
cache = Cache(app)

#SQL STUFF
def strip_spaces(obj):
	if isinstance(obj, str):
		return obj.strip()
	elif isinstance(obj, list):
		return [strip_spaces(item) for item in obj]
	elif isinstance(obj, dict):
		return {key: strip_spaces(value) for key, value in obj.items()}
	return obj

def priceHistoryCreation():
	#Imports existing data and any repeat data is sent to records
	#select matching locations and move the OLDER data to price history
	cursor = db.cursor()
	cursor.execute("INSERT INTO Price_History (location_id, unleaded_price, premium_price, record_time) SELECT location_id, unleaded_price, premium_price, record_time FROM Prices WHERE price_id NOT IN ( SELECT Prices.Price_id FROM Initial_Prices JOIN Prices ON Prices.location_id = Initial_Prices.location_id AND Prices.unleaded_price = Initial_Prices.unleaded_price AND Prices.premium_price = Initial_Prices.premium_price) AND price_id NOT IN ( SELECT Prices.Price_id FROM Price_History JOIN Prices ON Prices.location_id = Price_History.location_id AND Prices.unleaded_price = Price_History.unleaded_price AND Prices.premium_price = Price_History.premium_price);")
	cursor.execute("TRUNCATE Prices;")
	cursor.execute("INSERT INTO Prices SELECT * FROM Initial_Prices;")
	cursor.execute("TRUNCATE Initial_Prices;")
	db.commit()
	cursor.close()

def legacyDataCreation():
	#Demotes data from active history into legacy data by month
	#WARNING: Needs a value to base MAX(Legacy_id) off of however this can be fixed
	#TODO: fix that (easy)
	cursor = db.cursor()
	cursor.execute("INSERT INTO Legacy_Price_History (location_id,month,year,unleaded_price,premium_price) SELECT location_id, MONTH(record_time), YEAR(record_time), AVG(unleaded_price), AVG(premium_price) FROM Price_History WHERE (MONTH(record_time) < MONTH(NOW()) AND YEAR(record_time) = YEAR(NOW())) OR YEAR(Price_History.record_time) < YEAR(NOW()) GROUP BY location_id, YEAR(record_time), MONTH(record_time);")
	cursor.execute("DELETE FROM Price_History WHERE (MONTH(record_time) < MONTH(NOW()) AND YEAR(record_time) = YEAR(NOW())) OR YEAR(record_time) < YEAR(NOW())")
	db.commit()
	cursor.close()

def zeUberFunction():
	priceHistoryCreation()
	legacyDataCreation()

	#TESTING FUNCTIONS
def initPriceJunk():
	#Throws junk data into initial prices
	#NOTE: test data is denoted by a NEGATIVE dollar value
	cursor = db.cursor()
	values = "INSERT INTO Initial_Prices (location_id,unleaded_price,premium_price) VALUES "

	for x in range (1, 101):
		if(x==100):
			values += "("+str(-1*random.randint(1,10))+","+str(-1*random.randint(0,9))+'.'+str(random.randint(1,99))+","+str(-1*random.randint(0,9))+'.'+str(random.randint(1,99))+");"
		else:
			values += "("+str(-1*random.randint(1,10))+","+str(-1*random.randint(0,9))+'.'+str(random.randint(1,99))+","+str(-1*random.randint(0,9))+'.'+str(random.randint(1,99))+"),\n"
	cursor.execute(values)
	db.commit()
	cursor.close()
    
	return 0

def priceJunk():
	#Throws junk data into prices
	#NOTE: test data is denoted by a NEGATIVE dollar value
	cursor = db.cursor()
	values = "INSERT INTO Prices (location_id,unleaded_price,premium_price,record_time) VALUES "

	for x in range (1, 101):
		if(x==100):
			values += "("+str(-1*random.randint(1,10))+","+str(-1*random.randint(0,9))+'.'+str(random.randint(1,99))+","+str(-1*random.randint(0,9))+'.'+str(random.randint(1,99))+",\""+str(random.randint(1,9999))+'-'+str(random.randint(1,12))+'-'+str(random.randint(1,28))+"\");"
		else:
			values += "("+str(-1*random.randint(1,10))+","+str(-1*random.randint(0,9))+'.'+str(random.randint(1,99))+","+str(-1*random.randint(0,9))+'.'+str(random.randint(1,99))+",\""+str(2024)+'-'+str(random.randint(1,12))+'-'+str(random.randint(1,28))+"\"),\n"
	cursor.execute(values)
    
	db.commit()
	cursor.close()
	return 0

def historyJunk():
	#Throws junk into the History table
	#WARNING: PKs added are greater than the highest value
	#NOTE: test data is denoted by a NEGATIVE dollar value
	cursor = db.cursor()
	cursor.execute("SELECT MAX(history_id) FROM Price_History")
	values = "INSERT INTO Price_History VALUES "
	data = cursor.fetchall()
	maximum = data[0][0]
	if(maximum == None):
		maximum = 0
		for x in range(0,100):
			ID = maximum + x + 1
			if(x==99):
				values += "("+str(ID)+","+str(-1*random.randint(1,10))+","+str(-1*random.randint(0,9))+'.'+str(random.randint(1,99))+","+str(-1*random.randint(0,9))+'.'+str(random.randint(1,99))+",\""+str(random.randint(1,9999))+'-'+str(random.randint(1,12))+'-'+str(random.randint(1,28))+"\");"
			else:
				values += "("+str(ID)+","+str(-1*random.randint(1,10))+","+str(-1*random.randint(0,9))+'.'+str(random.randint(1,99))+","+str(-1*random.randint(0,9))+'.'+str(random.randint(1,99))+",\""+str(2024)+'-'+str(random.randint(1,12))+'-'+str(random.randint(1,28))+"\"),\n"
	cursor.execute(values)
	db.commit()
	cursor.close()

def junker():
	#Puts old junk on Prices and new junk on initial Prices
	initPriceJunk()
	priceJunk()

def clear():
	#Truncates all tables
	#NOTE: Needs password
	print("WARNING This will delete ALL data across ALL tables")
	cursor = db.cursor()
	password = input("Database Password: ")
	if(password == "54caf60528"):
		print("Cleaning Database...")
		cursor.execute("TRUNCATE Prices;")
		cursor.execute("TRUNCATE Initial_Prices;")
		cursor.execute("TRUNCATE Price_History;")
		cursor.execute("TRUNCATE Legacy_Price_History;")
	else:
		print("Incorrect Password No Data Modified")
	db.commit()
	cursor.close()

def testClear():
	print("WARNING Attempting to delete all test data, but may have unintended consequences")
	cursor = db.cursor()
	password = input("Proceed? (Y/N): ")
	if(password == "Y" or password == "y"):
		print("Cleaning Test Data...")
		cursor.execute("DELETE FROM Prices WHERE location_id < 0 OR unleaded_price < 0 OR premium_price < 0;")
		cursor.execute("DELETE FROM Initial_Prices WHERE location_id < 0 OR unleaded_price < 0 OR premium_price < 0;")
		cursor.execute("DELETE FROM Price_History WHERE location_id < 0 OR unleaded_price < 0 OR premium_price < 0;")
		cursor.execute("DELETE FROM Legacy_Price_History WHERE location_id < 0 OR unleaded_price < 0 OR premium_price < 0;")
		print("Success!")
	else:
		print("No Data Modified")
	db.commit()
	cursor.close()

def fullTest():
	#Tests with random inputs
	#NOTE: Needs password
	print("WARNING This test will insert test data, but may have unintended consequences")
	password = input("Proceed? (Y/N): ")
	if(password == "Y" or password == "y"):
		print("Inserting Data...")
		junker()
		print("Success!")
		print("Transferring Data to History...")
		priceHistoryCreation()
		legacyDataCreation()
		print("Success!")
		testClear()
	else:
		print("No Data Modified")
	return 0

@app.route("/gas.csv")
def gas():
	cursor = db.cursor()
	data = cache.get("gas")
	if data: return data

	sequel = []
	result = []
	for store in samsdata():
		if 'gasPrices' in store:
			prices = {11:0,16:0}
			for grade in store['gasPrices']:
				if grade['gradeId'] in prices:
					prices[grade['gradeId']] = int(grade['price']*100)
			sequel.append((store['id'],prices[11],prices[16]))
			result.append(f"{prices[11]},{prices[16]},{store['geoPoint']['latitude']},{store['geoPoint']['longitude']}")
	result.append("")
	for store in costcodata():
		if 'US' == store['country'] and 'regular' in store['gasPrices'] and 'PR' != store['state']:
			prices = {'regular':0,'premium':0}
			for grade in prices:
			    prices[grade] = int(float(store['gasPrices'][grade])*100)
			sequel.append((int(store['identifier']),prices['regular'],prices['premium']))
			result.append(f"{prices['regular']},{prices['premium']},{store['latitude']},{store['longitude']}")
	cursor.executemany("INSERT INTO Initial_Prices (location_id, unleaded_price, premium_price) VALUES (%s, %s, %s)", sequel)
	zeUberFunction()
	db.commit()
	cursor.close()
	data = "\n".join(result)
	cache.set("gas", data)
	return data

@app.route("/")
def index():
	return render_template("map.html")

@app.route("/gas.svg")
def favicon():
	return send_from_directory(app.static_folder, "gas.svg")

@app.route("/sams.json")
def samsdata():
	data = cache.get("sams")
	if data: return data

	url = 'https://www.samsclub.com/api/node/vivaldi/browse/v2/clubfinder/list?distance=10000&nbrOfStores=1000&singleLineAddr=10001'
	response = requests.get(url, headers={'User-Agent': 'Mozilla', 'Accept-Encoding': 'ztsd'})
	data = strip_spaces(response.json())
	cache.set("sams", data)
	return data

@app.route("/costco.json")
def costcodata():
	data = cache.get("costco")
	if data: return data

	url = 'https://www.costco.com/AjaxWarehouseBrowseLookupView?hasGas=true&populateWarehouseDetails=true'
	response = requests.get(url, headers={'User-Agent': 'Mozilla', 'Accept-Encoding': 'gzip'})
	data = strip_spaces(response.json()[1:])
	cache.set("costco", data)
	return data

def SQLTEST():
	cursor = db.cursor()
	cursor.execute("SELECT * FROM Initial_Prices")
	output = cursor.fetchall()
	for _ in output:
		print(_)
	cursor.close()

if __name__ == '__main__':
	clear()
	app.run()
