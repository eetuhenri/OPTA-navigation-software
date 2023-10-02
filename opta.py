#Start of the project
# Importing necessary libraries
import mysql.connector
import  customtkinter as CTk
from tkinter import messagebox
from mysql.connector import Error
from tkinter import *
import tkinter as tk
from hashlib import *
import hashlib
import tkintermapview
from geopy.geocoders import Nominatim
import osmnx as ox
import networkx as nx
import math



# Defining a function to connect to MySQL database
def Connect():

    try:
        # Declaring global variables for the connection and cursor
        global connection
        global c
        
        # Connecting to the MySQL server with given credentials
        connection = mysql.connector.connect(
            host='127.0.0.1',
            database='login_db',
            user='root',
            port='3306',
            password='')
        
        # Creating a cursor object for executing queries
        c = connection.cursor()
        
        # Checking if the connection is established successfully
        if connection.is_connected():
            # Retrieving server information and printing it
            db_Info = connection.get_server_info()
            print("Connected to MySQL Server version ", db_Info)
            
            # Executing a test query to get the name of the connected database and printing it
            cursor = connection.cursor()
            cursor.execute("select database();")
            record = cursor.fetchone()
            print("You're connected to database: ", record)

    except Error as e:
        # Catching any exceptions that may occur while connecting to the database and printing the error message
        print("Error while connecting to MySQL", e)
        
        # Closing the cursor and the connection if an error occurs
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed")

root = CTk.CTk()
root.title("Login")
root.geometry("500x400")
CTk.set_appearance_mode("system")
CTk.set_default_color_theme("dark-blue")

start_coord = None
end_coord = None
locator = Nominatim(user_agent = "myapp")


