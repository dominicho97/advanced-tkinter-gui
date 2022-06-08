import matplotlib
matplotlib.use("TkAgg")

from base64 import decode
from tkinter import *
import tkinter as tk
import socket
from tkinter import *
import sqlite3
from pathlib import Path

from tkinter.ttk import Treeview
from tkinter import messagebox
from turtle import color
from matplotlib.colors import cnames
from matplotlib.pyplot import show
from matplotlib import pyplot as plt
import mysql.connector
import logging
import socket
import sys
import pickle
from tkinter import ttk
import pandas as pd
import threading
import time

import os

import numpy as np
import re




logging.basicConfig(level=logging.INFO)

logging.info("Making connection with server...")

# create a socket object
socket_to_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# get local machine name
host = socket.gethostname()
port = 9999


# connection to hostname on the port.
socket_to_server.connect((host, port))

# Receive message from server-side
msg = socket_to_server.recv(1024)
logging.info(msg.decode("utf-8"))


# connect with mysql db
mydb = mysql.connector.connect(
    host='localhost', user="root", passwd="root", database="thuisopdracht", auth_plugin="mysql_native_password")

cursor = mydb.cursor()


# * GUI CLIENT



#NEW GUI AFTER LOGIN GUI
def create_new_window():

    # send client logout message to server-side
    def logout_client_to_server():
        client_logout_message = f"Client logged out"
        io_stream_server = socket_to_server.makefile(mode='rw')
        io_stream_server.write(f"{client_logout_message}\n")
        io_stream_server.flush()
        logging.info("Send client logout to server-side")
        
    

    #Log out as client
    def log_out_client():
        messagebox.askyesno("Log out", "Log out as client?")

        #delete most recent Id in DB
        query = "DELETE FROM thuisopdracht.clients ORDER BY id desc limit 1"
        cursor.execute(query)
        mydb.commit()
        
        print("Logged out as client!")
        messagebox.showinfo('Log out', "Logged out!")

    # client to server message logout
        logout_client_to_server()
        new_window.destroy()


    def get_calories_data_thread():
        get_calories_data_thread = threading.Thread(target=get_calories_data)
        get_calories_data_thread.start()
        time.sleep(1)
  

        #Get pickle data from txt files
    def get_calories_data():
        txt_data_file = open(r'C:\Users\domin\OneDrive\Bureaublad\MCT2\semester2\Advanced_programming_maths\2022-labooplossingen-HoDominic\project-2022-HoDominic\cereals_data.txt', 'rb')
        txt_data = pickle.load(txt_data_file)

        #get dataframe (pickled)data from client
        #protein data
        calories_column = txt_data['calories']
        calories_column = sorted(txt_data['calories'])
        #brands data
        brands_column = txt_data['name']
        brands_column = sorted(txt_data['name'])
       
        txt_data_file.close()


        #*CHART CALORIES BY CEREAL BRAND
        #chart size
        chart_figure = plt.figure(figsize=(30,30))
        
        #label font size
        plt.rcParams.update({'font.size': 6})
        
        #configure x and y for chart
        chart_x =  calories_column
        chart_y =  brands_column

        #sort list by value!
        sorted_chartx = sorted(chart_x,key=int)
        sorted_charty = sorted(chart_y,key=str)
        logging.info(sorted_chartx)
        logging.info(sorted_charty)

        #?Set x-axis
        #plt.xticks([0, 10,20,30,40,50,60,70,80,90,100,110,120,130,140,150,160])

        bar_width = [0.4]
        plt.barh(sorted_charty,sorted_chartx,height=bar_width )

        font1 = {'family':'serif','color':'blue','size':14}
        font1_title = {'family':'serif','color':'blue','size':20}

        plt.xlabel('calories',fontdict = font1)
        plt.ylabel('brand',fontdict = font1)
        plt.title('calories by brand (per serving)',fontdict = font1_title)

        plt.show()

       
        

    
    def get_rating_data():
        txt_data_file = open(r'C:\Users\domin\OneDrive\Bureaublad\MCT2\semester2\Advanced_programming_maths\2022-labooplossingen-HoDominic\project-2022-HoDominic\cereals_data.txt', 'rb')
        txt_data = pickle.load(txt_data_file)

        #get dataframe (pickled)data from client
        #protein data
        calories_column = txt_data['rating']
        calories_column = sorted(txt_data['rating'])
        #brands data
        brands_column = txt_data['name']
        brands_column = sorted(txt_data['name'])
       
        txt_data_file.close()


        #*CHART CALORIES BY CEREAL BRAND
        #chart size
        chart_figure = plt.figure(figsize=(30,30))
        
        #label font size
        plt.rcParams.update({'font.size': 6})
        
        #configure x and y for chart
        chart_x =  calories_column
        chart_y =  brands_column

        

        #sort list by value!
        sorted_chartx = sorted(chart_x,key=float)
        sorted_charty = sorted(chart_y,key=str)
        logging.info(sorted_chartx)
        logging.info(sorted_charty)

        #?Set x-axis
        plt.xticks([0,10,20,30,40,50,60,70,80,90,100])
        plt.xlim([0, 100])

        bar_width = [0.4]
        plt.barh(chart_y,chart_x,height=bar_width )

        font1 = {'family':'serif','color':'blue','size':14}
        font1_title = {'family':'serif','color':'blue','size':20}

        plt.xlabel('Rating',fontdict = font1)
        plt.ylabel('Brand',fontdict = font1)
        plt.title('Rating by brand',fontdict = font1_title)

        plt.show()


    def get_rating_data_thread():
        get_rating_data_thread = threading.Thread(target=get_rating_data)
        get_rating_data_thread.start() 



    def get_sodium_data():
        txt_data_file = open(r'C:\Users\domin\OneDrive\Bureaublad\MCT2\semester2\Advanced_programming_maths\2022-labooplossingen-HoDominic\project-2022-HoDominic\cereals_data.txt', 'rb')
        txt_data = pickle.load(txt_data_file)

        #get dataframe (pickled)data from client
        #sodium data
        sodium_column = txt_data['sodium']
        sodium_column = sorted(txt_data['sodium'])
        #brands data
        brands_column = txt_data['name']
        brands_column = sorted(txt_data['name'])
       
        txt_data_file.close()


        #*CHART CALORIES BY CEREAL BRAND
        #chart size
        chart_figure = plt.figure(figsize=(30,30))
        
        #label font size
        plt.rcParams.update({'font.size': 6})
        
        #configure x and y for chart
        chart_x =  sodium_column
        chart_y =  brands_column

        

        #sort list by value!
        sorted_chartx = sorted(chart_x,key=float)
        sorted_charty = sorted(chart_y,key=str)
        logging.info(sorted_chartx)
        logging.info(sorted_charty)

        bar_width = [0.4]
        plt.barh(sorted_charty,sorted_chartx,height=bar_width )

        font1 = {'family':'serif','color':'blue','size':14}
        font1_title = {'family':'serif','color':'blue','size':20}

        plt.xlabel('Sodium',fontdict = font1)
        plt.ylabel('Brand',fontdict = font1)
        plt.title('Sodium by brand',fontdict = font1_title)

        plt.show()


    def get_sodium_data_thread():
        get_sodium_data_thread = threading.Thread(target=get_sodium_data)
        get_sodium_data_thread.start() 


    def get_calories_with_params():
        
        global input_param

        #get client entry value as int
        input_param =  int(entry_client.get())
        print(input_param)
            

       
         

        txt_data_file = open(r'C:\Users\domin\OneDrive\Bureaublad\MCT2\semester2\Advanced_programming_maths\2022-labooplossingen-HoDominic\project-2022-HoDominic\cereals_data.txt', 'rb')
        txt_data = pickle.load(txt_data_file)

        #get dataframe (pickled)data from client
        #calories data
        calories_column = txt_data['calories']
        calories_column = sorted(txt_data['calories'])
        print(calories_column)
   
         #bins data
        bins_column=  bins = [0,10,20,30,40,50,60,70,80,90,100,110,120,130,140,150,160]
        bins_column = sorted(bins)

        #print(calories_column)
        #turn list of str in list of int
        calories_column_int = [int(values) for values in calories_column]
       

        #condition calories list with input parameter
        calories_column_with_param = [i for i in calories_column_int if i >= input_param]
        
            
        #sort
        sorted_calories_column_with_param = sorted(calories_column_with_param)
        print(sorted_calories_column_with_param)

            

        #*CHART CALORIES BY CEREAL BRAND WITH PARAMETER
         #chart size
     
        plt.figure(figsize=(30,30))
            
        #label font size
        plt.rcParams.update({'font.size': 6})
            
        #configure x and y for chart
        chart_x =  sorted_calories_column_with_param
        chart_y =  bins_column

        print(chart_x)
        print(chart_y)



        plt.hist(chart_x,chart_y)
       
      

        font1 = {'family':'serif','color':'blue','size':14}
        font1_title = {'family':'serif','color':'blue','size':20}

        plt.xlabel('Calories',fontdict = font1)
        plt.ylabel('Amount of cereal brands',fontdict = font1)
        plt.title(f'Cereals with minimum {input_param} calories (per serving) ',fontdict = font1_title)

        plt.show()

       
    def get_calories_with_params_thread():

        get_calories_with_params_thread = threading.Thread(target=get_calories_with_params)
        get_calories_with_params_thread.start()   



    def get_ratings_with_params():
        global input_param_rating

        #get client entry value as int
        input_param_rating =  int(entry_client2.get())
        print(input_param_rating)
   
        txt_data_file = open(r'C:\Users\domin\OneDrive\Bureaublad\MCT2\semester2\Advanced_programming_maths\2022-labooplossingen-HoDominic\project-2022-HoDominic\cereals_data.txt', 'rb')
        txt_data = pickle.load(txt_data_file)

        #get dataframe (pickled)data from client
        #calories data
        ratings_column = txt_data['rating']
        ratings_column = sorted(txt_data['rating'])
        print(ratings_column)
    

         #bins data
        bins_column=  bins = [0,10,20,30,40,50,60,70,80,90,100]
        bins_column = sorted(bins)

   
        #turn list of str in list of int
        ratings_column_int = [float(values) for values in ratings_column]
        #print(calories_column_int)

        #condition calories list with input parameter
        ratings_column_with_param = [i for i in ratings_column_int if i >= input_param_rating]
     
            
        #sort
        sorted_ratings_column_with_param = sorted(ratings_column_with_param)
        print(sorted_ratings_column_with_param)

            

        #*CHART CALORIES BY CEREAL BRAND WITH PARAMETER
         #chart size
     
        plt.figure(figsize=(30,30))
            
        #label font size
        plt.rcParams.update({'font.size': 6})
            
        #configure x and y for chart
        chart_x =  sorted_ratings_column_with_param
        chart_y =  bins_column

        print(chart_x)
        print(chart_y)



        plt.hist(chart_x,chart_y)
       
      

        font1 = {'family':'serif','color':'blue','size':14}
        font1_title = {'family':'serif','color':'blue','size':20}

        plt.xlabel('Rating',fontdict = font1)
        plt.ylabel('Amount of cereal brands',fontdict = font1)
        plt.title(f'Cereals with minimum rating of {input_param_rating} ',fontdict = font1_title)

        plt.show()
        
    
    def get_ratings_with_params_thread():
        get_ratings_with_params_thread = threading.Thread(target=get_ratings_with_params)
        get_ratings_with_params_thread.start()   

        
 
       

    def get_sodium_with_params():
        global input_param_sodium

        #get client entry value as int
        input_param_sodium =  int(entry_client3.get())
        print(input_param_sodium)
   
        txt_data_file = open(r'C:\Users\domin\OneDrive\Bureaublad\MCT2\semester2\Advanced_programming_maths\2022-labooplossingen-HoDominic\project-2022-HoDominic\cereals_data.txt', 'rb')
        txt_data = pickle.load(txt_data_file)

        #get dataframe (pickled)data from client
        #sodium data
        sodium_column = txt_data['sodium']
        sodium_column = sorted(txt_data['sodium'])
        print(sodium_column)
     

         #bins data
        bins_column=  bins = [0,10,20,30,40,50,60,70,80,90,100,110,120,130,140,150,160,170,180,190,200,210,220,230,240,250,260,270,280,290,300,310,320,330]
        bins_column = sorted(bins)


        #turn list of str in list of int
        sodium_column_int = [int(values) for values in sodium_column]
      

        #condition calories list with input parameter
        sodium_column_with_param = [i for i in sodium_column_int if i >= input_param_sodium]
        #print(calories_column_with_param)
            
        #sort
        sorted_sodium_column_with_param = sorted(sodium_column_with_param)
        print(sorted_sodium_column_with_param)

        

        #*CHART CALORIES BY CEREAL BRAND WITH PARAMETER
         #chart size
     
        plt.figure(figsize=(30,30))
            
        #label font size
        plt.rcParams.update({'font.size': 6})
            
        #configure x and y for chart
        chart_x =  sorted_sodium_column_with_param
        chart_y =  bins_column

        print(chart_x)
        print(chart_y)



        plt.hist(chart_x,chart_y)
       
      

        font1 = {'family':'serif','color':'blue','size':14}
        font1_title = {'family':'serif','color':'blue','size':20}

        plt.xlabel('Sodium',fontdict = font1)
        plt.ylabel('Amount of cereal brands',fontdict = font1)
        plt.title(f'Cereals with minimum sodium amount of {input_param_sodium} ',fontdict = font1_title)

        plt.show()
        
    def get_sodium_with_params_thread():
        get_sodium_with_params_thread = threading.Thread(target=get_sodium_with_params)
        get_sodium_with_params_thread.start()  

    def read_admin_message_thread():
        read_admin_message_thread = threading.Thread(target=read_admin_message)
        read_admin_message_thread.start()
        

    def read_admin_message():
        with open(r'C:\Users\domin\OneDrive\Bureaublad\MCT2\semester2\Advanced_programming_maths\2022-labooplossingen-HoDominic\project-2022-HoDominic\admin_to_client_message.txt','r') as rf:
            rf_content = rf.read()
            print(rf_content)
            messagebox.showinfo('Message', f"{rf_content}")
            




