import pandas as pd
import os
import re
import matplotlib.pyplot as plt

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
# Open, Read and Close Log File
def open_log():
    print('Available Log Files:') 
    log_names = [] # Get Log Files Names in current dir
    for files in os.scandir('.'):
        if files.is_file():
            log = files.name
            if log.startswith('Log'):
                log_names.append(log)
    log_names = sorted(log_names) # Sort Log Files Names:
    for item in log_names:
        print(item)  # Print Sorted Log Files Names:
    try:
        log_file = input('-Input Oldest Daily Log File: ')
        with open(log_file, "r") as daily_log:
            products = []
            for line in daily_log:
                if line.startswith('#'): #remove comments from log
                    continue
                else: 
                    product_key_value = tuple(line.strip().split(':')) #put products in tuple pairs
                    products.append(product_key_value)
            global daily_log_dic #not best practise / dictionary for products and their values
            try:
                daily_log_dic = dict(products) #dictionary from tuple pairs
            except:
                print('Possible Type: Please Check Log File')
        current_dir = './' + log_file
        mv_dir = 'OldLogs/Old'+ log_file #desitination and rename log file
        os.rename(current_dir, mv_dir) #move used log file
        compare_log_database()
    except:
        print('Invalid log file.')
# Compare Log to Database
def open_csv():
    csv_f = 'detailing_database.csv' #input("Input Database File Here: ")
    csv_database = pd.read_csv(csv_f) #read database
    csv_name = list(csv_database['Name']) #Names to list
    csv_case_name = list((item.casefold() for item in csv_name)) #change to Case Insensitive
    return csv_f, csv_database, csv_case_name, csv_name;
def compare_log_database():
    csv_f, csv_database, csv_case_name, csv_name = open_csv()
    for key in daily_log_dic.keys():
        value = daily_log_dic[key]
        if key.startswith('Recorded'):
            print(f'{key} : {value}')
            if key == 'Recorded_Date':
                date = value
                date = date.strip()
                if value not in csv_database.head(0):
                    csv_database[date] = "" #define new column based on date
                    csv_database.to_csv(csv_f, index=False) #push to csv
        # If Exist Set:
        elif key.casefold() in csv_case_name:
            print('Checking Product...')
            using = True #
            logged = True
            exist_in_database(key, using, logged, value, date)
            low_notify(key, value) #Notify if Low
        # Add new product to database file
        else:
            print(f'\nNew Product Found: {key}\n ')
            yes_no = input('-Add To Database? Y/N: ')
            if yes_no.lower() in yes_list:
                using = True
                logged = True
                add_to_database(key, using, logged, value, date)    
                low_notify(key, value) #Notify if Low

def exist_in_database(name, using, logged, value, date):
    csv_f, csv_database, csv_case_name, csv_name = open_csv()
    print(f"{name}: Already Exists" )
    if using == True:
        csv_database.loc[csv_name.index(name),'InUse'] = True #set InUse to True
    if logged == True:
        csv_database.loc[csv_name.index(name), date] = float(value) #record date usage
        csv_database.to_csv(csv_f, index=False) #push to csv
    
def add_to_database(name, using, logged, value, date):
    csv_f, csv_database, csv_case_name, csv_name = open_csv()
    csv_name.append(name)# IMPORTANT Update list so new product can be found in csv_name
    csv_category = set(csv_database['Category']) # set of Categories to prevent duplicates
    print(f'Exisiting Categories: {csv_category}')
    category = input('-Input Category: ')
    overall_price =  usr_input_num("-Input Price: ") # define Price
    unit_quantity =  usr_input_num("-Input Unit Quantity: ") # define Unit Quantity
    extra = usr_input_num("-Input Quantity Bought: ") # define extra
    unit_price = overall_price / unit_quantity # calc UnitPrice
    ratio =  usr_input_ratio('-Input Ratio') # define ratio
    single_use =  usr_input_boolean('-Single use? True or False: ')
    new_row = {'Name': name,
                'Category': category,
                'OverallPrice': overall_price,
                'UnitQuantity': unit_quantity,
                'Extra': extra,
                'UnitPrice': unit_price, 
                'Ratio': ratio,
                'InUse': False,
                'SingleUse': single_use}
    csv_database.loc[len(csv_database)] = new_row #create new row
    if using == True:
        csv_database.loc[csv_name.index(name),'InUse'] = True
    if logged == True:
        csv_database.loc[csv_name.index(name), date] = float(value)
    csv_database.to_csv(csv_f, index=False)#push to csv
    print(csv_database.loc[[csv_name.index(name)],:])

def order_product(name):
    csv_f, csv_database, csv_case_name, csv_name = open_csv()
    usr_quantity = usr_input_num('-Input Quantity of Product: ')
    price = csv_database.loc[csv_name.index(name),'OverallPrice']
    total = float(price) * float(usr_quantity)
    with open('productorder.txt', 'a') as product_order:
        product_order.write('\n' + str(usr_quantity) + ', ' + name + ', ' + str(price) + ', ' + str(total))
        print('\n   Added To: productorder.txt\n')

