"""
TODO
Input File
	Input Daily Log of Products COMPLETE
		Create Daily Log Template 
	Input Product Database COMPLETE
		Fix Product Database 

Data Manipulation
	Calculate Product Usage (used minus total stock)
	Forecast product Usage (days left)
	Calcualate cost of Product used daily/monthly/yearly
	
	Display
		Product usage over time

	Notification Warning When Low
	Notification Warning When Using above normal
	Calculate Average Weekly Use
	Compare Current product price to other products in database
	Find Cheaper Product

Database
	Comb over database and check if product exist
	Add To Database if doesnt exist
	Track History of product use and Store in database
	Search Database for products
	Show information such as ratio, cost, etc.

Output
	Txt
		Create Fake Orders
			Create Fake order template
	File Export
		Export Data to Spreadsheet csv
		Export Data to JSON
	Matplotlib
		Export Graph of Product Usage OverTime
		Export Graph of most used product
	Display
		Display to screen information in a clean format


Possible Additions
	Barcode Generator and Barcode Reader
"""


import pandas as pd
import numpy as np


# daily_log = open('log.txt', 'r')  input("Input Daily Log File Here: ")
# print(daily_log.readlines())

def find_product():
    csv_f = 'detailing_database.csv' #input("Input Database File Here: ")
    csv_database = pd.read_csv(csv_f)
    csv_name = list(csv_database['Name'])
    for key in daily_log_dic.keys():
        if key in csv_name:
            print(f" {key}: Already Exists" )
            print(int(csv_name.index(key)) + 2)
            csv_database.loc[csv_name.index(key),'InUse'] = 'TRUE'
            csv_database.to_csv(csv_f, index=False)
                

daily_log_dic = {}

# Open, Read and Close Log File
with open('log1.txt', "r") as daily_log: #input("Input Daily Log File Here: ")
    # print(daily_log.readlines())
    products = []
    for line in daily_log:
        if line.startswith('#'): #Remove Comments
            continue
        else: 
            product_key_value = tuple(line.strip().split(':'))
            products.append(product_key_value)
            #daily_log_dic = dict(product_data)
    daily_log_dic= dict(products)
# print(daily_log_dic)

find_product()


