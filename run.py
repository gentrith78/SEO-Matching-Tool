import random
import time
import os
from tkinter import *
from tkinter import messagebox
import tkinter as tk
import pandas as pd
import subprocess
from scripts.google_sheet_service import read_g_sheet
from scripts.utils.processed_counter import read_status

PATH = os.path.abspath(os.path.dirname(__file__))

win = Tk()
win.geometry("1000x650")

# main
main_frame = Frame(win)
main_frame.pack(fill=BOTH, expand=1)

# canvas
my_canvas = Canvas(main_frame,background='#D9D9D9')
# my_canvas.pack(side=LEFT, fill=BOTH, expand=1)
second_frame = Frame(my_canvas, width = 900, height = 800,highlightthickness=2,background='#D9D9D9')
second_frame.config(highlightbackground="gray", highlightcolor="gray")
# scrollbar
my_scrollbar = tk.Scrollbar(main_frame, orient=VERTICAL, command=my_canvas.yview,background='#D9D9D9')
my_scrollbar.pack(side=RIGHT, fill=Y)

# configuring the canvas
my_canvas.configure(yscrollcommand=my_scrollbar.set)
my_canvas.bind(
    '<Configure>', lambda e: my_canvas.configure(scrollregion=my_canvas.bbox("all"))
)

try:
    instance_df = pd.read_csv(f"{PATH}/scripts/instances.csv")
except:
    instance_df = pd.DataFrame(columns=['id','path','criteria_1','criteria_2','criteria_3'])
    instance_df.to_csv(f"{PATH}/scripts/instances.csv",index=False)

#############################################################################
#############################################################################
##########################SCROLL FRAME CREATED###############################
#############################################################################
#############################################################################
criterias ={
    #what category
    'criteria_1':{
        #user can select multiple categories
        'options':'',
        'status':'enabled'
    },
    #is website in english
    'criteria_2': {
        'options': '',
        'status': 'enabled'
    },
    #does it have a foreign domain
    'criteria_3': {
        'options': '',
        'status': 'enabled'
    },
    "path":''
}

row_counter = 2
buttons = []

def refresh_status(label_):
    label_.config(text=read_status())

def confirm_gSpread_url(input_gspread):
    try:
        read_g_sheet(input_gspread.get())
        messagebox.showinfo('Success','Reeded Spreadsheet Successfully')
        criterias['path'] = input_gspread
        return
    except:
        messagebox.showerror("Error Reading spreadsheet", "Please make sure you entered right url and that spreadsheet permission have been granted")
        pass


def run(start_button_itself, status_label):
    #C1
    criteria_1_options = criterias['criteria_1']['options'].get()
    print()
    if criteria_1_options == 'None':
        messagebox.showerror('Select', 'Select at least one Category')
        return
    criteria_1_status = criterias['criteria_1']['status'].get()
    if criteria_1_status == 'Enabled':
        criteria_1_options_for_csv = criteria_1_options
        pass
    else:
        criteria_1_options_for_csv = 'Disabled'
    # C2
    criteria_2_options = criterias['criteria_2']['options'].get()
    criteria_2_status = criterias['criteria_2']['status'].get()
    if criteria_2_status == 'Enabled':
        criteria_2_options_for_csv = criteria_2_options
        pass
    else:
        criteria_2_options_for_csv = 'Disabled'
    # C3
    criteria_3_options = criterias['criteria_3']['options'].get()
    criteria_3_status = criterias['criteria_3']['status'].get()
    if criteria_3_status == 'Enabled':
        criteria_3_options_for_csv = criteria_3_options
        pass
    else:
        criteria_3_options_for_csv = 'Disabled'
    #PATH
    try:
        path = criterias['path'].get()
    except:
        messagebox.showerror("Empty Input", "Please make sure to enter spreadsheet URL")
        return
    if path == '':
        messagebox.showerror("Empty Input", "Please make sure to enter spreadsheet URL")
        return
    ###
    print(f"Criteria 1:{criteria_1_status} -- {criteria_1_options}")
    print(f"Criteria 2:{criteria_2_status} -- {criteria_2_options}")
    print(f"Criteria 3:{criteria_3_status} -- {criteria_3_options}")
    print('PATH',path)
    id_of_this_instance = random.randint(0,9999999)
    instance = {
        'id':[id_of_this_instance],
        'path':[path],
        'criteria_1':[criteria_1_options_for_csv],
        'criteria_2':[criteria_2_options_for_csv],
        'criteria_3':[criteria_3_options_for_csv],
    }
    instances_df = pd.read_csv(f"{PATH}/scripts/instances.csv")
    pd.concat([pd.DataFrame.from_dict(instance),instances_df]).to_csv(f"{PATH}/scripts/instances.csv",index=False)
    process = subprocess.Popen(f'python "{PATH}/scripts/initiatior_v2.py" {id_of_this_instance}')
    start_button_itself.config(text = '        Sarted        ')
    start_button_itself.config(state="disabled")


