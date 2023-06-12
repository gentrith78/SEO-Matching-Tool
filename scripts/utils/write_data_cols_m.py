import string
import time

"""
Write the desired output and actual outputs:
Mode 1: Writes each output from filters one by one
Mode 2: Writes the desired outputs all at once
"""

UPPERCASE = list((l for l in string.ascii_uppercase))

def write_data_cols(worksheet, data_to_write, total_rows, row_index, first_data_col_index, length_cols,mode:int):
    if mode == 1:
        # ACCEPTED STRUCTURE
        """
        data_to_write = {
            0:'outputted categories',
            2:'outputted Is english',
            4:'outputted Forgein domain',
        }
        """
        cell_list = worksheet.range(f'{UPPERCASE[first_data_col_index-1]}{row_index}:{UPPERCASE[length_cols-1]}{row_index}')
        for ind_,cell in enumerate(cell_list):
            if ind_ in [1,3,5]:
                print(cell.col)
                cell.value = data_to_write[ind_]
            pass
        worksheet.update_cells(cell_list)
    if mode == 2:
        # ACCEPTED STRUCTURE
        """
        data_to_write = {
            0:'desired categories',
            2:'desired Is english',
            4:'desired Forgein domain',
        }
        """
        print(data_to_write)
        # Fill Desired Categories
        cell_list = worksheet.range(f'{UPPERCASE[first_data_col_index-1]}{2}:{UPPERCASE[first_data_col_index-1]}{total_rows}')
        for cell in cell_list:
            cell.value = data_to_write[0]
        worksheet.update_cells(cell_list)
        time.sleep(1)
        print('wrotted 1')
        # Fill Desired Is English
        cell_list = worksheet.range(f'{UPPERCASE[(first_data_col_index + 2)-1]}{2}:{UPPERCASE[(first_data_col_index + 2)-1]}{total_rows}')
        for cell in cell_list:
            cell.value = data_to_write[2]
        worksheet.update_cells(cell_list)
        time.sleep(1)
        print('wrotted 2')
        # Fill Desired Foreign Domain
        cell_list = worksheet.range(f'{UPPERCASE[(first_data_col_index + 4)-1]}{2}:{UPPERCASE[(first_data_col_index + 4)-1]}{total_rows}')
        for cell in cell_list:
            cell.value = data_to_write[4]
        worksheet.update_cells(cell_list)
        print('wrotted 3')
if __name__ == '__main__':
    print(UPPERCASE[8-1])

    pass