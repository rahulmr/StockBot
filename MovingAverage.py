
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

stockList = []
buyList = my_dictionary()  
topBuyList = {}

today = date.today()

#function to return list of stock names
def readExcel():
	df = pd.read_excel('stock-unique.xlsx', sheet_name=0, keep_default_na=False) # can also index sheet by name or fetch all sheets
	stockList = df['id'].tolist() 
	return stockList
	
#function to compare averages of the stock, add to topBuyList if high, otherwise check if it is part of bought list
def buyOrSell(item):
	url = 'https://appfeeds.moneycontrol.com//jsonapi//stocks//graph&format=json&range=max&type=area&ex=&sc_id='+item
	headers = {'authorization': "Basic API Key Ommitted", 'accept': "application/json", 'accept': "text/csv"}

	rcomp = requests.get(url, headers=headers)
	data = json.loads(rcomp.text)
	
	try:
	
		avg200 = utils.getAverage(data['graph']['values'], 200)
		avg50 = utils.getAverage(data['graph']['values'], 50)
		currentPrice = float(data['graph']['current_close'])
		print '200d price is '+str(avg200)+' | current price is '+str(currentPrice)+' | 50d avg is '+str(avg50)
	
		global buyList
		
		if (avg50 > avg200) and (currentPrice < avg50):
			print 'Adding '+item+' to buy list | 50d avg is '+str(avg50)+' | 200d avg is '+str(avg200)
			buyList.add(item, (avg50-avg200)/avg200)
			
	except Exception as e:
		print e
		return


def main():
	#main function
	os.system("notify-run configure -f https://notify.run/hRtUrGQaxEM0l3VR")
	
	#read list of all stock
	stockList = readExcel()
		
		
	#Loop through all, add to topBuyList
	for item in stockList:
		print 'Stock is '+item
		buyOrSell(item)
		
	#find top buy list
	topBuyList = dict(Counter(buyList).most_common(5))
		
	print 'Top shares to be bought are:'
	print topBuyList
	
	utils.sendSMS('buy ', topBuyList)
	
	
if __name__ == "__main__":
    main()
	