def mainpage():
    main = CTk.CTkToplevel(root)
    main_label = CTk.CTkLabel(main)
    main_label.pack
    main.transient(root)
    main.title("Map")
    main.geometry("900x900")


    def euclidean_dist(u, v):
        #Return the Euclidean distance between two nodes
        x1, y1 = graph.nodes[u]['x'], graph.nodes[u]['y']
        x2, y2 = graph.nodes[v]['x'], graph.nodes[v]['y']
        return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


    def search():
        global start_coord, end_coord
        global start_address
        global end_address
        start_address = map_widget.set_address(start_address_entry.get(), marker=True)
        end_address = map_widget.set_address(end_address_entry.get(), marker=True)
        start_coord = locator.geocode(start_address_entry.get())
        if start_coord is None:
            messagebox.showerror("Error", "Incorrect start address")
            return
        end_coord = locator.geocode(end_address_entry.get())
        if end_coord is None:
            messagebox.showerror("Error", "Incorrect end address")
            return
        place_choice_options = {"Joensuu": "Joensuu, North Karelia, Finland",
                                "Tohmajärvi": "Tohmajärvi, North Karelia, Finland",
                                "Kitee": "Kitee, North Karelia, Finland",
                                "Liperi": "Liperi, North Karelia, Finland",
                                "Heinävesi": "Heinävesi, North Karelia, Finland",
                                "Outokumpu": "Outokumpu, North Karelia, Finland",
                                "Kontiolahti": "Kontiolahti, North Karelia, Finland",
                                "Polvijärvi": "Polvijärivi, North Karelia, Finland",
                                "Juuka": "Juuka, North Karelia, Finland",
                                "Ilomantsi": "Ilomantsi, North Karelia, Finland",
                                "Lieksa": "Lieksa, North Karelia, Finland",
                                "Juuka": "Juuka, North Karelia, Finland",
                                "Nurmes": "Nurmes, North Karelia, Finland",
                                "Valtimo": "Valtimo, North Karelia, Finland"}
        optimizer_choice_options = {"Length": "length",
                                    "Time": "time",
                                    "Bus stop avoidance": "bus_stop_weight"}
        mode_choice_options = {"Drive": "drive",
                            "Bike": "bike",
                            "Walk": "walk",
                            "All": "all",
                            "Drive service": "drive_service"}

        place_choice = combobox_place_select.get()
        place_choice =place_choice_options[place_choice]
        #print("This is place choice in the search function:",place_choice)
        optimizer_choice = combobox_optimizer_select.get()
        optimizer_choice = optimizer_choice_options[optimizer_choice]
        #print("This is opt choice in the search function:",optimizer_choice)
        mode_choice = combobox_mode_select.get()
        mode_choice = mode_choice_options[mode_choice]
        #print("This is mode choice in the search function:",mode_choice)
        route(start_coord, end_coord, mode_choice, optimizer_choice, place_choice)

    def route(start_coord, end_coord, mode_choice, optimizer_choice, place_choice):
        global graph
        global complete_path
        start_coord = locator.geocode(start_coord).point
        end_coord = locator.geocode(end_coord).point
        place = place_choice
        mode = mode_choice # 'drive', 'bike', 'walk', in which you want to move
        optimizer = optimizer_choice #'Length' or 'time', what is the optimizer for the path
        #print(optimizer)
        graph = ox.graph_from_place(place,  network_type=mode) #Calculates the path
        orig_node = ox.distance.nearest_nodes(graph, start_coord[1], start_coord[0])#start point to the map
        dest_node = ox.distance.nearest_nodes(graph, end_coord[1],end_coord[0])#end point to the map
        shortest_route = nx.astar_path(graph, orig_node, dest_node, heuristic=euclidean_dist, weight=optimizer) #searching for the best route

        #print(shortest_route)

        node = shortest_route
        nodes = node
        for node in nodes:
            node_data = graph.nodes[node]
            coord = (node_data["y"], node_data["x"])
            path = []
            marker_path = []
            for i in range(len(shortest_route)):
                    node_data = graph.nodes[shortest_route[i]]
                    coord = (node_data["y"], node_data["x"])
                    marker_path.append(coord)
                    if i == 0:
                        path.append((node_data["y"], node_data["x"]))
                    elif i == len(shortest_route) - 1:
                        path.append((node_data["y"], node_data["x"]))
                    else:
                        path.append(marker_path[-2])

        #print("The complete path",path)
        complete_path = map_widget.set_path(path)
        map_widget.set_zoom(15)


    def clear_map():
        global start_address
        global end_address
        global complete_path
        map_widget.delete(start_address)
        map_widget.delete(end_address)
        map_widget.delete(complete_path)


        graph = None
        path = None
        start_address = None
        end_address = None

    start_address_entry = CTk.CTkEntry(main, font=("Arial", 16), width=300, placeholder_text="Insert start address")
    start_address_entry.grid(row=0,column=0, pady=5, padx=10,sticky="w")

    end_address_entry = CTk.CTkEntry(main, font=("Arial", 16), width=300, placeholder_text="Insert destination address")
    end_address_entry.grid(row=0,column=0, pady=5, padx=315,sticky="w")

    Grid.rowconfigure(main,0,weight=1)
    Grid.columnconfigure(main,0,weight=1)
    
    Grid.rowconfigure(main,2,weight=1)
    #Koko
    map_widget = tkintermapview.TkinterMapView(main, width=900, height=830)
    map_widget.grid(sticky="NSEW")
    #map_widget.set_tile_server("https://mt0.google.com/vt/lyrs=m&hl=en&x={x}&y={y}&z={z}&s=Ga", max_zoom=22) #possibility to use google maps base
    map_widget.set_address("Joensuu") #address
    map_widget.set_zoom(14) #How close

    def add_marker_event(coords):
        print("Add marker:", coords)
        new_marker = map_widget.set_marker(coords[0], coords[1], text="new marker")
        

    map_widget.add_right_click_menu_command(label="Add Marker",
                                            command=add_marker_event,
                                            pass_coords=True)

    my_frame = CTk.CTkFrame(master=main)
    
    optionmenu_place_select = CTk.StringVar()  # set initial value
    optionmenu_place_select.set("Joensuu")
    combobox_place_select = CTk.CTkOptionMenu(main,
                                            values=["Joensuu", "Tohmajärvi", "Kitee",
                                                    "Liperi", "Heinävesi", "Outokumpu",
                                                    "Kontiolahti", "Polvijärvi", "Juuka",
                                                    "Ilomantsi", "Lieksa", "Juuka",
                                                    "Nurmes", "Valtimo"])
    combobox_place_select.grid(row=2, column=0, pady=(5,10), padx=5, sticky="w")

    optionmenu_optimizer_select = CTk.StringVar()  # set initial value
    optionmenu_optimizer_select.set("Time")
    combobox_optimizer_select = CTk.CTkOptionMenu(main,
                                                values=["Length", "Time"])
    combobox_optimizer_select.grid(row=2, column=0, pady=(5,10), padx=150,sticky="w")

    optionmenu_mode_select = CTk.StringVar()  # set initial value
    optionmenu_mode_select.set("All")
    combobox_mode_select = CTk.CTkOptionMenu(main,
                                            values=["Drive", "Bike", "Walk", "All", "Drive service"])
    combobox_mode_select.grid(row=2, column=0, pady=(5,10), padx=300, sticky="w")

    search_button = CTk.CTkButton(main, text="Search", font=("Arial", 16), command=search)
    search_button.grid(row=0, column=0, pady=5, padx=(5,170), sticky="e")

    clear_button = CTk.CTkButton(main, text="Clear route", font=("Arial", 16), command=clear_map)
    clear_button.grid(row=0, column=0, pady=5, padx=(10,30), sticky="e")

    log_in_buttom = CTk.CTkButton(main, text="Log in", font=("Arial", 16), command=clear_button)
    log_in_buttom.grid(row=2, column=0, pady=(5,10), padx=160,sticky="e")

    sign_up_button = CTk.CTkButton(main, text="Sign up", font=("Arial", 16), command=clear_button)
    sign_up_button.grid(row=2, column=0, pady=(5,10), padx=10,sticky="e")