def get_categories(btn_categories):
    process = subprocess.Popen(f'python "{PATH}/scripts/select_categories/select_categories.py"',stdout=subprocess.PIPE)
    while True:
        if process.poll() == None:
            try:
                for el in list(process.stdout.readlines()):
                    if 'c@ategor!ies:' in str(el):
                        try:
                            criterias['criteria_1']['options'].set(str(el).replace('c@ategor!ies:','').split(':')[-1].replace("'",'')[1:-4])
                            print(criterias['criteria_1']['options'].get())
                        except:
                            btn_categories.config(state="disabled")
                            return None
            except :
                pass
        else:
            btn_categories.config(state="disabled")
            return None
        time.sleep(0.3)
#############################################################################
#############################################################################

#############################################################################
#############################################################################


#############################################################################
############################################################################
###########################################################################
def criteria_website_category(frame_):
    #criteria 1
    global row_counter
    criteria_name = "Select Website Category"

    instance_frame = tk.Canvas(frame_,highlightthickness=2,width=900,height=100,background='#EAEAEA')
    instance_frame.config(highlightbackground = "gray", highlightcolor= "gray")
    #Critera
    criteria_frame = tk.Frame(instance_frame,background='#EAEAEA')
    criteria_label = tk.Label(criteria_frame,text="Criteria",background='#EAEAEA')
    criteria_label.pack(side=TOP, fill=BOTH, expand=0,padx=10,pady=5)
    criteria_name_FRAME = tk.Frame(criteria_frame,highlightthickness=2,background='#FFFFFF')
    criteria_name_FRAME.config(highlightbackground = "gray", highlightcolor= "gray")
    criteria_label_name = tk.Label(criteria_name_FRAME,text=f"           {criteria_name}           ",bg='#FFFFFF')
    criteria_label_name.pack(side=TOP, expand=0,padx=10,pady=10)
    criteria_name_FRAME.pack(side=TOP, fill=BOTH, expand=0)
    criteria_frame.place(relx=.05,rely=.1)


    #options
    options_frame = tk.Frame(instance_frame,background='#EAEAEA')
    option_label = tk.Label(options_frame,text='Desired option',background='#EAEAEA')
    option_label.pack(side=TOP, fill=BOTH, expand=0,padx=10,pady=5)
    options__button_FRAME =  tk.Frame(options_frame,highlightthickness=2,background='#FCFCFC')
    options__button_FRAME.config(highlightbackground = "gray", highlightcolor= "gray")
    var_options = StringVar(options__button_FRAME)
    var_options.set("None")
    select_options_button = tk.Button(options__button_FRAME,text='Select Categories',background='#FCFCFC',command= lambda :get_categories(select_options_button))
    select_options_button.pack(side=TOP, fill=BOTH, expand=1,padx=10,pady=10)
    options__button_FRAME.pack(side=TOP, fill=BOTH, expand=0)

    options_frame.place(relx=.45,rely=.1)


    #status
    status_frame = tk.Frame(instance_frame,background='#EAEAEA')
    #
    status_label = tk.Label(status_frame,text='Status',background='#EAEAEA')
    status_label.pack(side=TOP, fill=BOTH, expand=1,padx=10,pady=5)
    #
    status_data_label_FRAME = tk.Frame(status_frame,highlightthickness=2,background='#FCFCFC')
    status_data_label_FRAME.config(highlightbackground = "gray", highlightcolor= "gray")
    var_status = StringVar(status_frame)
    var_status.set("Enabled")  # initial valu
    option_status_e = OptionMenu(status_data_label_FRAME,var_status,'Enabled','Disabled')
    option_status_e.config(background='#FCFCFC')
    option_status_e.pack(side=TOP, fill=BOTH, expand=1,padx=30,pady=5.1)
    status_data_label_FRAME.pack(side=TOP, fill=BOTH, expand=0)
    # status_frame.grid(row=0,column = 3, padx= 10, pady= 5)
    status_frame.place(relx=.75,rely=.1)


    data_criteria = {
        'options':var_options,
        'status':var_status
    }
    criterias['criteria_1'].update(data_criteria)
    instance_frame.pack(side=TOP, fill=BOTH, expand=1,padx=10,pady=10)
