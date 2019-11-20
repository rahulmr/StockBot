from pprint import pprint
import numpy as np
import pandas as pd
import csv
import json 
import requests
from datetime import datetime
from collections import Counter
from datetime import date
from my_dictionary import my_dictionary
from notify_run import Notify
import os
import xlrd
import utils


sellList = []

def getAnnualReturn(currentPrice, purchasePrice, purchaseDate):
	ROI  = currentPrice*.995/purchasePrice
	today = date.today()
	delta = today - purchaseDate;
	deltaPer = float(delta.days + 1)/365.0
	return pow(ROI,1/deltaPer)


def shouldSell(currentPrice, purchasePrice, purchaseDate):
	#sell if annual return is more than 115%
	if (currentPrice - purchasePrice > 5) and (getAnnualReturn(currentPrice, purchasePrice, purchaseDate) > 1.15):
		return 1
	
	#sell if annual return is less than 90%
	if (purchasePrice - currentPrice > 5) and (getAnnualReturn(currentPrice, purchasePrice, purchaseDate) < 0.9) and (currentPrice > 20.0):
		return 1
	
	return 0
	

def main():
	#main function
	headers = {'authorization': "Basic API Key Ommitted", 'accept': "application/json", 'accept': "text/csv"}
	print "Running seller"
	
	df = utils.readExcel('boughtList.xlsx')
	
	for index, row in df.iterrows():
		print 'Running for '+ str(row['Name'])
		url = 'https://appfeeds.moneycontrol.com//jsonapi//stocks//graph&format=json&range=max&type=area&ex=&sc_id='+str(row['Name'])
		rcomp = requests.get(url, headers=headers)
		data = json.loads(rcomp.text)
		currentPrice = float(data['graph']['current_close'])
		if shouldSell(currentPrice, float(row['Price']), datetime.strptime(row['Date'], '%d %b %Y').date()):
			sellList.append(row['Name'])
			
	if len(sellList) is not 0:
		utils.sendSMS('sell ', sellList)
	
	print 'sell '+str(sellList)
	
if __name__ == "__main__":
    main()