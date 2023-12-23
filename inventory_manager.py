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



def notify(key, csv_f, value):
    if not key.startswith('Recorded'):
        csv_database = pd.read_csv(csv_f) #Important read UPDATED csv
        csv_name = list(csv_database['Name'])
        if csv_database.loc[csv_name.index(key),'SingleUse'] in [True, 'TRUE', 'True']: #Not single use, then it wont be under 20%
            unit_quantity = csv_database.loc[csv_name.index(key),'UnitQuantity']
            extra = csv_database.loc[csv_name.index(key),'Extra']
            amount_left = (unit_quantity * extra) - float(value)
            if amount_left <= (unit_quantity * extra)*.2:
                print("WARNING UNDER 20%' LEFT!")
                yes_no = input('-Order More Product? Y/N: ')
                if yes_no.lower() in yes_list:
                    usr_quantity = usr_input_num('-Input Quantity of Product: ')
                    price = csv_database.loc[csv_name.index(key),'OverallPrice']
                    total = float(price) * float(usr_quantity)
                    with open('productorder.txt', 'a') as product_order:
                        product_order.write(str(usr_quantity) + ', ' + key + ', ' + str(price) + ', ' + str(total))
                        print('Added To: productorder.txt')


    # if 'over_usage':
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
                if value not in csv_database.head(0):
                    csv_database[date] = "" #define new column based on date
                    csv_database.to_csv(csv_f, index=False) #push to csv
            
        # If Exist Set:
        elif key.casefold() in csv_case_name:
            print('Checking Product...')
            print(f"{key}: Already Exists" )
            csv_database.loc[csv_name.index(key),'InUse'] = True #set InUse to True
            csv_database.loc[csv_name.index(key), date] = float(value) #record date usage
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
                           date: float(value)}
                csv_database.loc[len(csv_database)] = new_row #create new row
                csv_database.to_csv(csv_f, index=False)#push to csv
                print(csv_database.tail(1))#print last element added
        
        notify(key, csv_f, value)

# Open, Read and Close Log File
def open_log():
    try:
        log_file = input('-Input Daily Log File: ')
        with open(log_file, "r") as daily_log:
            products = []
            for line in daily_log:
                if line.startswith('#'): #remove comments
                    continue
                else: #put products in tuple pairs
                    product_key_value = tuple(line.strip().split(':'))
                    products.append(product_key_value)
            global daily_log_dic #not best practise / dictionary for products and their values
            daily_log_dic = dict(products) #dictionary from tuple pairs
    except:
        print('Invalid log file.')

# Main
yes_list = ['y', 'yes']
daily_log_dic = {} #incase open_log() doesnt run
while True:
    print(""""
    Inventory Manager
    Options:
    Process Log File      = (1)
    Forecast Usage        = (2)
          """)
    usr = usr_input_num('-Input a Number: ')

    match usr:
        case 1:
            open_log()
            find_product_database()
        case 2:
            calculate_forecast()

    exit = input('\nWould you like to Again or exit? Y/N: ')
    print('\n')
    if exit.lower() not in yes_list:
        print('Exiting...')
        break



