import pandas as pd
import os
import re
import matplotlib.pyplot as plt
import shutil
from enum import Enum

# Global variables
csv_file = 'detailing_database.csv'
daily_log_dic = {}  # Initialize an empty dictionary

def main():
    while True:
        cls()
        display_menu_options()
        usr_choice = usr_input_num('-Input a Number: ')

        match usr_choice:
            case 1:
                cls()
                main_process_logs()

            case 2:
                cls()
                main_usr_forecast()

            case 3:
                cls()
                main_usr_search_database_input()

            case 4:
                cls()
                main_usr_add_product_to_order_input()

            case 5:
                cls()
                main_display_database()

            case 6: 
                cls()
                main_reset()

        if yes_no_check('\nExit? Y/N: '):
            print('Exiting...')
            break
#------------------------------------------------------------------------
# Display Menu Options
def display_menu_options():
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
# Display Log Files: in root directory
def display_log_files():
    print('Available Log Files:')
    try: # Scan for files in root, if is file, get file name, if file starts with Log, add to list
        log_names = [log.name for log in os.scandir('.') if log.is_file() and log.name.startswith('Log')]
        log_names.sort()
        for item in log_names:
            print(item)
        return log_names
    except : #Exception as e
        # print(e)
        print('Error: Missing Log Files')
# Display Whole Database
def main_display_database():
    _, csv_database, _ = open_csv() #Run Check on csv for new values
    pd.set_option('display.max_rows', 1000)
    print(csv_database)
# Display Specific Column
def display_column_value(column):
    try:
        _, csv_database, _ = open_csv()
        csv_column_values = set(csv_database[column])
        print(f'Existing {column}: {csv_column_values}')
    except:
        print('Error: Column Could Not Be Found!')
# Display Create Graph
def line_graph(x, y, name):
    plt.plot(x, y)
    plt.xlabel('Days')
    plt.ylabel('Usage')
    plt.title(name + ' Graph')
    plt.show()
# Display Clean Terminal
def cls():
    os.system('cls' if os.name=='nt' else 'clear')  # For Windows Linux Apple
#------------------------------------------------------------------------
# Check Number Input
def usr_input_num(prompt):
    while True:
        try:
            num = float(input(prompt))
            return num
        except ValueError:
            print("Invalid number, Try Again")
# Check Boolean Input
def usr_input_boolean(prompt):
    while True:
        bool_in = input(prompt)
        if bool_in.lower() in ['true', 'false']:
            return bool_in
        else:
            print("Invalid Entry, Try True or False")
# Check Ratio Input
def usr_input_ratio(prompt):
    while True:
        print(prompt)
        try:
            ratio_1 = usr_input_num('-First Number: ')
            ratio_2 = usr_input_num('-Second Number: ')
            if ratio_1 == ratio_2:
                ratio_in = "1.0" 
            else:
                ratio_in = f"{float(ratio_1)}:{float(ratio_2)}" #f String how cool is that!
            return ratio_in
        except ValueError:
            print("Invalid ratio Number")
# Check Yes or No Input
def yes_no_check(prompt):
    while True:
        yes_list = ['y', 'yes']
        no_list = ['n', 'no']
        yes_no = input(prompt).lower()
        if yes_no in yes_list:
            return True
        elif yes_no in no_list:
            return False
        else:
            print("Invalid Yes or No, Try Again")
#------------------------------------------------------------------------
# Open csv & Make Name List
def open_csv():
    try:
        csv_file = 'detailing_database.csv'
        csv_database = pd.read_csv(csv_file)
        csv_names = list(csv_database['Name'])
        return csv_file, csv_database, csv_names
    except: #Exception as e
        #print(e)
        print('Error: Failed to Open Csv')
# Get Date Names In csv
def get_dates_names():
    _, csv_database, _ = open_csv()  
    date_names = [] #Possible List Comprehension Here
    for column_names in csv_database.columns: # PANDAS HAS .columns USED IN column check aswell
        if re.match("^([0]?[1-9]|[1|2][0-9]|[3][0|1])[./-]([0]?[1-9]|[1][0-2])[./-]([0-9]{4}|[0-9]{2})$", column_names): # If Regex match Get Dates from Columns Names
            date_names.append(column_names)
    return date_names