#######################################################################################################################
def criteria_is_english(frame_):
    #criteria 2
    global row_counter
    criteria_name = 'Is Website English?'

    instance_frame = tk.Canvas(frame_,highlightthickness=2,width=900,height=100,background='#EAEAEA')
    instance_frame.config(highlightbackground = "gray", highlightcolor= "gray")
    #Critera
    criteria_frame = tk.Frame(instance_frame,background='#EAEAEA')
    criteria_label = tk.Label(criteria_frame,text="Criteria",background='#EAEAEA')
    criteria_label.pack(side=TOP, fill=BOTH, expand=0,padx=10,pady=5)
    criteria_name_FRAME = tk.Frame(criteria_frame,highlightthickness=2,background='#FFFFFF')
    criteria_name_FRAME.config(highlightbackground = "gray", highlightcolor= "gray")
    criteria_label_name = tk.Label(criteria_name_FRAME,text=f"               {criteria_name}               ",bg='#FFFFFF')
    criteria_label_name.pack(side=TOP, expand=0,padx=10,pady=10)
    criteria_name_FRAME.pack(side=TOP, fill=BOTH, expand=0)
    criteria_frame.place(relx=.05,rely=.1)
    #options
    options_frame = tk.Frame(instance_frame,background='#EAEAEA')
    option_label = tk.Label(options_frame,text='Desired option',background='#EAEAEA')
    option_label.pack(side=TOP, fill=BOTH, expand=0,padx=10,pady=5)
    options__button_FRAME =  tk.Frame(options_frame,highlightthickness=2,background='#FCFCFC')
    options__button_FRAME.config(highlightbackground = "gray", highlightcolor= "gray")
    var_options = StringVar(options_frame)
    var_options.set("Yes")  # initial valu
    option_status = OptionMenu(options__button_FRAME,var_options,'Yes','No')
    option_status.config(background='#FCFCFC')
    option_status.pack(side=TOP, fill=BOTH, expand=1,padx=30,pady=5.1)
    options__button_FRAME.pack(side=TOP, fill=BOTH, expand=0)

    options_frame.place(relx=.45,rely=.1)


    #status
    status_frame = tk.Frame(instance_frame,background='#EAEAEA')
    #
    status_label = tk.Label(status_frame,text='Status',background='#EAEAEA')
    status_label.pack(side=TOP, fill=BOTH, expand=1,padx=10,pady=5)
    #
    status_data_label_FRAME = tk.Frame(status_frame,highlightthickness=2,background='#FCFCFC')
    status_data_label_FRAME.config(highlightbackground = "gray", highlightcolor= "gray")
    var_status = StringVar(status_frame)
    var_status.set("Enabled")  # initial valu
    option_status_e = OptionMenu(status_data_label_FRAME,var_status,'Enabled','Disabled')
    option_status_e.config(background='#FCFCFC')
    option_status_e.pack(side=TOP, fill=BOTH, expand=1,padx=30,pady=5.1)
    status_data_label_FRAME.pack(side=TOP, fill=BOTH, expand=0)
    # status_frame.grid(row=0,column = 3, padx= 10, pady= 5)
    status_frame.place(relx=.75,rely=.1)


    data_criteria = {
        'options':var_options,
        'status':var_status
    }
    criterias['criteria_2'].update(data_criteria)
    instance_frame.pack(side=TOP, fill=BOTH, expand=1,padx=10,pady=10)

