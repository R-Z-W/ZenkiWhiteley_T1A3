import pandas as pd
import os
import re
import matplotlib.pyplot as plt
import os
import shutil

def main():
    while True:
        cls()
        print("""
        Inventory Manager
        Options:
        Process Log File            = (1)
        Linear Regression Forecast
        (3 Logs Required)           = (2)
        Search/Add Database         = (3)
        Add Product to Order        = (4)
        Display Database            = (5)
        Reset Program               = (6)    
            """)
        usr = usr_input_num('-Input a Number: ')
        match usr:
            case 1: #Process Log
                cls()
                # BUG make sure log files are inserted in order else dates will not align in csv
                log_names = get_log_names() # Display Available Log Files
                if len(log_names) > 1:
                    if yes_no_check('\n-Open Multiple Log Files Y/N: ') == True:
                        for log_file in log_names:
                            if open_log(log_file) == True: #If Successful move onto next functions
                                move_to_OldLogs(log_file) # Move Log File
                                compare_log_database()
                elif len(log_names) <= 1:
                    log_file = input('-Input Oldest Daily Log File: ')
                    if open_log(log_file) == True: #If Successful move onto next functions
                        move_to_OldLogs(log_file) #Move Log File
                        compare_log_database()
                # No Log Files is handled in get_log_names()
                        
            case 2: # Forecast
                cls()
                csv_f, csv_database, csv_name = open_csv()
                print(f'Available Products:\n {csv_name} \n')
                name = input('-Input Name of Product: ')
                date_names = get_dates_names()
                try:
                    date_data = get_dates_data(date_names, name)
                    total_amount = calculate_total_amount(name)
                    if len(date_names) < 3: # Not enough data check. Must have atleast 3 logs
                        print('Not Enough Log Data Available! Must Have 3 Entries Available')
                    else:
                        calculate_leastsquare_to_limit(name, date_data, total_amount)
                except Exception as e:
                    print(e)
                    print('Error: Invalid Name')

            case 3: # Search #BUG NEED FIX
                cls()
                csv_f, csv_database, csv_name = open_csv()
                print(f'Available Products:\n {csv_name} \n')
                name = input('-Input Name of Product: ')
                using = usr_input_boolean('-Currently InUse? True or False: ') #Change InUse to True or false
                try:
                    search_database(name, using)
                except Exception as e:
                    print(e)
                    print('Error: Invalid Name')
            
            case 4: # Order
                cls()
                name = input('-Input Name of Product: ')
                order_product(name)

            case 5: # Display Database
                cls()
                display_database()

            case 6:
                cls()
                reset()

        if yes_no_check('\nExit? Y/N: ') == True:
            print('Exiting...')
            break

# User Input Try Functions
def usr_input_num(prompt):
    while True:
        num = input(prompt)
        try:
            num = float(num)
            return num
        except Exception as e:
            print(e)
            print("Invalid number, Try Again")
def usr_input_boolean(prompt):
    while True:
        bool_in = input(prompt)
        if bool_in in ['True', 'False']:
            return bool_in
        else:
            print("Invalid Entry, Try True or False")

def usr_input_ratio(prompt):
    print(prompt)
    try:
        ratio_1 = usr_input_num('-First Number: ')
        ratio_2 = usr_input_num('-Second Number: ')
        if ratio_1 == ratio_2:
            ratio_in = 1
        else:
            ratio_in = str(ratio_1) + ':' + str(ratio_2)
        return ratio_in
    except Exception as e:
            print(e)
            print("Invalid ratio Number")
def yes_no_check(prompt):
    yes_list = ['y', 'yes']
    yes_no = input(prompt)
    if yes_no.lower() in yes_list:
        return True