# Get Data From Dates In csv
def get_dates_data(date_names, name):
    _, csv_database, csv_names = open_csv()
    date_data = []
    for dates in date_names:
            date_data.append(csv_database.loc[csv_names.index(name),dates]) #Values From Dates
    date_data = pd.Series(date_data, dtype=object).fillna(0).tolist()  #Turn Nan values = 0
    return date_data
# Casefold csv_names: checking against usr input
def csv_names_casefold(csv_names): # Just Return A List, Dont Need To Create A List Name
    return [name.casefold() for name in csv_names] #Changed To pandas array instead of list (having issues in test)
#------------------------------------------------------------------------
# Open Log & Copy Content: to list/dictionary
def open_log(log_file):
    try:
        with open(log_file, "r") as daily_log: # List Comprehensioned, Make tuple pairs from log file if data doesnt start with #
            products = [tuple(line.strip().split(':')) for line in daily_log if not line.startswith('#')]
            global daily_log_dic # IMPORTANT! Not Best Practise But REQUIRED !!!!!!!!!!!!!!!!
            daily_log_dic = dict(products)
            return True
    except: #Exception as e
        #print(e)
        print('Error: Failed to Open, Invalid log file Or Missing Colons.')  # TO MANY EXCEPTION SO I SHRINK TO 1 LOOKS NICER
        return False
#------------------------------------------------------------------------
# Decide Multiple or Single Logs
def main_process_logs():
    log_names = display_log_files()
    usr_multiple_logs = False

    if len(log_names) > 1:
        usr_multiple_logs = yes_no_check('\n-Open Multiple Log Files Y/N: ')

        if usr_multiple_logs: # If True
            for log_file in log_names:
                process_single_log(log_file)
            return # Important Or It Will Ask BELOW

    log_file = input('-Input Oldest Daily Log File: ')
    process_single_log(log_file)
# Process log file
def process_single_log(log_file):
    if open_log(log_file): # If True
        move_to_old_logs(log_file)
        log_compare_database()
# Move Renamed Log To Folder: used Log renamed OldLog and moved to OldLogs folder
def move_to_old_logs(log_file):
    try:
        current_dir = './' + log_file
        old_log_dir = 'OldLogs/Old' + log_file
        os.rename(current_dir, old_log_dir)
    except: #Exception as e
        # print(e)
        print('Error: Failed to Move, Check OldLogs Folder')
#------------------------------------------------------------------------
# Compare Log To Database
def log_compare_database():
    _, _, csv_names = open_csv()
    print(daily_log_dic)
    for key, value in daily_log_dic.items():
        if value is None:
            print(f'Error: No Value Found For Key: {key}')
        elif key.startswith('Recorded'):
            print(f'{key} : {value}') # Print Recorded Keys and Values
            if key == 'Recorded_Date':
                date = create_date_column(value) # Takes in keys value (e.g. Date 20/12/2023)
        else:
            if date is None:
                print('Error: No Date')
            elif key.casefold() in csv_names_casefold(csv_names): # If Exist in Set:
                print('Checking Product...')
                exist_in_database(key, value, date)
                low_notify(key, value)
            else:
                print(f'\nNew Product Found: {key}\n ')
                if yes_no_check('-Add To Database Y/N: '):
                    using = True
                    absent_in_database(key, using, value, date)
                    low_notify(key, value)
#------------------------------------------------------------------------
# Usr Input For Searching Database
def main_usr_search_database_input():
    _, _, csv_names = open_csv()
    print(f'Available Products:\n {csv_names} \n')
    name = input('-Input Name of Product: ')
    is_using = usr_input_boolean('-Currently InUse? True or False: ')

    try:
        usr_compare_database(name, is_using)

    except : 
        # print(e)
        print('Error: Invalid Name')
