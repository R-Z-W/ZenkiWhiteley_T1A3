"""
TODO
Input File
	Input Daily Log of Products COMPLETE
		Create Daily Log Template COMPLETE
	Input Product Database COMPLETE
		Fix Product Database COMPLETE

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
	Comb over database and check if product exist COMPLETE
	Add To Database if doesnt exist INPROGRESS
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
#import numpy as np


def find_product():
    csv_f = 'detailing_database.csv' #input("Input Database File Here: ")
    csv_database = pd.read_csv(csv_f)
    csv_name = list(csv_database['Name'])
    csv_case_name = list((item.casefold() for item in csv_name)) #Case Insensitive
    print(f'case: {csv_case_name}')
    for key in daily_log_dic.keys():
        if key.startswith('Recorded'):
            print("Recorded")
        elif key.casefold() in csv_case_name:
            # Change to tr
            print(f"{key}: Already Exists" )
            # print(int(csv_name.index(key)) + 2)
            csv_database.loc[csv_name.index(key),'InUse'] = True
            csv_database.to_csv(csv_f, index=False)
        else:
            # Add new product to database file
            print(f'\nNew Product Found: {key}\n ')
            yes_no = input('-Add To Database? Y/N: ')
            if yes_no == 'Y' or 'y' or 'Yes' or 'yes':
                csv_category = set(csv_database['Category'])
                print(f'Exisiting Categories: {csv_category}')
                category = input('-Input Category: ')
                overall_price =  int(input("-Input Price: "))
                quantity =  int(input("-Input Quantity: "))
                unit_price = overall_price / quantity
                new_row = {'Name': key,'Category': category,'Overall Price': overall_price,'Quantity': quantity,'InUse': True,'Unit Price': unit_price, 'Ratio': input('-Input Ratio: ')}
                csv_database = csv_database.append(new_row, ignore_index=True)
                print(csv_database.tail(1))
                


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
    daily_log_dic = dict(products)
# print(daily_log_dic)

find_product()


