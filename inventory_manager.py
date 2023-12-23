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
	Add To Database if doesnt exist INPROGRESS COMPLETE 
	Track History of product use and Store in database COMPLETE 
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


def calculate_usage():
    pass
def calculate_forecast():
    pass
def calculate_cost():
    pass
def notify():
    if 'low':
        pass
    if 'over_usage':
        pass
def calculate_compare():
    if 'cheaper':
        pass
def search_database():
    pass
def history():
    pass


# User Input Try Functions
def usr_input_num(prompt):
    while True:
        num = input(prompt)
        try:
            num = float(num)
            return num
        except:
            print("Invalid number, Try Again")
def usr_input_boolean(prompt):
    while True:
        bool_in = input(prompt)
        try:
            bool_in == 'True' or 'False'
            return bool_in
        except:
            print("Invalid bool, Try True or False")

def usr_input_ratio(prompt):
    print(prompt)
    ratio_1 = usr_input_num('-First Number: ')
    ratio_2 = usr_input_num('-Second Number: ')
    if ratio_1 == ratio_2:
        ratio_in = 1
    else:
        ratio_in = str(ratio_1) + ':' + str(ratio_2)
    return ratio_in




def find_product_database():
    csv_f = 'detailing_database.csv' #input("Input Database File Here: ")
    csv_database = pd.read_csv(csv_f) #read database
    csv_name = list(csv_database['Name']) #Names to list
    csv_case_name = list((item.casefold() for item in csv_name)) #change to Case Insensitive
    for key in daily_log_dic.keys():
        value = daily_log_dic[key]
        if key.startswith('Recorded'):
            print(f'{key} : {value}')
            if key == 'Recorded_Date':
                date = value
                csv_database[date] = "" #define new column based on date
                csv_database.to_csv(csv_f, index=False) #push to csv
            
        # If Exist Set:
        elif key.casefold() in csv_case_name:
            print('Checking Product...')
            print(f"{key}:{value} : Already Exists" )
            # print(int(csv_name.index(key)) + 2)
            csv_database.loc[csv_name.index(key),'InUse'] = True #set InUse to True
            csv_database.loc[csv_name.index(key), date] = value #record date usage / Bug: Make sure recorded is set.
            csv_database.to_csv(csv_f, index=False) #push to csv
        
        # Add new product to database file
        else:
            print(f'\nNew Product Found: {key}\n ')
            yes_no = input('-Add To Database? Y/N: ')
            if yes_no.lower() in yes_list:
                csv_category = set(csv_database['Category']) # set of Categories to prevent duplicates
                print(f'Exisiting Categories: {csv_category}')
                category = input('-Input Category: ')
                overall_price =  usr_input_num("-Input Price: ") # define Price
                unit_quantity =  usr_input_num("-Input Unit Quantity: ") # define Unit Quantity
                extra = usr_input_num("-Input Quantity Bought: ") # define extra
                unit_price = overall_price / unit_quantity # calc UnitPrice
                ratio =  usr_input_ratio('-Input Ratio') # define ratio
                single_use =  usr_input_boolean('-Single use? True or False: ')
                new_row = {'Name': key,
                           'Category': category,
                           'OverallPrice': overall_price,
                           'UnitQuantity': unit_quantity,
                           'Extra': extra,
                           'UnitPrice': unit_price, 
                           'Ratio': ratio,
                           'InUse': True,
                           'SingleUse': single_use,
                           date: value}
                csv_database.loc[len(csv_database)] = new_row
                csv_database.to_csv(csv_f, index=False)#push to csv
                print(csv_database.tail(1))#print last element added

    
# Open, Read and Close Log File
def open_log():
    try:
        log_file = input("Input Daily Log File Here: ")
        with open(log_file, "r") as daily_log:
            # print(daily_log.readlines())
            products = []
            for line in daily_log:
                if line.startswith('#'): #remove comments
                    continue
                else: #put products in tuple pairs
                    product_key_value = tuple(line.strip().split(':'))
                    products.append(product_key_value)
                    #daily_log_dic = dict(product_data)
            global daily_log_dic #not best practise / dictionary for products and their values
            daily_log_dic = dict(products) #dictionary from tuple pairs
    except:
        print('Invalid log file.')



# Main
yes_list = ['y', 'yes']
daily_log_dic = {} #incase open_log() doesnt run
while True:
    open_log()
    find_product_database()

    exit = input('\nWould you like to Again or exit? Y/N: ')
    print('\n')
    if exit.lower() not in yes_list:
        print('Exiting...')
        break