#* INITIAL LOGIN GUI




    new_window = Tk()

    new_window.title("Client GUI ")
    new_window.geometry("500x500")
    new_window.resizable(False, False)
    
 
     #TABS
    my_tabs = ttk.Notebook(new_window)
    my_tabs.pack(pady=15)

    tab1 = Frame(my_tabs,width=500,height=500)
    tab1.pack(fill='both', expand=1)
    tab2 = Frame(my_tabs,width=500,height=500 )
    tab2.pack(fill='both', expand=1)

    tab3 = Frame(my_tabs,width=500,height=500 )
    tab3.pack(fill='both', expand=1)

    my_tabs.add(tab1, text='Tab1')
    my_tabs.add(tab2, text='Tab2')
    my_tabs.add(tab3, text='Tab3')
    

     # Label frames
    wrapper1 = LabelFrame(tab1, text="Clients List")
    wrapper1.pack(fill="both", expand="yes", padx=20, pady=10)

    wrapper2 = LabelFrame(tab1, text="Get data by brand")
    wrapper2.pack(fill="both", expand="yes", padx=20, pady=10)

    wrapper3 = LabelFrame(tab1, text="Get amount of brands by calories per serving")
    wrapper3.pack(fill="both", expand="yes", padx=20, pady=10)

    wrapper4 = LabelFrame(tab1, text="Get amount of brands by rating")
    wrapper4.pack(fill="both", expand="yes", padx=20, pady=10)

    wrapper5 = LabelFrame(tab1, text="Get amount of brands by sodium")
    wrapper5.pack(fill="both", expand="yes", padx=20, pady=10)

    wrapper6 = LabelFrame(tab2, text="Read admin message")
    wrapper6.pack(fill="both", expand="yes", padx=20, pady=10)

    #log out client button
    btn = Button(wrapper1, text="Log out", command=log_out_client)
    btn.pack(side=tk.LEFT,padx=10 ,pady=0)

    #get calories by chart button
    btn = Button(wrapper2, text="Calories by brand", command=get_calories_data_thread)
    btn.pack(side=tk.LEFT,padx=10 ,pady=0)

    btn = Button(wrapper2, text="Rating by brand", command=get_rating_data_thread)
    btn.pack(side=tk.LEFT,padx=20 ,pady=0)

    btn = Button(wrapper2, text="Sodium by brand", command=get_sodium_data_thread)
    btn.pack(side=tk.LEFT,padx=30 ,pady=0)


    #WRAPPER3
    input_calories = Label(wrapper3, text='input minvalue calories')
    input_calories.pack(side=tk.LEFT, padx=10)
    entry_client = Entry(wrapper3)
    entry_client.pack(side=tk.LEFT, padx=10)

    btn = Button(wrapper3, text="Get data", command=get_calories_with_params_thread)
    btn.pack(side=tk.LEFT,padx=20 ,pady=0)


    #WRAPPER4
    input_rating = Label(wrapper4, text='input minvalue rating')
    input_rating.pack(side=tk.LEFT, padx=10)
    entry_client2 = Entry(wrapper4)
    entry_client2.pack(side=tk.LEFT, padx=10)

    btn = Button(wrapper4, text="Get data", command=get_ratings_with_params_thread)
    btn.pack(side=tk.LEFT,padx=20 ,pady=0)

    #WRAPPER5
    input_rating = Label(wrapper5, text='input minvalue sodium')
    input_rating.pack(side=tk.LEFT, padx=10)
    entry_client3 = Entry(wrapper5)
    entry_client3.pack(side=tk.LEFT, padx=10)

    btn = Button(wrapper5, text="Get data", command=get_sodium_with_params_thread)
    btn.pack(side=tk.LEFT,padx=20 ,pady=0)


    #WRAPPER6
    btn = Button(wrapper6, text="Read admin message", command=read_admin_message_thread)
    btn.pack(side=tk.LEFT,padx=20 ,pady=0)






    win.destroy()
    new_window.mainloop()



