"""
COMMENTARIES FOR RUBLE CONVERSION PROGRAM
This program converts your currency to
rubles throw exchange rate of Russian Central Bank

"""

#main.py
#importing necessary libraries
import toml
import tkinter as tk
from tkinter import ttk
from check import Currencies

#langauges load function (see locale.toml)
def load_locale(lang):
    with open ('localization/locale.toml', 'r', encoding='utf8') as f: #open file
        data = toml.load(f) #load text for two langauges
    return data[lang] #return this text

#change langauge function
def set_lang():
    global lan, var #defining variables
    check = var.get() #checking the check
    if check == 'english': #if check is english...
        lan = load_locale('english') #load it
    elif check == 'russian': #if check is russian...
        lan = load_locale('russian') #load it

    #configuring text after lang change (see locale.toml)
    n1.configure(text=lan['maintxt'])
    n2.configure(text=lan['info'])
    n3.configure(text=lan['btn'])

#conversion function (code at the bottom)
def on_click():
    curr = Currencies() #defining variable
    curr.getCurrencies() #taking all necessary data
    x = None #defining variable x and assigning an empty value
    try:
        x = int(curr.names.index(in_txt.get())) #getting the currency name index
    except (TypeError and ValueError): #if we can't get it...
        text = lan['currencyerr'] #saying this to user
        output.configure(text=text) #outputing the message
        return #leaving the function

    y = curr.currencies[x] #searching the exchange rate
    y = y.replace(',', '.') #replacing comma to dot (because of the comma program thinks that the rate is string, not number)
    try:
        if float(in_num.get()) <= 0: #if amount is or lesser than 0
            raise ValueError #raising the incorrect number error
        
        final = (float(y) / int(curr.mn[x])) * float(in_num.get()) #converting currency (dividing currency to its multiplier provided by site and multiplying by amount)
    except ValueError: #if amount is incorrect
        text = lan['amounterr'] #saying this to user
        output.configure(text=text) #outputing the message
        return #leaving the function

    text = (f"{lan['success']} {in_num.get()} {in_txt.get()} = {round(final, 3)} {lan['rubles']}") #getting the result
    output.configure(text=text) #outputing the result then leaving the function

root = tk.Tk() #defining the program window

root.title('Ruble converter') #naming it
root.geometry('600x600') #setting its size
root.iconbitmap('etc/icon.ico') #setting its icon

#creating langauge change menu
menu_file = tk.Menu(root) #defining the main menu
var = tk.StringVar() #defining the check variable
var.set('russian') #setting the default langauge as russian
menu = tk.Menu(menu_file, tearoff=0) #creating the langauge section
menu.add_checkbutton(label='Русский', variable=var, onvalue='russian', command=set_lang) #adding russian lang check
menu.add_checkbutton(label='English', variable=var, onvalue='english', command=set_lang) #adding english lang check
menu_file.add_cascade(label='Язык/Langauge', menu=menu) #adding section to menu

lan = load_locale('russian') #setting russian langauge as default

#creating the UI
n1 = ttk.Label(root, text=lan['maintxt'], font=('Arial Bold', 15, 'bold')) #title
n1.place(relx = 0.27, rely = 0.2) #placing it
n2 = ttk.Label(root, text=lan['info'], wraplength=500) #instructions
n2.place(relx = 0.14, rely = 0.35) #placing it
in_txt = ttk.Entry(root, width=10) #currency entry field
in_txt.place(relx = 0.2, rely = 0.47) #placing it
in_num = ttk.Spinbox(root, from_=0, to=999999, width=10) #amount entry field
in_num.place(relx = 0.6, rely = 0.47) #placing it
n3 = ttk.Button(root, text=lan['btn'], command=on_click) #convert button
n3.place(relx = 0.38, rely = 0.6) #placing it
output = ttk.Label(root, text='', font=('Georgia', 12)) #result line
output.place(relx = 0.27, rely = 0.7) #placing it

#starting the program
root.config(menu=menu_file) #adding menu to the window
root.mainloop() #opening the window

#--------------------------------------------------------------

#check.py
#importing necessary libraries
import requests
from lxml import html

#defining program class
class Currencies:
    #defining all variables
    def __init__(self):
        self.currencies = [] #all currencies
        self.names = [] #all names
        self.mn = [] #all multipliers

    #parsing the site
    def getCurrencies(self):
        r = requests.get('https://www.cbr.ru/currency_base/daily/') #entering site
        tree = html.fromstring(r.content) #getting whole page
        #using the XPath...
        self.currencies.extend(tree.xpath('//tr/td[5]/text()')) #getting all currencies
        self.names.extend(tree.xpath('//tr/td[2]/text()')) #getting all names
        self.mn.extend(tree.xpath('//tr/td[3]/text()')) #getting all multipliers

"""

© Copyright 2023 Kalmyk1902
Redistributing under MIT license

"""