def logged():
    mainpage()

def wrong_credentials():
    
    messagebox.showwarning("False credentials!", "False credentials! Please try again!")
    


def insert_data():
    
    firstname = firstname_entry.get()
    lastname = lastname_entry.get()
    phonenumber = phone_entry.get()
    email = email_entry.get()
    username = username_entry.get()
    password=password_entry.get()
    
    username_hash=hashlib.sha256(username.encode()).hexdigest()
    password_hash=hashlib.sha256(password.encode()).hexdigest()
    var_user.set(username_entry)
    var_psw.set(password_entry)
    

    sql = "INSERT INTO `users`(`firstname`, `lastname`, `phonenumber`, `email`,`username_hash`, `password_hash`) VALUES (%s,%s,%s,%s,%s,%s)"
    vals = (firstname,lastname,phonenumber,email,username_hash, password_hash)
    c.execute(sql,vals)
    connection.commit()


def select():
    username = username_entry.get()
    password=password_entry.get()
    username_hash=hashlib.sha256(username.encode()).hexdigest()
    password_hash=hashlib.sha256(password.encode()).hexdigest()

    sql = "SELECT `username_hash`,`password_hash` FROM `users`WHERE username_hash = %s AND password_hash = %s"
    vals = (username_hash, password_hash)
    c.execute(sql,vals)

    myresults = c.fetchall()

    
    if myresults:
        for i in myresults:
            logged()
    else:
        wrong_credentials()


Connect()

def close_window():
    root.destroy()

def login():
    select()


def insert():
    insert_data()

var_user = StringVar()
var_psw = StringVar()


def register():
    top2 = CTk.CTkToplevel(root)
    top2.title("Registering")
    top2.transient(root)
    top2.geometry("500x800")

    class registering_frame:
        frame = CTk.CTkFrame(master=top2)
        frame.pack(pady=20, padx=60, fill="both", expand=True)

        label = CTk.CTkLabel(master=top2, text="Registering System")
        label.pack(pady=12, padx=10)
        global firstname_entry
        firstname_entry = CTk.CTkEntry(master=top2, placeholder_text="Firstname")
        firstname_entry.pack(pady=12, padx=10)
        global lastname_entry
        lastname_entry = CTk.CTkEntry(master=top2, placeholder_text="Lastname")
        lastname_entry.pack(pady=12, padx=10)
        global phone_entry
        phone_entry = CTk.CTkEntry(master=top2, placeholder_text="Phonenumber")
        phone_entry.pack(pady=12, padx=10)
        global email_entry
        email_entry = CTk.CTkEntry(master=top2, placeholder_text="Email")
        email_entry.pack(pady=12, padx=10)

        global username_entry
        username_entry = CTk.CTkEntry(master=top2,placeholder_text="Username")
        username_entry.pack(pady=12, padx=10)

        global password_entry
        password_entry = CTk.CTkEntry(master=top2,placeholder_text="Password", show="*")
        password_entry.pack(pady=12, padx=10)
        
        button_insert = CTk.CTkButton(master=top2, text="Register", command=insert)
        button_insert.pack(pady=12, padx=10)

        button_cancel = CTk.CTkButton(master=top2, text="Close", command=top2.destroy)
        button_cancel.pack(pady=12, padx=10)



class Login_frame:
    frame = CTk.CTkFrame(master=root)
    frame.pack(pady=20, padx=60, fill="both", expand=True)

    label = CTk.CTkLabel(master=frame, text="Login System")
    label.pack(pady=12, padx=10)
    
    global username_entry
    username_entry = CTk.CTkEntry(master=frame, placeholder_text="Username")
    username_entry.pack(pady=12, padx=10)
    global password_entry
    password_entry = CTk.CTkEntry(master=frame, placeholder_text="Password", show="*")
    password_entry.pack(pady=12, padx=10)
    

    button_login = CTk.CTkButton(master=frame, text="Login", command=login)
    button_login.pack(pady=12, padx=10)

    button_cancel = CTk.CTkButton(master=frame, text="Close", command=close_window)
    button_cancel.pack(pady=12, padx=10)

    button_insert = CTk.CTkButton(master=frame, text="Go register", command=register)
    button_insert.pack(pady=12, padx=10)

    #checkbox = CTk.CTkCheckBox(master=frame, text="Remember Me")
    #checkbox.pack(pady=12, padx=10)
            
#root.iconbitmap("")
root.mainloop()
