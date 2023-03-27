"""
КОММЕНТАРИИ К ПРОГРАММЕ ВЫЧИСЛЕНИЯ ВАЛЮТ В РУБЛИ
Данная программа конвертирует какую то валюту
в рубли по курсу ЦБ РФ

"""
#main.py
#импортируем нужные библиотеки
import toml
import tkinter as tk
from tkinter import ttk
from check import Currencies

#функция загрузки языков (см. locale.toml)
def load_locale(lang):
    with open ('localization/locale.toml', 'r', encoding='utf8') as f: #открываем файл
        data = toml.load(f) #загружаем текст для двух языков
    return data[lang] #возвращаем этот текст

#функция задания языка
def set_lang():
    global lan, var #объявляем переменные
    check = var.get() #проверяем галочку из меню выбора языка
    if check == 'english': #если стоит английский язык...
        lan = load_locale('english') #то его и загружаем
    elif check == 'russian': #если стоит русский язык...
        lan = load_locale('russian') #то его и загружаем

    #вставляем текст при изменении языка (см. locales.toml)
    n1.configure(text=lan['maintxt'])
    n2.configure(text=lan['info'])
    n3.configure(text=lan['btn'])

#функция конвертации (код внизу)
def on_click():
    curr = Currencies() #задаем переменную
    curr.getCurrencies() #и берем нужные данные с сайта
    x = None #объявляем переменную х с пустым значением
    try:
        x = int(curr.names.index(in_txt.get())) #пробуем получить индекс валюты
    except (TypeError and ValueError): #если мы ее не находим ее...
        text = lan['currencyerr'] #говорим об этом пользователю
        output.configure(text=text) #выводим на экран сообщение
        return #выходим из функции

    y = curr.currencies[x] #ищем курс валюты
    y = y.replace(',', '.') #меняем запятую на точку (т.к программа будет считать что курс это строка, а не число)
    try:
        if float(in_num.get()) <= 0: #если сумма валюты меньше или равно 0
            raise ValueError #возвращаем ошибку некорректного значения
        
        final = (float(y) / int(curr.mn[x])) * float(in_num.get()) #конвертируем валюту (валюту делим на её множитель, который дан на сайте и умножаем на указанную сумму)
    except ValueError: #если указанная сумма некорректная
        text = lan['amounterr'] #говорим об этом пользователю
        output.configure(text=text) #выводим сообщение на экран
        return #выходим из функции

    text = (f"{lan['success']} {in_num.get()} {in_txt.get()} = {round(final, 3)} {lan['rubles']}") #получаем результат конвертации 
    output.configure(text=text) #и выводим его на экран, после чего фунция завершается

root = tk.Tk() #определяем окно программы

root.title('Ruble converter') #задаем ей имя
root.geometry('600x600') #задаем размер окна
root.iconbitmap('etc/icon.ico') #ставим иконку

#создаем меню выбора языка
menu_file = tk.Menu(root) #определяем основное меню
var = tk.StringVar() #определяем переменную как галочку выбора
var.set('russian') #задаем значение по умолчанию на русский язык
menu = tk.Menu(menu_file, tearoff=0) #определяем окно выбора
menu.add_checkbutton(label='Русский', variable=var, onvalue='russian', command=set_lang) #создаем 1 кнопку выбора (русский язык)
menu.add_checkbutton(label='English', variable=var, onvalue='english', command=set_lang) #создаем 2 кнопку выбора (английский язык)
menu_file.add_cascade(label='Язык/Langauge', menu=menu) #добавляем окно выбора в меню

lan = load_locale('russian') #ставим загрузку русского языка по умолчанию

#создаем интерфейс
n1 = ttk.Label(root, text=lan['maintxt'], font=('Arial Bold', 15, 'bold')) #название программы
n1.place(relx = 0.27, rely = 0.2) #распологаем его
n2 = ttk.Label(root, text=lan['info'], wraplength=500) #инструкция
n2.place(relx = 0.14, rely = 0.35) #распологаем её
in_txt = ttk.Entry(root, width=10) #поле ввода валюты
in_txt.place(relx = 0.2, rely = 0.47) #распологаем его
in_num = ttk.Spinbox(root, from_=0, to=999999, width=10) #поле ввода валюты
in_num.place(relx = 0.6, rely = 0.47) #распологаем его
n3 = ttk.Button(root, text=lan['btn'], command=on_click) #кнопка конвертации
n3.place(relx = 0.38, rely = 0.6) #распологаем её
output = ttk.Label(root, text='', font=('Georgia', 12)) #вывод результата
output.place(relx = 0.27, rely = 0.7) #распологаем его

#запуск программы
root.config(menu=menu_file) #добавляем меню в окно программы
root.mainloop() #запускаем окно программы

#--------------------------------------------------------------

#check.py
#импортируем нужные библиотеки
import requests
from lxml import html

#создаем класс программы
class Currencies:
    #определяем все переменные для класса
    def __init__(self):
        self.currencies = [] #все курсы валют
        self.names = [] #все имена валют
        self.mn = [] #все множители валют

    #парсим сайт
    def getCurrencies(self):
        r = requests.get('https://www.cbr.ru/currency_base/daily/') #заходим на сайт ЦБ РФ
        tree = html.fromstring(r.content) #загружаем всю страницу
        #при помощи XPath выражений...
        self.currencies.extend(tree.xpath('//tr/td[5]/text()')) #берем все курсы
        self.names.extend(tree.xpath('//tr/td[2]/text()')) #берем все имена
        self.mn.extend(tree.xpath('//tr/td[3]/text()')) #берем все множители


"""

© Copyright 2023 Kalmyk1902
Распространяется по лицензии MIT

"""