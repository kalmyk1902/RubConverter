import toml
import tkinter as tk
from tkinter import ttk
from check import Currencies

def load_locale(lang):
    with open ('localization/locale.toml', 'r', encoding='utf8') as f:
        data = toml.load(f)
    return data[lang]


def set_lang():
    global lan, var
    check = var.get()
    if check == 'english':
        lan = load_locale('english')
    elif check == 'russian':
        lan = load_locale('russian')

    n1.configure(text=lan['maintxt'])
    n2.configure(text=lan['info'])
    n3.configure(text=lan['btn'])

def on_click():
    curr = Currencies()
    curr.getCurrencies()
    x = None
    try:
        x = int(curr.names.index(in_txt.get()))
    except (TypeError and ValueError):
        text = lan['currencyerr']
        output.configure(text=text)
        return

    y = curr.currencies[x]
    y = y.replace(',', '.')
    try:
        if float(in_num.get()) <= 0:
            raise ValueError
        
        final = (float(y) / int(curr.mn[x])) * float(in_num.get())
    except ValueError:
        text = lan['amounterr']
        output.configure(text=text)
        return

    text = (f"{lan['success']} {in_num.get()} {in_txt.get()} = {round(final, 3)} {lan['rubles']}")
    output.configure(text=text)

root = tk.Tk()

root.title('Ruble converter')
root.geometry('600x600')
root.iconbitmap('etc/icon.ico')

menu_file = tk.Menu(root)
var = tk.StringVar()
var.set('russian')
menu = tk.Menu(menu_file, tearoff=0)
menu.add_checkbutton(label='Русский', variable=var, onvalue='russian', command=set_lang)
menu.add_checkbutton(label='English', variable=var, onvalue='english', command=set_lang)
menu_file.add_cascade(label='Язык/Langauge', menu=menu)

lan = load_locale('russian')

n1 = ttk.Label(root, text=lan['maintxt'], font=('Arial Bold', 15, 'bold'))
n1.place(relx = 0.27, rely = 0.2)
n2 = ttk.Label(root, text=lan['info'], wraplength=500)
n2.place(relx = 0.14, rely = 0.35)
in_txt = ttk.Entry(root, width=10)
in_txt.place(relx = 0.2, rely = 0.47)
in_num = ttk.Spinbox(root, from_=0, to=999999, width=10)
in_num.place(relx = 0.6, rely = 0.47)
n3 = ttk.Button(root, text=lan['btn'], command=on_click)
n3.place(relx = 0.38, rely = 0.6)
output = ttk.Label(root, text='', font=('Georgia', 12))
output.place(relx = 0.27, rely = 0.7)


root.config(menu=menu_file)
root.mainloop()