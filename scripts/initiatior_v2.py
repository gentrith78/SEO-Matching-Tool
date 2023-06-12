import sys
import time
from tkinter import messagebox
import pandas as pd
import os

from filters import categorize, is_english, is_foreign_domain
from google_sheet_service import read_g_sheet, get_first_data_col
from db_service import check_database, save_to_database
from utils import logger, write_data_cols
from utils.processed_counter import write_status
###################################################
#                RECEIVING DATA FROM GUI
PATH = os.path.abspath(os.path.dirname(__file__))
#
instance_id = int(sys.argv[1])
# #
data_from_main_gui = []
instance_csv_file = pd.read_csv(f'{PATH}/instances.csv')
for ind,row in instance_csv_file.iterrows():
    if instance_csv_file.loc[ind,'id'] == instance_id:
        data_from_main_gui = row.values

# preparing GUI data
path_to_input = str(data_from_main_gui[1])
filter_categorization_api = str(data_from_main_gui[2]).split('@@!!@@')
filter_is_english = data_from_main_gui[3]
filter_foreign_domain = data_from_main_gui[4]


# google spreadsheet worksheet
try:
    worksheet = read_g_sheet(path_to_input)
    cols_ = worksheet.row_values(1)
    first_data_cols_index = get_first_data_col(worksheet)
    length_cols = len(cols_)
    length_rows = worksheet.row_count
    # Write desired data into columns into spreadsheet
    data_to_write_desired = {
        0: str(filter_categorization_api),
        2: filter_is_english,
        4: filter_foreign_domain,
    }
    time.sleep(5)
    write_data_cols(worksheet,data_to_write_desired,length_rows,2,first_data_cols_index,length_cols,2)
    time.sleep(5)
    logger().info('Desired Filters wroted to Spreadsheet')
except:
    messagebox.showerror('Failed to Read', 'Failed to Read Spreadsheet')
    sys.exit()

###################################################
#                FUNCTIONS
def verify_filters_output(data_of_url):
    if len(data_of_url['categories']) == 0 or 'Not enough content' in data_of_url['categories'][0]:
        logger().info('Error with categorization api')
        logger().info(data_of_url['categories'])
        return False
    if data_of_url['is_english'] == '' or str(data_of_url['is_english']).isspace() or str(data_of_url['is_english']).isdigit():
        logger().info('Error with web scraping api')
        logger().info(data_of_url['is_english'])
        return False
    return True

def call_filters(url, row_index):
    categories_ = categorize(url)
    is_english_ = is_english(url)
    raw_language = is_english_
    if is_english_ == 'en':
        is_english_ = 'Yes'
    else:
        is_english_ = 'No'
    is_foreign_domain_ = is_foreign_domain(url)
    if  is_foreign_domain_ == True:
        is_foreign_domain_ = 'Yes'
    is_foreign_domain_ =  "No"
    data_of_url = {
        'categories':categories_,
        'is_english':is_english_,
        'is_foreign_domain':is_foreign_domain_
    }
    save_to_database(url,categories_,is_english_,is_foreign_domain_)
    data_to_write_output = {
        1: str(categories_),
        3: str(raw_language),
        5: str(is_foreign_domain_),
    }
    write_data_cols(worksheet, data_to_write_output, length_rows, row_index, first_data_cols_index, length_cols, 1)
    return data_of_url

def compare_data(data_of_url):
    #verify output of filters
    if verify_filters_output(data_of_url) == False:
        return None
    to_pass = 0
    passed = 0
    if len(filter_categorization_api) >= 1:
        logger().info('c')
        to_pass +=1
        for category in filter_categorization_api:
            if category.rstrip().lstrip() in data_of_url['categories']:
                logger().info('pass c')
                passed+=1
                break
    else:
        pass
    if filter_is_english != 'Disabled' and data_of_url['is_english'] != '':
        logger().info('e')
        to_pass +=1
        if filter_is_english == data_of_url['is_english']:
            logger().info('pass e')
            passed +=1
    else:
        pass
    if filter_foreign_domain != 'Disabled' and data_of_url['is_foreign_domain'] != '':
        logger().info('d')
        to_pass +=1
        if filter_foreign_domain == data_of_url['is_foreign_domain']:
            logger().info('pass d')
            passed +=1
    else:
        pass
    logger().info(f"Desired Categorization: {filter_categorization_api} --- Response Categorization: {data_of_url['categories']}")
    logger().info(f"Desired is_English: {filter_is_english} --- Response is_English: {data_of_url['is_english']}")
    logger().info(f"Desired foreign_Domain: {filter_foreign_domain} --- Response foreign_Domain: {data_of_url['is_foreign_domain']}")
    if to_pass == passed:
        logger().info('Relevancy = True')
        logger().info(f'to_pass: {to_pass} -- passed: {passed}')
        return True
    logger().info('Relevancy = False')
    logger().info(f'to_pass: {to_pass} -- passed: {passed}')
    return False


###################################################
#                    ITERATE
for row in range(2,worksheet.row_count):
    row_data_ = worksheet.row_values(row)
    url_to_check = str(row_data_[1])
    logger().info(f'Checking {url_to_check}')
    pass
    ###################################################
    #                CHECK DATABASE
    database_result = check_database(worksheet.row_values(row)[1]) # this var will be like data_of_url type
    if database_result != None:
        logger().info('In Database')
        relevancy = compare_data(database_result)
        if relevancy == True:
            worksheet.update(f'G{row}', 'Yes')
        if relevancy == False:
            worksheet.update(f'G{row}', 'No')
        if relevancy == None:
            worksheet.update(f'G{row}', 'Couldn\'t Determine')
        time.sleep(3)
    else:
        logger().info('Applying Filters')
        try:
            filters_output = call_filters(url_to_check,row)
        except Exception as e:
            logger().error(f'Error while calling filters:: {e}')
            continue
        # True or False
        relevancy = compare_data(filters_output)
        time.sleep(3)
        if relevancy == True:
            worksheet.update(f'G{row}', 'Yes')
        if relevancy == False:
            worksheet.update(f'G{row}', 'No')
        if relevancy == None:
            worksheet.update(f'G{row}', 'Couldn\'t Determine')
    logger().info(f'Finished {url_to_check}')
    write_status(f'{row} out of {worksheet.row_count} Completed')
    logger().info('##############################################')
    continue
write_status('FINISHED')


