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



def main():
	#main function
	
	
	#read list of all stock
	df = utils.readExcel('Ratios.xlsx')
	print df.groupby(['Industry', 'Year', 'Month'], as_index=False)['Net Profit Margin(%)'].median()


if __name__ == "__main__":
    main()
	
