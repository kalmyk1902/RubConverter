import requests
from lxml import html

class Currencies:
    def __init__(self):
        self.currencies = []
        self.names = []
        self.mn = []

    def getCurrencies(self):
        r = requests.get('https://www.cbr.ru/currency_base/daily/')
        tree = html.fromstring(r.content)
        self.currencies.extend(tree.xpath('//tr/td[5]/text()'))
        self.names.extend(tree.xpath('//tr/td[2]/text()'))
        self.mn.extend(tree.xpath('//tr/td[3]/text()'))
