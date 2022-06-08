

from fileinput import filename
from msilib.schema import Class
from ntpath import join
from time import perf_counter, sleep
from tkinter import *
import tkinter as tk
import socket
from tkinter import *
import sqlite3
from tkinter import filedialog
from tkinter.ttk import Treeview
from tkinter import messagebox
from turtle import onclick, update, width
from matplotlib.pyplot import fill, grid, show, text
import mysql.connector
import csv
import os
import threading
import pandas as pd

import logging
import socket
import time
from tkinter import ttk
import sys
import concurrent.futures

from numpy import insert
from pyrsistent import v
import pickle
from admin_clienthandler import ClientHandler




logging.basicConfig(level=logging.INFO)

# create a socket object
logging.info("Creating serversocket...")
serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# get local machine name
host = socket.gethostname()

port = 9999

# bind to the port
serversocket.bind((host, port))

# queue up to 5 requests
serversocket.listen(5)


# connect with mysql db

mydb = mysql.connector.connect(
    host='localhost', user="root", passwd="root", database="thuisopdracht", auth_plugin="mysql_native_password")


cursor = mydb.cursor()



  

# * GUI ADMIN/Server









#GUI ADMIN
def GUI_admin():

    

    # update client list 
    def update(rows):

        # global csv_datas
        # csv_data = rows
        # clear table,get children
        trv.delete(*trv.get_children())
        for i in rows:
            trv.insert('', 'end', values=i)


    def update_client_list_thread():
        update_client_list_thread = threading.Thread(target=update_client_list)
        update_client_list_thread.start()
        


     # update client list button
    def update_client_list():
        query = "SELECT id,name,nickname,email FROM clients"
        cursor.execute(query)
        rows = cursor.fetchall()
        update(rows)
        mydb.commit()
        log_window.insert("end", "Admin refreshed db")

    def search_client():
        q2 = q.get()
        query = "SELECT id, name,nickname,email FROM clients WHERE name LIKE '%"+q2+"%'"
        cursor.execute(query)
        rows = cursor.fetchall()
        update(rows)
        logging.info(rows)
        log_window.insert("end",f"get {q2} data")

    def search_client_thread():
        search_client_thread = threading.Thread(target=search_client)
        search_client_thread.start()

    def search_all_client():
        query = "SELECT id, name,nickname,email FROM clients "
        cursor.execute(query)
        rows = cursor.fetchall()
        update(rows)
        logging.info(rows)
        log_window.insert("end","get all client data")
       

    def search_all_client_thread():
        search_client_thread = threading.Thread(target=search_all_client)
        search_client_thread.start()
        
        
    def clear_clients_thread():
        clear_clients_thread = threading.Thread(target=clear_clients)
        clear_clients_thread.start()
       

    def clear_clients():
        query = "SELECT id, name,nickname,email FROM clients "
        cursor.execute(query)
        rows = cursor.fetchall()
        update(rows)
     
        





    

    #Tkinter ADMIN GUI
    root = Tk()

    

    #Detect tab click events
    def handle_tab_changed(event):
        selection = event.widget.select()
        tab = event.widget.tab(selection, "text")
        #print("text:", tab)
        #Send tab clicks to admin action log
        log_window.insert("end",f"{tab} clicked")


        #TABS
    my_tabs = ttk.Notebook(root)
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
    
    #Bind tab click event
    my_tabs.bind("<<NotebookTabChanged>>", handle_tab_changed)


    
 

        # Label frames
    wrapper1 = LabelFrame(tab1, text="Clients List") #tab1
    wrapper1_5 = LabelFrame(tab1, text="Client data") #tab1
    wrapper2 = LabelFrame(tab1, text="Admin action log window") #tab1

    wrapper3 = LabelFrame(tab2, text="Send message to Clients") #tab2
    wrapper4 = LabelFrame(tab3, text="Cereals") #tab3

    wrapper1.pack( fill="both",expand="yes", padx=20, pady=0)
    wrapper1_5.pack( fill="both",expand="yes", padx=20, pady=0)

    wrapper2.pack(fill="both", expand="yes", padx=20, pady=10)
    wrapper3.pack(fill="both", expand="yes", padx=20, pady=10)
    wrapper4.pack(fill="both", expand="yes", padx=20, pady=0)

    #Admin action log window   

     

    
    log_window = Listbox(wrapper2)
    log_window.pack(pady=20, padx=50)
    log_window.insert("end","Admin action log..")

  

    
    #* DB:thuisopdracht
    #* table:clients
    # id: INT NN UQ AI
    # name :VARCHAR(45)
    # nickname VARCHAR(45)
    # email VARCHAR(45)
    
        
    # Treeview  client list wrapper 1 
    trv = Treeview(wrapper1, columns=(1, 2, 3, 4), show='headings', height='5')
    trv.pack()

       #configure side,x,y for scrollbars
    trv.pack(side=LEFT)
    trv.place(x=0, y=0)

    trv.heading(1, text='Id')
    trv.heading(2, text='Name')
    trv.heading(3, text='Nickname')
    trv.heading(4, text='Email')

    trv.column(0,width=50)
    trv.column(1,width=120,minwidth=100)
    trv.column(2,width=120,minwidth=100)
    trv.column(3,width=120,minwidth=100)
    trv.column(4,width=120,minwidth=100)

         # Horizontal scroll bar treeview cereal
    xscrollbar_trv1 = ttk.Scrollbar(wrapper1, orient="horizontal", command=trv.xview)
    xscrollbar_trv1 .pack(side=BOTTOM,fill="x" , pady=0)

    #
    yscrollbar_trv1  = ttk.Scrollbar(wrapper1, orient="vertical", command=trv.yview)
    yscrollbar_trv1 .pack(side=RIGHT,fill="y" )

    #configure scrollbar
    trv.configure( xscrollcommand=xscrollbar_trv1.set,yscrollcommand =yscrollbar_trv1.set)

    # Retrieve clients in db for treeview
    query = "SELECT id,name,nickname,email FROM clients"
    cursor.execute(query)
    rows = cursor.fetchall()
    update(rows)
    

    # button refresh client list
    btn = Button(wrapper1, text="Refresh client list", command=update_client_list_thread)
    btn.pack(side=tk.BOTTOM,padx=0 ,pady=0)