def login_client_to_server():

    # Get gebruiken anders kan het de waarde niet lezen
    client_name = entry.get()
    client_nickname = entry2.get()
    client_email = entry3.get()

    # client to server message
    io_stream_server = socket_to_server.makefile(mode='rw')
    io_stream_server.write(f"{client_name}\n")
    io_stream_server.flush()
    io_stream_server.write(f"{client_nickname}\n")
    io_stream_server.flush()
    io_stream_server.write(f"{client_email}\n")
    io_stream_server.flush()
    


def add_client():
    # Id voor DB
    client_id = cursor.lastrowid

    client_name = entry.get()

    client_nickname = entry2.get()
    client_email = entry3.get()

    pattern = '^[a-z0-9]+[\._]?[ a-z0-9]+[@]\w+[. ]\w{2,3}$'
    if re.search(client_email,pattern):
        if client_email != pattern:
            print("invalid email")

    # Name  input error handling
    if client_name == "":
        messagebox.showerror("Name Invalid", "Name input can't be empty")
        messagebox.ERROR("Empty name input error")
    #  Nickname input error handling
    if client_nickname == "":
        messagebox.showerror("Nickname Invalid",
                             "Nickname input can't be empty")
        messagebox.ERROR("Empty nickname input error")
    # Email input error handling
    if client_email == "":
        messagebox.showerror("Email Invalid", "Email input can't be empty")
        messagebox.ERROR("Empty email input error")
    
    

    # Id has to be sent!
    sql = "INSERT INTO clients VALUES(%s,%s,%s,%s)"
    cursor.execute(sql, (client_id, client_name,
                         client_nickname, client_email))

    #must be commited after executing query
    mydb.commit()
    print("Logged in as client!")
    messagebox.showinfo('Login', "Logged in!")
    

    # client to server message login
    login_client_to_server()

    # Open new window after login
    create_new_window()
   




