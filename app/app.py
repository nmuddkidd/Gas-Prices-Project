from flask import Flask, render_template, send_from_directory
from flask_caching import Cache
import requests
import MySQLdb

db = MySQLdb.connect(
	host='cse335-fall-2024.c924km8o85q2.us-east-1.rds.amazonaws.com',
	user='ncmudd01',
	password='54caf60528',
	database='student_ncmudd01_db'
)

app = Flask(__name__)
app.config['CACHE_TYPE'] = 'SimpleCache'
app.config['CACHE_DEFAULT_TIMEOUT'] = 1800
cache = Cache(app)

def strip_spaces(obj):
	if isinstance(obj, str):
		return obj.strip()
	elif isinstance(obj, list):
		return [strip_spaces(item) for item in obj]
	elif isinstance(obj, dict):
		return {key: strip_spaces(value) for key, value in obj.items()}
	return obj

def upload(sequel):
	cursor = db.cursor()
	cursor.executemany("INSERT INTO gas_prices (store_id, regular_price, premium_price) VALUES (%s, %s, %s)", sequel)
	db.commit()
	cursor.close()

@app.route("/")
def index():
	return render_template("map.html")

@app.route("/gas.svg")
def favicon():
	return send_from_directory(app.static_folder, "gas.svg")

@app.route("/sams.csv")
def sams():
	result = sequel = []
	for store in samsdata():
		if 'gasPrices' in store:
			prices = {11:0,16:0}
			for grade in store['gasPrices']:
				if grade['gradeId'] in prices:
					prices[grade['gradeId']] = f"{int(grade['price']*100)/100:.2f}"
			result.append(f"{prices[11]},{prices[16]},{store['geoPoint']['latitude']},{store['geoPoint']['longitude']}")
			sequel.append((store['id'],prices[11],prices[16]))
	upload(sequel)
	return "\n".join(result)

@app.route("/costco.csv")
def costco():
	result = sequel = []
	for store in costcodata():
		if 'US' == store['country'] and 'regular' in store['gasPrices'] and 'PR' != store['state']:
			prices = {'regular':0,'premium':0}
			for grade in prices:
				prices[grade] = store['gasPrices'][grade][:-1]
			result.append(f"{prices['regular']},{prices['premium']},{store['latitude']},{store['longitude']}")
			sequel.append((store['identifier'],prices['regular'],prices['premium']))
	upload(sequel)
	return "\n".join(result)

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

if __name__ == '__main__':
	app.run()
