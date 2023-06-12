import sys
import tkinter.messagebox

from tkinter import *

import os
import tkinter as tk

PATH = os.path.abspath(os.path.dirname(__file__))

win = Tk()
win.geometry("770x940")

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
#############################################################
####################FUNCTIONS AREA##########################
#############################################################
#this is main output  list, so this script will output this list with all categories listed
buttons_selected = []
last_free_space = []

def remove_selected(frame,btn,frame_select_categories):
    #this funtion will be responsible to remove the selected category from the main list, remove the button from selected categories frame, add the button back to select categories frame
    btn_for_selected_categories = tk.Button(frame_select_categories,text=btn.cget('text'),command=lambda : add_to_selected(frame,btn_for_selected_categories,frame_select_categories))
    btn_for_selected_categories.pack(side=TOP, fill=BOTH, expand=1,padx=10,pady=5)
    buttons_selected.remove(btn.cget('text'))
    print(buttons_selected)
    btn.destroy()

    pass
def add_to_selected(frame,btn,frame_selected_categories):
    #this function will remove the button from categories and create new one to selected categories frame also it will append the text of the button to main output list
    btn_in_selected = tk.Button(frame,text=btn.cget('text'),command=lambda :remove_selected(frame,btn_in_selected,frame_selected_categories))
    #here i check each position in grid. Grid has 5 cols and 2 rows.
    #so i will check from the first row and first column for a empty place and then i will place the widget or button in the first free spot.
    if len(buttons_selected) > 9:
        return
    for r_ in range(2):
        for c_ in range(5):
            if len(frame.grid_slaves(r_+1,c_)) == 1:
                continue
            if len(frame.grid_slaves(r_+1,c_)) == 0:
                place_in_grid = {
                    'row': r_+1,
                    'col':c_
                }
                last_free_space.append(place_in_grid)
                btn_in_selected.grid(row=r_+1, column=c_, padx=5, pady=5, sticky=W)
                pass
    buttons_selected.append(btn.cget('text'))
    btn.destroy()
    print(buttons_selected)
    pass
def create_button(frame_,name,selected_categories_frame):
    #this func will create buttons for user to select
    btn = tk.Button(frame_,text=name,command=lambda :add_to_selected(selected_categories_frame,btn,frame_))
    btn.pack(side=TOP, fill=BOTH, expand=1,padx=10,pady=5)

def return_selected():
    if len(buttons_selected) > 0:
        categories = "@@!!@@".join(buttons_selected)
        print(f'c@ategor!ies: {categories}')
        sys.exit()
        pass
    else:
        tkinter.messagebox.showerror('Select','Select at least one Category')
#############################################################
####################SELECTED AREA##########################
#############################################################
select_are_label_MAPPER = tk.Label(second_frame,text='Selected/Click to Remove', font={'bold',15},background='#D9D9D9')
select_are_label_MAPPER.pack(side=TOP, fill=BOTH, expand=1,padx=10,pady=5)
# remove selected frame
selected_area_frame = tk.Frame(second_frame,highlightthickness=2,background='#D9D9D9')
selected_area_frame.config(highlightbackground="gray", highlightcolor="gray",width=520,height=100)
selected_area_frame.pack(side=TOP, fill=BOTH, expand=1,padx=10)
#
remove_selected_label_MAPPER = tk.Label(selected_area_frame,text='Click To Remove',background='#D9D9D9')
# remove_selected_label_MAPPER.pack(side=TOP,padx=10,pady=5)
#CATEGORIES
select_categories_label_MAPPER = tk.Label(second_frame,text='Select Categories', font={'bold',15},background='#D9D9D9')
select_categories_label_MAPPER.pack(side=TOP, fill=BOTH, expand=1,padx=10,pady=5)
# Categories Frame
main_category_frame = tk.Frame(second_frame,highlightthickness=2,background='#D9D9D9')
main_category_frame.config(highlightbackground="gray", highlightcolor="gray",width=520,height=100)
main_category_frame.pack(side=TOP, fill=BOTH, expand=1,padx=10)
#DONE button
done_button = tk.Button(second_frame,text='Done',background='green',command=return_selected)
done_button.pack(side=TOP, expand=0,padx=10,pady=5)
##############################################################
#creting buttons with category names
categories_names = []

def f7(seq):
    seen = set()
    seen_add = seen.add
    return [x for x in seq if not (x in seen or seen_add(x))]

with open(os.path.join(PATH,'categories.txt'), 'r') as f:
    cats = []
    data = f.readlines()
    for c in data:
        cats.append(c.split('/')[1].rstrip().lstrip())
    categories_names = f7(cats)

for category in categories_names:
    create_button(main_category_frame,category,selected_area_frame)


my_canvas.pack(side=TOP, fill=BOTH, expand=1,padx=10,pady=10)
my_canvas.create_window((0, 0), window=second_frame, anchor="nw")
win.mainloop()