# Compare Usr To Database
def usr_compare_database(name, using):
    _, csv_database, csv_names = open_csv()
    # Dont Need to declare value or date just put straight into function!
    if name.casefold() in csv_names_casefold(csv_names):
        exist_in_database(name, None, None)
        print(csv_database.loc[[csv_names.index(name)], :])
    else:
        print(f'\nNew Product: {name}\n ') #Ask if want in database
        if yes_no_check('-Add To Database Y/N: '):
            absent_in_database(name, using, None, None)
#------------------------------------------------------------------------
# Create Date Column
def create_date_column(date):
    _, csv_database, _ = open_csv()
    date = date.strip() #!Important Remove White Space

    if date not in csv_database.columns: # PANDAS HAS .columns THANK GOD????
        csv_database[date] = "" #define new column based on date
        csv_database.to_csv(csv_file, index=False)
    return date
#------------------------------------------------------------------------
# Update Input In Database
def exist_in_database(name, value, date):
    _, csv_database, csv_names = open_csv()
    print(f"{name}: Already Exists")

    index = csv_names.index(name) #Cleaner To have Seperate and reuse!!!
    csv_database.loc[index, 'InUse'] = True

    if date is not None:
        csv_database.loc[index, date] = float(value)

    csv_database.to_csv(csv_file, index=False)
# Add Input To Database
def absent_in_database(name, using, value, date):
    _, csv_database, csv_names = open_csv()

    csv_names.append(name)
    index = csv_names.index(name) #Again Cleaner
    # len(csv_database and csv_name.index(name) are the smae)

    category = input('-Input Category: ')
    overall_price = usr_input_num("-Input Price: ")
    unit_quantity = usr_input_num("-Input Unit Quantity: ")
    extra = usr_input_num("-Input Quantity Bought: ")
    unit_price = overall_price / unit_quantity
    ratio = usr_input_ratio('-Input Ratio')
    single_use = usr_input_boolean('-Single use? True or False: ')
    # New Entry Created as Dictionary
    new_row = {'Name': name,
               'Category': category,
               'OverallPrice': overall_price,
               'UnitQuantity': unit_quantity,
               'Extra': extra,
               'UnitPrice': unit_price,
               'Ratio': ratio,
               'InUse': False,
               'SingleUse': single_use}

    csv_database.loc[index] = new_row # Create New Row In database

    if using: # Adjust InUse in database
        csv_database.loc[index, 'InUse'] = True

    if date is not None: # Adjust Date Values in database
        csv_database.loc[index, date] = float(value)

    csv_database.to_csv(csv_file, index=False)
    print(csv_database.loc[[index], :])
#------------------------------------------------------------------------
# Add Usr Input To Order
def main_usr_add_product_to_order_input():
    name = input('-Input Name of Product: ')
    order_product(name)
# Place Order In productorder.txt
def order_product(name):
    _, csv_database, csv_names = open_csv()
    usr_quantity = usr_input_num('-Input Quantity of Product: ')

    try:
        overall_price = csv_database.loc[csv_names.index(name), 'OverallPrice']
        total_cost = overall_price * usr_quantity

        with open('productorder.txt', 'a') as product_order:
            product_order.write(f'\n{usr_quantity}, {name}, {overall_price}, {total_cost}')

        print('\n   Added To: productorder.txt\n')

    except: #Exception as e
        #print(e)
        print('Error: Product or productorder.txt Does Not Exist. Please Add In Search/Add Database(3) First')
# Notify When Amount is Below 20%
def low_notify(name, value):
    if not name.startswith('Recorded'):
        _, csv_database, csv_names = open_csv()
        if csv_database.loc[csv_names.index(name), 'SingleUse'] in [True, 'TRUE', 'True']: #False SingleUse, no need for 20%
            total_amount = calculate_total_amount(name)
            amount_left = total_amount - float(value) #Caluclate Max Quantity Left

            if 0 <= amount_left <= total_amount * 0.2: #Calculate 20% of Max Quantity and compare to Total Amount left
                print("\n   WARNING UNDER '20%' LEFT!    \n")
                if yes_no_check('-Add To Order Y/N: '):
                    order_product(name)
