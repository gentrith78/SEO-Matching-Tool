from pymongo import MongoClient
from tkinter import messagebox
import sys

sys.path.append('..')
import settings
from .check_in_mongo import check_database_m
from .save_to_mongo import save_to_database_m

credentials_database = settings.database_credentials

try:
    user_name = credentials_database['username']
    password = credentials_database['password']
    database_name = credentials_database['database_name']
    main_collection = credentials_database['collection_name']
    cluster = credentials_database['cluster_string']
    client = MongoClient(cluster)
    db = client.relevancy_data_full
    collection = client[database_name][main_collection]
except:
    messagebox.showerror('Error While connecting to Database','Make sure to check the database credentials or payment')



def check_database(url):
    return check_database_m(collection,url)

def save_to_database(url,categories,is_english,is_forgein_domain):
    return save_to_database_m(collection,url,categories,is_english,is_forgein_domain)