win = Tk()

frm1 = Frame(win)
frm1.pack(side=tk.LEFT, padx=20)


var1 = StringVar()
client_name = StringVar()

var2 = StringVar()
client_nickname = StringVar()

var3 = StringVar()
client_email = StringVar()


# name text
label1 = Label(frm1, textvariable=var1)
var1.set("Client Name:")
label1.grid(row=0, column=1)

# name input field
entry = Entry(frm1, textvariable=client_name)
#client_name.set("Enter Name ")
entry.grid(row=0, column=2)

# nickname text
label2 = Label(frm1, textvariable=var2)
var2.set("Client Nickname:")
label2.grid(row=1, column=1)

# nickname input field
entry2 = Entry(frm1, textvariable=client_nickname)
entry2.grid(row=1, column=2)


# email text
label3 = Label(frm1, textvariable=var3)
var3.set("Client Email:")
label3.grid(row=2, column=1)

# email input field
entry3 = Entry(frm1, textvariable=client_email)
entry3.grid(row=2, column=2, padx=20)


# button
btn = Button(frm1, text="Log in as client", command=add_client)
btn.grid(row=4, column=2)



win.title("Client login form")
win.geometry("350x350")
win.resizable(False, False)
win.mainloop()



# Catch Message server-to-client message 

io_stream_server = socket_to_server.makefile(mode='rw')
text_to_send = io_stream_server.readline().rstrip('\n')
io_stream_server.flush()
print(f"received message from admin: {text_to_send}")




logging.info("Close connection with server...")
socket_to_server.close()