#------------------------------------------------------------------------
# Check Usr Input Valid For Forecast
def main_usr_forecast():
    _, _, csv_names = open_csv()
    print(f'Available Products:\n {csv_names} \n')
    name = input('-Input Name of Product: ')
    date_names = get_dates_names()

    try:
        date_data = get_dates_data(date_names, name)
        total_amount = calculate_total_amount(name)

        if len(date_names) < 3:
            print('Not Enough Log Data Available! Must Have 3 Entries Available')
        else:
            calculate_least_square_to_limit(name, date_data, total_amount)

    except: #Exception as e
        # print(e)
        print('Error: Invalid Name')
# Calculate Least Square Until Limit
def calculate_least_square_to_limit(name, y, limit):
    try:
        print(f'{name} Available Data: {y}') # Display If Data Is Available
        calc_amount = 0

        if limit <= 0:
            print('Error: Total Amount <= 0. Incorrect Data In Database! There Must Be Atleast 1.')
            return

        while 0 <= calc_amount <= float(limit):
            x = list(range(len(y))) # make Sure x is same length as y before calculation
            xy = [xi * yi for xi, yi in zip(x, y)] # Zip combines Both x and y into pairs in a list, Pairs are then timesed together :stack overflow
            xsqr = [xi ** 2 for xi in x] # Loop Through x and for each square x

            sum_x = sum(x)
            sum_data = sum(y)
            sum_xy = sum(xy)
            sum_xsqr = sum(xsqr)

            m = ((len(y) * sum_xy) - (sum_x * sum_data)) / ((len(y) * sum_xsqr) - (sum_x ** 2))
            b = (sum_data - (m * sum_x)) / len(y)
            new_y = (m * len(x)) + b

            calc_amount = new_y + sum_data
            y.append(new_y) # Append new y to y and go again with new list

        x.append(len(x)) # Make x the same length as y after exiting loop

        if calc_amount <= 0:
            print('Projected Usage Approaches 0 before running out. Provide more data!')
            line_graph(x, y, name)

        elif calc_amount >= limit:
            print(f'Projected {len(y) - 1} Days Left!')
            line_graph(x, y, name)

    except: #Exception as e
        #print(e)
        print(f'No Useable Data Available For {name}')
# Calculate Total Amount: from uniquantity and extra
def calculate_total_amount(name):
    _, csv_database, csv_names = open_csv()
    unit_quantity = csv_database.loc[csv_names.index(name), 'UnitQuantity']
    extra = csv_database.loc[csv_names.index(name), 'Extra']
    total_amount = (unit_quantity + unit_quantity * extra)
    return total_amount
#------------------------------------------------------------------------
# Reset Files
def main_reset():
    print('Reseting...')
    del_old_logs()
    del_database_and_order_file()
    backup_data()
# Delete All Files In OldLogs
def del_old_logs():
    try:
        with os.scandir('./OldLogs') as old_logs:
            for log in old_logs:
                if log.is_file():
                    os.unlink(log.path)
        print("All Old Logs deleted.")
    except:
        print('Error: OldLog Files Delete Failure')
# Delete Database & Order From Root
def del_database_and_order_file():
    try:
        with os.scandir('./') as old_data:
            for data in old_data:
                data_name = data.name
                if data_name in ['detailing_database.csv', 'productorder.txt']:
                    os.unlink(data.path)
            print("Database & Order File Deleted.")
    except:
        print('Error: Database & Order Form Delete Failure')
# Copy Backup Data Into Root
def backup_data():
    try:
        with os.scandir('./BackupData') as new_files:
            for file in new_files:
                if file.is_file():
                    file = file.name
                    old_dir = './BackupData/' + file
                    new_dir = './' + file
                    print(old_dir)
                    print(new_dir)
                    shutil.copyfile(old_dir, new_dir)
                else:
                    continue
    except:
        print('Error: Backup Data Failure!')
#------------------------------------------------------------------------

if __name__ == "__main__":
    main()
