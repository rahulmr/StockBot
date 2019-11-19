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
import xlsxwriter
import utils
from openpyxl import load_workbook



def main():
	#main function
	print 'Running median'
	
	#read list of all stock
	ratioList = ['Net Profit Margin(%)','Return on Assets Excluding Revaluations', 'Return On Net Worth(%)', 'Return On Capital Employed(%)', 'Net Interest Income / Total Funds']
	count = 0
	
	for item in ratioList:
		df = utils.readExcel('Ratios.xlsx')
		# Replace the column with the converted values
		df['Return On Net Worth(%)'] = pd.to_numeric(df['Return On Net Worth(%)'], errors='coerce')
		df['Return On Capital Employed(%)'] = pd.to_numeric(df['Return On Capital Employed(%)'], errors='coerce')
		df['Net Interest Income / Total Funds'] = pd.to_numeric(df['Net Interest Income / Total Funds'], errors='coerce')


		# Drop NA values, listing the converted columns explicitly
		#   so NA values in other columns aren't dropped
		df.dropna(subset = ['Return On Net Worth(%)', 'Return On Capital Employed(%)', 'Net Interest Income / Total Funds'])
		df2 = df.groupby(['Industry', 'Year', 'Month'], as_index=False)[item].median()
		print df2
		df2.to_excel(str(item).replace('/','-')+'.xlsx', sheet_name=str(count))
		print item + " done"
		count = count + 1
		


if __name__ == "__main__":
    main()
	