# WRAPPER 1.5



    q = StringVar()


    #Search clients
    search_client_lbl = Label(wrapper1_5, text='Client name')
    search_client_lbl.pack(side=tk.LEFT, padx=10)
    entry_client = Entry(wrapper1_5, textvariable=q)
    entry_client.pack(side=tk.LEFT, padx=10)

    search_btn = Button(wrapper1_5, text="Search data", command=search_client_thread)
    search_btn.pack(side=tk.LEFT, padx=6)

    search_all_btn = Button(wrapper1_5, text="Search all client data", command=search_all_client_thread)
    search_all_btn.pack(side=tk.LEFT, padx=6)

    #clear clients list from search wrapper
    clear_clients_btn = Button(wrapper1_5,  text="Clear", command=clear_clients_thread)
    clear_clients_btn.pack(side=tk.LEFT, padx=6)

   

       

    root.title("Server admin GUI")
    root.geometry("700x800")
    root.resizable(False,False)


        #----WRAPPER 3, Tab 2  Message/textbox------

    def clear_textbox_thread():
        text_thread = threading.Thread(target=clear_textbox)
        text_thread.start()
        time.sleep(1)
        

        #clear textbox
    def clear_textbox():
            my_text.delete(1.0, END)

    
    def get_textbox_text_thread():
        text_thread = threading.Thread(target=get_textbox_text)
        text_thread.start()

        #Get textbox message
    def get_textbox_text():
            # establish a connection
        
        text_label.config(text=my_text.get(1.0, END))
        text_to_send = my_text.get(1.0,END)
            #send message to client
        io_stream_server = socket_to_client.makefile(mode='rw')
        io_stream_server.write(f"{text_to_send}\n")
        io_stream_server.flush()
        log_window.insert("end", "Admin sent message")
        with open(r'C:\Users\domin\OneDrive\Bureaublad\MCT2\semester2\Advanced_programming_maths\2022-labooplossingen-HoDominic\project-2022-HoDominic\admin_to_client_message.txt', 'w') as admin_message:
            admin_message.write(text_to_send)
            admin_message.flush()
            admin_message.close()
            
       
    

        
    my_text= Text(wrapper3, width=60,height=20 )
    my_text.pack(pady=20)

    button_frame = Frame(wrapper3)
    button_frame.pack()

        #clear button
    clear_button= Button(button_frame, text="Clear screen", command=clear_textbox_thread)
    clear_button.grid(row=0, column=0, pady=20)

        #send/get text button from textbox
    get_text_button= Button(button_frame, text="Send text", command=get_textbox_text_thread)
    get_text_button.grid(row=0, column=1, padx=20,pady=20)

    text_label = Label(wrapper3, text="Message:")
    text_label.pack(pady=20)


    #----WRAPPER 4 , TAB 3 ------





    #* DB:thuisopdracht
    #* table:cereals
    # name :VARCHAR(45) NN
    # mfr VARCHAR(45)
    # type VARCHAR(45)

    csv_data = []
    
    # update client list 
    def update_cereals(rows):

        global csv_data
        csv_data = rows
        # clear table,get children
        trv2.delete(*trv2.get_children())
        for i in rows:
            trv2.insert('', 'end', values=i)


    def export_CSV():
        if len(csv_data) < 1:
            messagebox.showerror("No data", "No data available to export")
            return False

        file_name = filedialog.asksaveasfilename(initialdir=os.getcwd(),title="Save CSV", filetypes= (("CSV File", "*.csv"), ("All Files", "*.*")))
        with open(file_name, mode='w') as my_file:
            exp_writer = csv.writer(my_file, delimiter=',')
            for i in csv_data:
                exp_writer.writerow(i)

        messagebox.showinfo("Data exported", "Your data has been exported to " + os.path.basename(file_name)+ " succesfully")



    def import_CSV():
        csv_data.clear()
        file_name = filedialog.askopenfilename(initialdir=os.getcwd(), title="Open CSV", filetypes= (("CSV File", "*.csv"), ("All Files", "*.*")))
        with open(file_name) as my_file:
            csv_read = csv.reader(my_file, delimiter = ',')
            #skip first row of csv
            next(csv_read)
            for i in csv_read:
                csv_data.append(i)
        update_cereals(csv_data)




    def save_CSV():
        #cereal_name = StringVar

        if messagebox.askyesno("Save data", "Save CSV data to MYSQL Database?"):
            for i in csv_data:
                cereal_name = i[0]
                cereal_mfr = i[1]
                cereal_type = i[2]
                cereal_calories = i[3]
                cereal_protein = i[4]
                cereal_fat = i[5]
                cereal_sodium = i[6]
                cereal_fiber = i[7]
                cereal_carbo = i[8]
                cereal_sugars = i[9]
                cereal_potass = i[10]
                cereal_vitamins = i[11]
                cereal_shelf = i[12]
                cereal_weight = i[13]
                cereal_cups = i[14]
                cereal_rating = i[15]

                query = "INSERT INTO cereals VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                cursor.execute(query,(cereal_name,cereal_mfr,cereal_type,cereal_calories,cereal_protein,cereal_fat,cereal_sodium,cereal_fiber,cereal_carbo,cereal_sugars,cereal_potass,cereal_vitamins,cereal_shelf,cereal_weight,cereal_cups,cereal_rating))
            mydb.commit()
            csv_data.clear()
            messagebox.showinfo("Data saved", "Data saved to MYSQL database")
        else:
            return False

    #read csv data to make a txt-file with pickled data to send to server-side
    def pickle_CSV():
        with open(r'C:\Users\domin\OneDrive\Bureaublad\MCT2\semester2\Advanced_programming_maths\2022-labooplossingen-HoDominic\project-2022-HoDominic\dataset\cereal.csv', "r") as my_file:
            csv_reader = csv.DictReader(my_file, delimiter = ',')
            #skip first row of csv
            next(csv_reader)
            for i in csv_reader:
                csv_data.append(i)
            
            
            #csv_names = pickle.dumps(brands_data)
            csv_protein = pickle.dumps(csv_data)
            print(csv_protein)
         
      
            pickle_protein = pickle.loads(csv_protein)
            print(pickle_protein)


            df_pickleprotein = pd.DataFrame(pickle_protein)
            print(df_pickleprotein)

            #protein txt file
            protein_data_file = open('cereals_data.txt', 'wb')
            pickle.dump(df_pickleprotein,protein_data_file)
            protein_data_file.close()



            logging.info("Send admin protein data to client")
            log_window.insert("end","pickled protein data.")
          
        #close server
    def close_server():
        print('closed server')
        socket_to_client.close()
       
      
      
        

        



   #(name,mfr,type,calories,protein,fat,sodium,fiber,carbo,sugars,potass,vitamins,shelf,weight,cups,rating)

        #List of cereals
    trv2 = Treeview(wrapper4, columns=(1, 2, 3, 4,5,6,7,8,9,10,11,12,13,14,15,16), show='headings', height='10')

    #configure side,x,y for scrollbars
    trv2.pack(side=LEFT)
    trv2.place(x=0, y=0)

    #trv2.heading(1, text='Id') No id in dataset
    trv2.heading(1, text='Name')
    trv2.heading(2, text='Mfr')
    trv2.heading(3, text='Type')
    trv2.heading(4, text='Calories')
    trv2.heading(5, text='Protein')
    trv2.heading(6, text='Fat')
    trv2.heading(7, text='Sodium')
    trv2.heading(8, text='Fiber')
    trv2.heading(9, text='Carbo')
    trv2.heading(10, text='Sugars')
    trv2.heading(11, text='Potass')
    trv2.heading(12, text='Vitamins')
    trv2.heading(13, text='Shelf')
    trv2.heading(14, text='Weight')
    trv2.heading(15, text='Cups')
    trv2.heading(16, text='Rating')

    # configure colums for scrollbar and because the dataset doesn't fit the treeview
    trv2.column(0,width=50)
    trv2.column(1,width=80,minwidth=100)
    trv2.column(2,width=50,minwidth=100)
    trv2.column(3,width=50,minwidth=100)
    trv2.column(4,width=50,minwidth=100)
    trv2.column(5,width=50,minwidth=100)
    trv2.column(6,width=50,minwidth=100)
    trv2.column(7,width=50,minwidth=100)
    trv2.column(8,width=50,minwidth=100)
    trv2.column(9,width=50,minwidth=100)
    trv2.column(10,width=50,minwidth=100)
    trv2.column(11,width=50,minwidth=100)
    trv2.column(12,width=50,minwidth=100)
    trv2.column(13,width=50,minwidth=100)
    trv2.column(14,width=50,minwidth=100)
    trv2.column(15,width=50,minwidth=100)
    trv2.column(16,width=50,minwidth=100)
    #trv2.column(17,width=50,minwidth=100)
    

     # Horizontal scroll bar treeview cereal
    xscrollbar = ttk.Scrollbar(wrapper4, orient="horizontal", command=trv2.xview)
    xscrollbar.pack(side=BOTTOM,fill="x" )

    #
    yscrollbar = ttk.Scrollbar(wrapper4, orient="vertical", command=trv2.yview)
    yscrollbar.pack(side=RIGHT,fill="y" )

    #configure scrollbar
    trv2.configure( xscrollcommand=xscrollbar.set,yscrollcommand=yscrollbar.set)



    
    # Retrieve cereals in db for treeview
    query = "SELECT name,mfr,type,calories,protein,fat,sodium,fiber,carbo,sugars,potass,vitamins,shelf,weight,cups,rating FROM cereals"
    cursor.execute(query)
    rows = cursor.fetchall()
    update_cereals(rows)

    #Button 
    export_button = Button(wrapper4, text="Export CSV", command=export_CSV)
    export_button.pack(side=tk.LEFT, padx=10,pady=10)

    import_button = Button(wrapper4, text="Import CSV", command=import_CSV)
    import_button.pack(side=tk.LEFT, padx=10,pady=10)

    save_button = Button(wrapper4, text="Save CSV data", command=save_CSV)
    save_button.pack(side=tk.LEFT, padx=10,pady=40)

    pickle_button = Button(wrapper4, text="Pickle CSV data", command=pickle_CSV)
    pickle_button.pack(side=tk.LEFT, padx=10,pady=30)

    
    exit_button = Button(wrapper4, text="Exit", command=lambda:threading.Thread(exit(close_server)))
    exit_button.pack(side=tk.LEFT, padx=10,pady=20)


        

    root.mainloop()


    
while True:
    logging.info("waiting for a client...")
    # establish a connection
    

    
    
    socket_to_client, addr = serversocket.accept()
    
    logging.info(f"Got a connection from {addr}")

   


    clh = ClientHandler(socket_to_client)
    clh.start()

    threading.Thread(target=GUI_admin).start()


    
   

    