# Reset Files Back To Normal
def reset():
    print('Reseting')
    try:
        try:
            with os.scandir('./OldLogs') as old_logs:
                for log in old_logs:
                    if log.is_file():
                        os.unlink(log.path)
            print("All Old Logs deleted.")
        except OSError:
            print('Error: OldLog Files Delete Failure')
        try:
            with os.scandir('./') as old_data:
                for data in old_data:
                    data_name = data.name
                    if data_name in ['detailing_database.csv', 'productorder.txt']:
                        os.unlink(data.path)
                print("All Database & Order Files Deleted.")
        except:
            print('Error: Database & Order Form Delete Failure')
        try:
            with os.scandir('./BackupData') as new_file:
                for file in new_file:
                    if file.is_file():
                        file = file.name
                        curr_dir = './BackupData/'+file
                        dest_dir = './'+file
                        print(curr_dir)
                        print(dest_dir)
                        shutil.copyfile(curr_dir, dest_dir)
                    else:
                        continue       
        except:
            print('Error: Backup Data Failure!')
    except:
        print('Error: Reset Failure!')

#Clear Console
def cls():
    os.system('cls' if os.name=='nt' else 'clear') # For Windows Linux Apple

# Find And Print Available Log Files In Current Directory
def get_log_names():
    print('Available Log Files:') 
    log_names = [] # Get Log Files Names in current dir
    try:
        for files in os.scandir('.'): #Scan for files
            if files.is_file(): #If file not folder
                log = files.name #Get File name
                if log.startswith('Log'): #If file starts with Log
                    log_names.append(log) #Add to List
        log_names = sorted(log_names) # Sort Log Files Names:
        for item in log_names: 
            print(item)  # Print Sorted Log Files Names:
        return log_names
    except Exception as e:
        print(e)
        print('Error: Missing Log Files')

# Move used log files to OldLogs folder
def move_to_OldLogs(log_file):
    try:
        current_dir = './' + log_file
        old_log_dir = 'OldLogs/Old'+ log_file # desitination and rename log file
        os.rename(current_dir, old_log_dir) # move used log file
    except Exception as e:
        print(e)
        print('Error: Failed to Move, Check for OldLogs Folder')
    
# Open Log & Copy Content to List/Dictionary & Move File
def open_log(log_file):
    try:
        with open(log_file, "r") as daily_log: # If failed to open Invalid
            products = []
            for line in daily_log:
                if line.startswith('#'): # Remove Comments from Log
                    continue
                else: 
                    product_key_value = tuple(line.strip().split(':')) # Extract Data Into Tuple Pairs
                    products.append(product_key_value)
            try:
                global daily_log_dic # IMPORTANT! Not Best Practise
                daily_log_dic = dict(products) # Dictionary from Tuple pairs
                return True #If Successful
            except Exception as e:
                print(e)
                print('Error: Please Check Log File Colons') # Dictionary Fails to be Created if Colon missing
    except Exception as e:
        print(e)
        print('Error: Failed to Open, Invalid log file.')

# Open csv and create list of names in csv to compare to
def open_csv():
    try:
        csv_f = 'detailing_database.csv' #!Important Change for Different database.csv
        csv_database = pd.read_csv(csv_f) # Read database                                                        ***ACCESS COLUMNS***
        csv_name = list(csv_database['Name']) # Names to List                                                    ***ACCESS ROWS***
        return csv_f, csv_database, csv_name;
    except Exception as e:
        print(e)
        print('Error: Failed to Open Csv')

# Casefold csv_name
def csv_name_casefold(csv_name):
    csv_case_name = list((item.casefold() for item in csv_name)) # For Case Insensitive check
    return csv_case_name

# Create Column in csv
def create_date_column(value):
    csv_f, csv_database, csv_name = open_csv() #Run Check on csv for new values
    date = value
    date = date.strip() #!Important Remove White Space
    if value not in csv_database.head(0):
        csv_database[date] = "" #define new column based on date
        csv_database.to_csv(csv_f, index=False) #push to csv
    return date

