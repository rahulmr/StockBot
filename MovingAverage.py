
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

stockList = []
buyList = my_dictionary()  
topBuyList = {}
sellList = []
boughtList = []

today = date.today()


def deleteContent(fName):
    with open(fName, "w"):
        pass

def inRange(time, days):
	global today
	#date = today.strftime("%d %b %Y")
	date_object = datetime.strptime(time, '%d %b %Y').date()
	delta = today - date_object;
	if delta.days > days:
		return 0
	else:
		return 1

#return average of value of the number of days specified
def getAverage(data, days):
	sum = 0.0;
	for row in data:
		if inRange(row.get('_time'), days):
			sum = sum + float(row.get('_value'))
	return sum/days

def readBoughtList():
	#df = pd.read_excel('boughtList.xlsx', sheet_name=0) # can also index sheet by name or fetch all sheets
	#boughtList = df['id'].tolist()
	f = open('boughtList.txt', 'r')
	boughtList = f.readlines()
	f.close()
	return boughtList

#function to return list of stock names
def readExcel():
	df = pd.read_excel('stock-unique-dummy.xlsx', sheet_name=0) # can also index sheet by name or fetch all sheets
	stockList = df['id'].tolist() 
	return stockList
	
#function to compare averages of the stock, add to topBuyList if high, otherwise check if it is part of bought list
def buyOrSell(item):
	url = 'https://appfeeds.moneycontrol.com//jsonapi//stocks//graph&format=json&range=max&type=area&ex=&sc_id='+item
	headers = {'authorization': "Basic API Key Ommitted", 'accept': "application/json", 'accept': "text/csv"}

	rcomp = requests.get(url, headers=headers)
	data = json.loads(rcomp.text)
	
	try:
	
		avg200 = getAverage(data['graph']['values'], 200)
		avg50 = getAverage(data['graph']['values'], 50)
	
		global sellList
		global buyList
		
		if avg50 > avg200:
			print 'Adding '+item+' to buy list | 50d avg is '+str(avg50)+' | 200d avg is '+str(avg200)
			buyList.add(item, avg50-avg200)
		else:
			if item in boughtList:
				print 'Adding '+item+' to sell list | 50d avg is '+str(avg50)+' | 200d avg is '+str(avg200)
				sellList.append(item)
	except:
		return



#main function
#read list of all stock
stockList = readExcel()
	
#read boughtList
boughtList = readBoughtList()

	
#Loop through all, add to topBuyList
for item in stockList:
	print 'Stock is '+item
	buyOrSell(item)
	
#find top buy list
topBuyList = dict(Counter(buyList).most_common(5))
	
#print buyList and SellList
print 'Top shares to be bought are:'
print topBuyList
#print sellList
	
#updateBoughtList
newList = []
SMS = ""

#adding the new shares to be bought
for item in topBuyList:
	if item not in boughtList:
		newList.append(item)
		SMS = SMS + str(item) + ','
			
#write new list to file
with open('boughtList.txt', 'w') as f:
    for item in newList:
        print >> f, item
		
		

notify = Notify()
notify.send(SMS)
	