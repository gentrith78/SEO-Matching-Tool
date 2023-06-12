import sys
import os
import time
from tkinter import messagebox

import gspread

PATH = os.path.abspath(os.path.dirname(__file__))

DATA_COLUMNS = [{'Desired Categories':1}, {'Outputted Categories':2}, {'Desired Language':3}, {'Language':4},
                {'Desired Is Foreign Domain':5}, {'Outputed is Foreign Domain':6}]


def get_first_data_col(worksheet):
    ind = 0
    cols = worksheet.row_values(1)
    for ind_,col in enumerate(cols):
        if col == 'Desired Categories':
            ind = ind_+1
    return ind

def add_cols(wsheet):
    not_existing = DATA_COLUMNS
    col_values = wsheet.row_values(1)
    for col in col_values:
        for col_data_ in DATA_COLUMNS:
            if col in col_data_:
                for ind,exist_possible in enumerate(not_existing):
                    if exist_possible == col_data_:
                        not_existing.pop(ind)
    for data_col in not_existing:
        wsheet.insert_cols([[list(data_col.keys())[0]]], (len(col_values))+list(data_col.values())[0],inherit_from_before=True)
        wsheet.add_cols(6)
        time.sleep(2)
    pass


def read_g_sheet(g_sheet_url):
    #  service account
    try:
        sa = gspread.service_account(f'{PATH}\\service_account_creds\\{os.listdir(os.path.join(PATH, "service_account_creds"))[0]}')
        entire = sa.open_by_url(g_sheet_url)
        worksheet = entire.worksheets()[0]
        add_cols(worksheet)
        a = worksheet.range('')
        get_first_data_col(worksheet)
        return worksheet
    except:
        messagebox.showerror('Failed to Read', 'Failed to Read Spreadsheet')
        sys.exit()

if __name__ == '__main__':
    read_g_sheet('https://docs.google.com/spreadsheets/d/1HYJxfnlhulvkqGkB7JdNYcRxdzTAygZhBoKhzPvxxlk/edit#gid=0')