################################################################################
def criteria_foreign_domain(frame_):
    # criteria 3
    global row_counter
    criteria_name = 'Does it have Foreign Domain?'

    instance_frame = tk.Canvas(frame_,highlightthickness=2,width=900,height=100,background='#EAEAEA')
    instance_frame.config(highlightbackground = "gray", highlightcolor= "gray")
    #Critera
    criteria_frame = tk.Frame(instance_frame,background='#EAEAEA')
    criteria_label = tk.Label(criteria_frame,text="Criteria",background='#EAEAEA')
    criteria_label.pack(side=TOP, fill=BOTH, expand=0,padx=10,pady=5)
    criteria_name_FRAME = tk.Frame(criteria_frame,highlightthickness=2,background='#FFFFFF')
    criteria_name_FRAME.config(highlightbackground = "gray", highlightcolor= "gray")
    criteria_label_name = tk.Label(criteria_name_FRAME,text=f"     {criteria_name}     ",bg='#FFFFFF')
    criteria_label_name.pack(side=TOP, expand=0,padx=10,pady=10)
    criteria_name_FRAME.pack(side=TOP, fill=BOTH, expand=0)
    criteria_frame.place(relx=.05,rely=.1)


    #options
    options_frame = tk.Frame(instance_frame,background='#EAEAEA')
    option_label = tk.Label(options_frame,text='Desired option',background='#EAEAEA')
    option_label.pack(side=TOP, fill=BOTH, expand=0,padx=10,pady=5)
    options__button_FRAME =  tk.Frame(options_frame,highlightthickness=2,background='#FCFCFC')
    options__button_FRAME.config(highlightbackground = "gray", highlightcolor= "gray")
    var_options = StringVar(options_frame)
    var_options.set("No")  # initial valu
    option_status = OptionMenu(options__button_FRAME,var_options,'Yes','No')
    option_status.config(background='#FCFCFC')
    option_status.pack(side=TOP, fill=BOTH, expand=1,padx=30,pady=5.1)
    options__button_FRAME.pack(side=TOP, fill=BOTH, expand=0)

    options_frame.place(relx=.45,rely=.1)


    #status
    status_frame = tk.Frame(instance_frame,background='#EAEAEA')
    #
    status_label = tk.Label(status_frame,text='Status',background='#EAEAEA')
    status_label.pack(side=TOP, fill=BOTH, expand=1,padx=10,pady=5)
    #
    status_data_label_FRAME = tk.Frame(status_frame,highlightthickness=2,background='#FCFCFC')
    status_data_label_FRAME.config(highlightbackground = "gray", highlightcolor= "gray")
    var_status = StringVar(status_frame)
    var_status.set("Enabled")  # initial valu
    option_status_e = OptionMenu(status_data_label_FRAME,var_status,'Enabled','Disabled')
    option_status_e.config(background='#FCFCFC')
    option_status_e.pack(side=TOP, fill=BOTH, expand=1,padx=30,pady=5.1)
    status_data_label_FRAME.pack(side=TOP, fill=BOTH, expand=0)
    # status_frame.grid(row=0,column = 3, padx= 10, pady= 5)
    status_frame.place(relx=.75,rely=.1)


    data_criteria = {
        'options':var_options,
        'status':var_status
    }
    criterias['criteria_3'].update(data_criteria)
    instance_frame.pack(side=TOP, fill=BOTH, expand=1,padx=10,pady=10)


def add_filter(frame_,name):
    global row_counter
    instance_frame = tk.Canvas(frame_,highlightthickness=2,width=900,height=100)
    instance_frame.config(highlightbackground = "gray", highlightcolor= "gray")
    #Critera
    criteria_frame = tk.Frame(instance_frame)
    criteria_label = tk.Label(criteria_frame,text="Criteria")
    criteria_label.pack(side=TOP, fill=BOTH, expand=1,padx=10,pady=10)
    criteria_label_name = tk.Label(criteria_frame,text=name)
    criteria_label_name.pack(side=TOP, fill=BOTH, expand=1,padx=10,pady=10)
    criteria_frame.grid(row=0,column = 1, padx= 10, pady= 5)

    #options
    options_frame = tk.Frame(instance_frame)
    option_label = tk.Label(options_frame,text='Desired option')
    option_label.pack(side=TOP, fill=BOTH, expand=1,padx=10,pady=10)
    option_label_name = tk.Label(options_frame,text='some option')
    option_label_name.pack(side=TOP, fill=BOTH, expand=1,padx=10,pady=10)
    options_frame.grid(row=0,column = 2, padx= 10, pady= 5)


    #status
    status_frame = tk.Frame(instance_frame)
    #
    status_label = tk.Label(status_frame,text='Status')
    status_label.pack(side=TOP, fill=BOTH, expand=1,padx=10,pady=10)
    #
    var_status = StringVar(status_frame)
    var_status.set("Disabled")  # initial valu
    option_status = OptionMenu(status_frame,var_status,'Enabled','Disabled')
    # status_label_name = tk.Label(status_frame,text='Yes')
    option_status.pack(side=TOP, fill=BOTH, expand=1,padx=10,pady=10)
    status_frame.grid(row=0,column = 3, padx= 10, pady= 5)

    instance_frame.pack(side=TOP, fill=BOTH, expand=1,padx=10,pady=10)