# Compare Log to Database, Takes in log files
def compare_log_database():
    csv_f, csv_database, csv_name = open_csv() #Run Check on csv for new values
    csv_case_name = csv_name_casefold(csv_name)
    for key in daily_log_dic.keys():
        value = daily_log_dic[key]
        if value == None:
            print(f'Error: No Value Found For Key: {key}')
        elif key.startswith('Recorded'):
            print(f'{key} : {value}') # Print Recorded Keys and Values
            if key == 'Recorded_Date':
                date = create_date_column(value) # Takes in keys value (e.g. Date 20/12/2023)
        else:
            if date == None:
                print('Error: No Date')
            elif key.casefold() in csv_case_name: # If Exist Set:
                print('Checking Product...')
                exist_in_database(key, value, date)
                low_notify(key, value) #Notify if Low
            else: # Add new product to database file
                print(f'\nNew Product Found: {key}\n ')
                if yes_no_check('-Add To Database Y/N: ') == True:
                    using = True
                    # logged = True
                    add_to_database(key, using, value, date)    
                    low_notify(key, value) #Notify if Low

# Exists in database, update to InUse to true + add log data
def exist_in_database(name, value, date):
    csv_f, csv_database, csv_name = open_csv() #Run Check on csv for new values
    print(f"{name}: Already Exists" )
    csv_database.loc[csv_name.index(name),'InUse'] = True #set InUse to True
    if date != None:
        csv_database.loc[csv_name.index(name), date] = float(value) #record date usage
    csv_database.to_csv(csv_f, index=False) # Push to csv
    
# Add to database, update to InUse to true + add log data
def add_to_database(name, using, value, date):
    csv_f, csv_database, csv_name = open_csv() #Run Check on csv for new values
    csv_name.append(name)# IMPORTANT Update list so new product can get index in csv_name
    column = 'Category'
    display_column_value(column)
    category = input('-Input Category: ')
    overall_price =  usr_input_num("-Input Price: ") # Define Price
    unit_quantity =  usr_input_num("-Input Unit Quantity: ") # Define Unit Quantity
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
                'SingleUse': single_use} # New Entry Created as Dictionary
    csv_database.loc[len(csv_database)] = new_row # Create New Row In database
    if using == True: # Adjust InUse in database
        csv_database.loc[csv_name.index(name),'InUse'] = True
    if date != None: # Adjust Date Values in database
        csv_database.loc[csv_name.index(name), date] = float(value)
    csv_database.to_csv(csv_f, index=False) # Push To csv
    print(csv_database.loc[[csv_name.index(name)],:]) # Print Result

#Place Order in productorder.txt
def order_product(name):
    csv_f, csv_database, csv_name = open_csv() #Run Check on csv for new values
    usr_quantity = usr_input_num('-Input Quantity of Product: ') #Quantity needed
    try:
        overall_price = csv_database.loc[csv_name.index(name),'OverallPrice']
        total_cost = overall_price * usr_quantity
        try:
            with open('productorder.txt', 'a') as product_order:
                product_order.write('\n' + str(usr_quantity) + ', ' + name + ', ' + str(overall_price) + ', ' + str(total_cost))
                print('\n   Added To: productorder.txt\n')
        except Exception as e:
            print(e)
            print('Error: Could Not Find productorder.txt')
    except Exception as e:
        print(e)
        print('Error: Product Does Not Exist. Please Add In Search/Add Database(3) First')
    

#Notifty When Amount is Below 20%
def low_notify(name, value):
    if not name.startswith('Recorded'): #Skip Recorded
        csv_f, csv_database, csv_name = open_csv() #Run Check on csv for new values
        if csv_database.loc[csv_name.index(name),'SingleUse'] in [True, 'TRUE', 'True']: #Not SingleUse, no need for 20%
            total_amount = calculate_total_amount(name)
            amount_left = total_amount - float(value)#Caluclate Max Quantity Left
            if amount_left <= total_amount*.2: #Calculate 20% of Max Quantity and compare to Total Amount left
                print("\n   WARNING UNDER '20%' LEFT!    \n")
                if yes_no_check('-Add To Order Y/N: ') == True:
                    order_product(name)

# Compare Input to Database, takes in usr input                
def search_database(name, using):
    csv_f, csv_database, csv_name = open_csv() #Run Check on csv for new values
    csv_case_name = csv_name_casefold(csv_name)
    value = None  #Empty values for add_to_database # Wont be called but need for add_in_database & exist_in_database
    date = None  #Empty values for add_to_database
    if name.casefold() in csv_case_name: #Check if already exists
        exist_in_database(name, value, date)
        print(csv_database.loc[[csv_name.index(name)],:])
    else:
        print(f'\nNew Product: {name}\n ') #Ask if want in database
        if yes_no_check('-Add To Database Y/N: ') == True:
            add_to_database(name, using, value, date) #Add to database

