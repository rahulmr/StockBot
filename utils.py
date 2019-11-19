
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



def readExcel(filename):
	df = pd.read_excel(filename, sheet_name=0, keep_default_na=False) # can also index sheet by name or fetch all sheets
	stockList = df
	return df


def readText():
	f = open('boughtList.txt', 'r')
	boughtList = f.readlines()
	f.close()
	return boughtList

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