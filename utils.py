
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
import newsRun


def upsert(dic, key):
	if dic.has_key(key):
		dic[key] = dic[key] + 1
	else:
		dic[key] = 0
	return dic

def upsertAverage(dic, key, value, count):
	if dic.has_key(key):
		dic[key] = (dic[key]*(count-1)+value)/count
	else:
		dic[key] = value
	return dic

def sendSMS(message, itemList):
	SMS = message
	os.system("notify-run configure -f https://notify.run/hRtUrGQaxEM0l3VR")

	#adding the new shares to be bought
	for item in itemList:
		SMS = SMS + getShareName(item) + ','
			
	notify = Notify()
	notify.send(SMS)

def saveToFile(itemList, filename):
	with open(filename, 'w') as f:
		for item in itemList:
			print >> f, item

def readExcel(filename):
	df = pd.read_excel(filename, sheet_name=0, keep_default_na=False) # can also index sheet by name or fetch all sheets
	stockList = df
	return df


def readText(filename):
	f = open(filename, 'r')
	boughtList = f.readlines()
	f.close()
	return str(boughtList)

def deleteContent(fName):
    with open(fName, "w"):
        pass

def inDayRange(time, days):
	today = date.today()
	#date = today.strftime("%d %b %Y")
	date_object = datetime.strptime(time, '%d %b %Y').date()
	delta = today - date_object;
	if delta.days > days:
		return 0
	else:
		return 1

def getDays(time, format):
	today = date.today()
	date_object = datetime.strptime(time, format).date()
	delta = today - date_object
	return delta.days
		
#return average of value of the number of days specified
def getAverage(data, days):
	sum = 0.0
	count = 0
	for row in data:
		if inDayRange(row.get('_time'), days):
			sum = sum + float(row.get('_value'))
			count = count + 1;
	return sum/count
	
def getShareName(item):
	wb = xlrd.open_workbook('stock-unique.xlsx')
	sheet = wb.sheet_by_index(0)
	
	for row_num in range(sheet.nrows):
		row_value = sheet.row_values(row_num)
		if row_value[0] == str(item):
			return row_value[1]
			
def monthToNum(month):
	return{
		'January' : 1,
		'February' : 2,
		'March' : 3,
		'April' : 4,
		'May' : 5,
		'June' : 6,
		'July' : 7,
		'August' : 8,
		'September' : 9, 
		'October' : 10,
		'November' : 11,
		'December' : 12
}[month]
	
def normalizaScore(score, date):
	days = getDays('2019 '+str(date), '%Y %b %d, %H:%M')
	return score - (score*days/30.0)

def getAlertScore(stock):
	url = 'https://www.moneycontrol.com/news18/stocks/overview/'+str(stock)+'/N'
	headers = {'authorization': "Basic API Key Ommitted", 'accept': "application/json", 'accept': "text/csv"}

	rcomp = requests.get(url, headers=headers)
	data = json.loads(rcomp.text)
	scoreNews = 0.0
	try:
		items = data['alerts']
		for row in items: 
			if str(row.get('title')) == 'News':
				scoreNews = scoreNews + normalizaScore(newsRun.getNewsScore(str(stock), str(row.get('message'))), str(row.get('entdate')))		
	except Exception as e:
		print e
	return scoreNews