def low_notify(name, value):
    if not name.startswith('Recorded'):
        csv_f, csv_database, csv_case_name, csv_name = open_csv()
        if csv_database.loc[csv_name.index(name),'SingleUse'] in [True, 'TRUE', 'True']: #Not SingleUse, no need for 20%
            unit_quantity = csv_database.loc[csv_name.index(name),'UnitQuantity']
            extra = csv_database.loc[csv_name.index(name),'Extra']
            amount_left = (unit_quantity * extra) - float(value)
            if amount_left <= (unit_quantity * extra)*.2: #Calculate 20% and compare to Total Amount left
                print("\n   WARNING UNDER '20%' LEFT!    \n")
                yes_no = input('-Order More Product? Y/N: ')
                if yes_no.lower() in yes_list:
                    order_product(name)
                    
def search_database():
    csv_f, csv_database, csv_case_name, csv_name = open_csv()
    name = input('-Input Product: ')
    using = usr_input_boolean('-Currently in use? True or False: ') #change logged to set InUse to true or false
    logged = False
    value = None
    date = None
    if name.casefold() in csv_case_name:
        exist_in_database(name, using, logged, value, date)
        print(csv_database.loc[[csv_name.index(name)],:])
    else:
        print(f'\nNew Product: {name}\n ')
        yes_no = input('-Add To Database? Y/N: ')
        if yes_no.lower() in yes_list:
            add_to_database(name, using, logged, value, date)

def calculate_leastsquare():
    csv_f, csv_database, csv_case_name, csv_name = open_csv()
    date_names = []
    date_data = []
    for dates in csv_database:
        if re.match("^([0]?[1-9]|[1|2][0-9]|[3][0|1])[./-]([0]?[1-9]|[1][0-2])[./-]([0-9]{4}|[0-9]{2})$", dates):
            date_names.append(dates)
    if len(date_names) < 3:
        print('Not Enough Log Data Available!')
    name = input('-Input Product: ')
    try:
        for dates in date_names:
            date_data.append(csv_database.loc[csv_name.index(name),dates])
        date_data = pd.Series(date_data, dtype=object).fillna(0).tolist()
        unit_quantity = csv_database.loc[csv_name.index(name),'UnitQuantity']
        extra = csv_database.loc[csv_name.index(name),'Extra']
        total_amount = (unit_quantity * extra)
        print(f'{name} Available Data: {date_data}')
        limit = 0
        while 0 <= limit <= float(total_amount):
            x = []
            i = 0
            xy = []
            xsqr = []
            while i < len(date_data):
                x.append(i)
                xy.append(x[i] * date_data[i])
                xsqr.append(pow(x[i], 2))
                i += 1
            sum_x = sum(x)
            sum_data = sum(date_data)
            sum_xy = sum(xy)
            sum_xsqr = sum(xsqr)
            m = ((len(date_data)*sum_xy)-(sum_x*sum_data))/((len(date_data)*sum_xsqr)-(pow(sum_x,2)))
            b = (sum_data-(m*sum_x))/len(date_data)
            y = (m*len(x)) + b
            limit = y + sum_data
            date_data.append(y)
        if limit <= 0:
            print('Projected Usage Approaches 0 before running out. Provide more data!')
            
        elif limit >= 100:
            print(f'Projected {len(date_data)-1} Days Left!')
            line_graph(x, date_data, name)
    except:
        print(f'No Forecast Data Available For {name}')
        line_graph(x, date_data, name)

def line_graph(x, y, name):
    plt.plot(x, y)  # Line Graph    
    plt.xlabel('Days')
    plt.ylabel('Usage')
    plt.title(name + ' Graph')
    plt.show() 

def calculate_cost():
    pass

# Main
yes_list = ['y', 'yes']
daily_log_dic = {} #incase open_log() doesnt run
while True:
    print("""
    Inventory Manager
    Options:
    Process Log File            = (1)
    Linear Regression Forecast
    (3 Logs Required)           = (2)
    Search/Add Database         = (3)
    Add Product to Order        = (4)
    Display Database            = (5)
    Calculate Log Cost          = (6)     
          """)
    usr = usr_input_num('-Input a Number: ')

    match usr:
        case 1: #Process Log
            open_log()
        case 2: # Forecast
            calculate_leastsquare()
        case 3: # Search
            search_database()
        case 4: # Order
            name = input('-Input Name of Product: ')
            order_product(name)
        case 5: # Display Database
            csv_f, csv_database, csv_case_name, csv_name = open_csv()
            pd.set_option('display.max_rows', 1000)
            print(csv_database)
        

    exit = input('\nExit? Y/N: ')
    print('\n')
    if exit.lower() in yes_list:
        print('Exiting...')
        break