# Find Date Names In csv
def get_dates_names():
    csv_f, csv_database, csv_name = open_csv() #Run Check on csv for new values
    date_names = []
    for column_names in csv_database: #get Dates from Columns Names
        if re.match("^([0]?[1-9]|[1|2][0-9]|[3][0|1])[./-]([0]?[1-9]|[1][0-2])[./-]([0-9]{4}|[0-9]{2})$", column_names): # If Regex match Get Dates from Columns Names
            date_names.append(column_names)
    return date_names

# Get Data From Dates In csv
def get_dates_data(date_names, name):
        csv_f, csv_database, csv_name = open_csv() #Run Check on csv for new values
        date_data = []
        for dates in date_names:
            date_data.append(csv_database.loc[csv_name.index(name),dates]) #Values From Dates
        date_data = pd.Series(date_data, dtype=object).fillna(0).tolist() #Turn Nan values = 0
        return date_data

# Calculate total amount from unit quantity and extra
def calculate_total_amount(name):
    csv_f, csv_database, csv_name = open_csv() #Run Check on csv for new values
    unit_quantity = csv_database.loc[csv_name.index(name),'UnitQuantity'] #get UnitQuantity
    extra = csv_database.loc[csv_name.index(name),'Extra'] #get Extra
    total_amount = (unit_quantity + unit_quantity * extra) #calculate Total Amount
    return total_amount

# For Forecast Calculation    
def calculate_leastsquare_to_limit(name, y, limit):
    try:        
        print(f'{name} Available Data: {y}')
        calc_amount = 0
        while 0 <= calc_amount <= float(limit): # Contine to calculate unit 0 or limit is reached
            x = []
            xy = []
            xsqr = []
            i = 0
            while i < len(y):
                x.append(i) # Range of number to the length of y
                xy.append(x[i] * y[i]) # Calculate x * y
                xsqr.append(pow(x[i], 2)) # Calculate x square root
                i += 1
            sum_x = sum(x)
            sum_data = sum(y)
            sum_xy = sum(xy)
            sum_xsqr = sum(xsqr)
            m = ((len(y)*sum_xy)-(sum_x*sum_data))/((len(y)*sum_xsqr)-(pow(sum_x,2)))
            b = (sum_data-(m*sum_x))/len(y)
            new_y = (m*len(x)) + b # Calculate new y value
            calc_amount = new_y + sum_data # New amount used to compare to 0 or limit
            y.append(new_y) # Append new y to y and go again with new list
        x.append(len(x)) # Make x the same length as y    
        if calc_amount <= 0:
            print('Projected Usage Approaches 0 before running out. Provide more data!')
            line_graph(x, y, name)
        elif calc_amount >= limit:
            print(f'Projected {len(y)-1} Days Left!')
            line_graph(x, y, name)
    except Exception as e:
        print(e)
        print(f'No Useable Data Available For {name}')

# Display Whole Database
def display_database():
    csv_f, csv_database, csv_name = open_csv() #Run Check on csv for new values
    pd.set_option('display.max_rows', 1000)
    print(csv_database)

# Display Specific Column
def display_column_value(column):
    csv_f, csv_database, csv_name = open_csv() #Run Check on csv for new values
    csv_column_values = set(csv_database[column]) # set of Categories to prevent duplicates
    print(f'Exisiting {column}: {csv_column_values}')

# Create Gaph
def line_graph(x, y, name):
    plt.plot(x, y)  # Line Graph    
    plt.xlabel('Days')
    plt.ylabel('Usage')
    plt.title(name + ' Graph')
    plt.show() 

    pass


#_____________MAIN_______________________-
#Global Variables
yes_list = ['y', 'yes']
daily_log_dic = {} #incase open_log() doesnt run
main()