##############################################################
#############################SELECT FILE#########################
##############################################################
mapper_label_select_file_path = tk.Label(second_frame, text='Select File Path',background='#D9D9D9')
mapper_label_select_file_path.pack(side=TOP, expand=0)
#frame
select_path_frame = tk.Frame(second_frame,highlightthickness=2,padx=40,pady=20,background='#D9D9D9')
select_path_frame.config(highlightbackground="gray", highlightcolor="gray")
#labels
select_path_frame_labels = tk.Label(select_path_frame,background='#D9D9D9')
browsed_path_mapper = tk.Label(select_path_frame_labels, text='Worksheet URL', font=('Calibri', 13),background='#D9D9D9')
browsed_path_mapper.pack(side=TOP,fill=BOTH, expand=1,padx=10)
input_file_entry = tk.Entry(select_path_frame_labels,width=80)
select_path_frame_labels.pack(side=LEFT, expand=0,padx=10)
input_file_entry.pack(side=TOP,fill=BOTH, expand=0,padx=10,pady=10)
#buton
browse_file_button = tk.Button(select_path_frame, text='         Confirm         ', bg='#C4CFD4', fg='#000000', command=lambda: confirm_gSpread_url(input_file_entry))
browse_file_button.pack(side=LEFT, expand=0,padx=50)
# browse_file_button.place(relx=.8,rely=.01)
select_path_frame.pack(side=TOP, fill=BOTH,expand=1,padx=10,pady=1)
mapper_label_filters = tk.Label(second_frame,text='Filters',background='#D9D9D9')
mapper_label_filters.pack(side=TOP,fill=BOTH, expand=0,padx=10)
##############################################################
#############################Filter Frame#########################
##############################################################
filters_frame = tk.Frame(second_frame,background='#D9D9D9',highlightthickness=2)
filters_frame.config(highlightbackground="gray", highlightcolor="gray")
filters_frame.pack(side=TOP, fill=BOTH, expand=1,padx=10,pady=1)
criteria_website_category(filters_frame)
criteria_is_english(filters_frame)
criteria_foreign_domain(filters_frame)
#start
start_button_frame = tk.Frame(second_frame,background='#D9D9D9')
status_frame = tk.Frame(start_button_frame,background='#D9D9D9')
status_data_label_FRAME = tk.Frame(status_frame,background='#D9D9D9',highlightthickness=2)
status_data_label = tk.Label(status_data_label_FRAME,text='Ready',background='#D9D9D9')
status_data_label.config(width=60)
start_button = tk.Button(start_button_frame,text='        Start        ',bg='#C4CFD4',fg='#000000',command= lambda :run(start_button,status_data_label))
start_button.pack(side=LEFT, expand=0,padx=30,pady=10)
start_data_mapper = tk.Label(status_frame,text='Status',background='#D9D9D9',font={'bold',15})
start_data_mapper.pack(side=TOP, expand=1,padx=10)

status_data_label_FRAME.config(highlightbackground="gray", highlightcolor="gray")
status_data_label.pack(side=TOP, expand=0,padx=10,pady=5)
status_data_label_FRAME.pack(side=TOP, expand=0,padx=50,pady=5)
status_frame.pack(side=LEFT, fill=BOTH, expand=1,padx=10,pady=10)
refresh_status_button = tk.Button(status_frame,text='Refresh Status',bg='#C4CFD4',fg='#000000',command=lambda :refresh_status(status_data_label))
refresh_status_button.pack(side=LEFT, fill=BOTH,expand=1,padx=10,pady=10)
start_button_frame.pack(side=TOP, expand=0,padx=10)
my_canvas.pack(side=TOP, fill=BOTH, expand=1,padx=10,pady=10)

my_canvas.create_window((0, 0), window=second_frame, anchor="nw")
win.mainloop()

