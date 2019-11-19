
from pprint import pprint
import numpy
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
import xlsxwriter
import utils
from openpyxl import load_workbook
from collections import defaultdict
from time import strptime

#read list of all stock
ratioFiles = ['Net Profit Margin(%)','Return on Assets Excluding Revaluations', 'Return On Net Worth(%)', 'Return On Capital Employed(%)', 'Net Interest Income - Total Funds']
shareRatiodf = utils.readExcel('Ratios.xlsx')
PATdf = utils.readExcel('Net Profit Margin(%).xlsx')
ROAdf = utils.readExcel('Return on Assets Excluding Revaluations.xlsx')
ROWdf = utils.readExcel('Return On Net Worth(%).xlsx')
ROCAdf =  utils.readExcel('Return On Capital Employed(%).xlsx')
NIdf =  utils.readExcel('Net Interest Income - Total Funds.xlsx')
buyList = my_dictionary()  
topBuyList = {}

def getdfMap(ratio):
	return{
		'Net Profit Margin(%)': PATdf,
		'Return on Assets Excluding Revaluations': ROAdf,
		'Return On Net Worth(%)': ROWdf,
		'Return On Capital Employed(%)': ROCAdf,
		'Net Interest Income / Total Funds': NIdf
}[ratio]


def getValue(share, industry, ratio):
	year = 0
	monthNum = 0
	shareMedian = 0
	industryMedian = 0
	for index, row in shareRatiodf.iterrows():
		if row['Share'] == share:
			if int(row['Year']) > year or ((int(row['Year']) == year) and utils.monthToNum(row['Month']) > monthNum):
				try:
					shareMedian = float(row[ratio])
					year = int(row['Year'])
					month = str(row['Month'])
					monthNum = utils.monthToNum(row['Month'])
				except:
					print row[ratio]
	
	for index, row in getdfMap(ratio).iterrows():
		if (row['Industry'] == industry) and (int(row['Year']) == year) and (row['Month'] == month):
			industryMedian = float(row[ratio])

	if (shareMedian > industryMedian) and (shareMedian < 10.0):
		return 0.25
	else:
		return 0
				
			

def getMedianScore(share, industry):
	score = 0.0
	for item in ratioFiles:
		score = score + getValue(share, industry, str(item).replace('-','/'))
	
	return score * 0.25

def getTrendScore(data):
	try:
		avg200 = utils.getAverage(data['graph']['values'], 200)
		avg50 = utils.getAverage(data['graph']['values'], 50)
		currentPrice = float(data['graph']['current_close'])
		print '200d price is '+str(avg200)+' | current price is '+str(currentPrice)+' | 50d avg is '+str(avg50)
	
		return (avg50-avg200)/avg200
			
	except Exception as e:
		print e
		return 0

def main():
	
	headers = {'authorization': "Basic API Key Ommitted", 'accept': "application/json", 'accept': "text/csv"}

	print 'Running stock scoring'
	#read list of all stock
	df = utils.readExcel('stock-unique.xlsx')
	averageList = my_dictionary()
	countList = my_dictionary()
	positiveList = my_dictionary()
	
	#iterate every stock
	for index, row in df.iterrows():
		try:
			#runtime calculate change average and percentage of stocks on the rise
			url = 'https://appfeeds.moneycontrol.com//jsonapi//stocks//graph&format=json&range=max&type=area&ex=&sc_id='+str(row['id'])
			rcomp = requests.get(url, headers=headers)
			data = json.loads(rcomp.text)
			currentPrice = float(data['graph']['current_close'])
			prevPrice = float(data['graph']['prev_close'])
			change  = currentPrice/prevPrice
			countList = utils.upsert(countList, str(row['Industry']))
			averageList = utils.upsertAverage(averageList, str(row['Industry']), change, countList[str(row['Industry'])])
			if currentPrice > prevPrice:
				positiveList = utils.upsertAverage(positiveList, str(row['Industry']), 1, countList[str(row['Industry'])])
			else:
				positiveList = utils.upsertAverage(positiveList, str(row['Industry']), 0, countList[str(row['Industry'])])
		except Exception as e:
			print str(e)+' '+str(row['id'])
			
		
	#iterate every stock
	for index, row in df.iterrows():
		try:
			#runtime calculate change average and percentage of stocks on the rise
			url = 'https://appfeeds.moneycontrol.com//jsonapi//stocks//graph&format=json&range=max&type=area&ex=&sc_id='+str(row['id'])
			rcomp = requests.get(url, headers=headers)
			data = json.loads(rcomp.text)
			
			#give trend score
			trendScore = getTrendScore(data)
			
			#give industry change score
			industryScore = (averageList[str(row['Industry'])] - 0.9)*(0.5 + positiveList[str(row['Industry'])])
			
			#give ratio median score
			medianScore = getMedianScore(str(row['id']), str(row['Industry']))
			
			buyList.add(str(row['id']), trendScore + industryScore+ medianScore)
		except Exception as e:
			print e
	
	#find top buy list
	topBuyList = dict(Counter(buyList).most_common(5))
		
	print 'Top shares to be bought are:'
	print topBuyList
	
	utils.sendSMS('buy ', topBuyList)

if __name__ == "__main__":
    main()
            