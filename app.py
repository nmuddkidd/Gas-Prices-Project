import mysql.connector;
import traceback;
from flask import Flask, render_template, send_from_directory
import requests
import json


class Store:
	def __init__(self, history_id, location_id, fuel_type, price, date_recorded):
		self.history = history_id
		self.location = location_id
		self.fuel_type = fuel_type
		self.price = price
		self.date = date_recorded

class Avg_Store:
	def __init__(self, legacy_history_id, location_id, week, year, price, fuel_type):
		self.history = legacy_history_id
		self.location = location_id
		self.week = week
		self.year = year
		self.price = price
		self.fuel = fuel_type


if __name__ == '__main__':	
	stores = []
	avg_price_store = []
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
		exit

	print("connection established")
	print(cnx)
	cursor = cnx.cursor()
	
	try:
		sql = "SELECT * FROM  Price_History ORDER BY history_id DESC"
		cursor.execute(sql)

		for row in cursor:
			stores.append(Store(row[0],row[1],row[2],row[3],row[4]))
			
			
	finally:
		cnx.commit()
		cnx.close()

	
	for store in stores:
		location_id = 1
		sum_premium = 0
		sum_unleaded = 0
		total_unleaded = 0
		total_premium = 0
		unleaded_avg = 0
		premium_avg = 0
		if(store.history == location_id and str(store.fuel) == "Unleaded"):
			sum_unleaded+= store.price
			total_unleaded+=1
		elif(str(store.fuel) == "Premium"):
			sum_premium+= store.price
			total_premium+=1
		else:
			break
		
		if (str)
		location_id+=1


			

