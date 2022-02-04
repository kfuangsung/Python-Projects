import os
import json
import requests
import pandas as pd 
from bs4 import BeautifulSoup
from IPython.display import display
from tqdm import tqdm


def get_soup(url):
    web = requests.get(url)
    if not web.ok:
        print(f"ERROR | cannot request url")
        return
    soup = BeautifulSoup(web.text, "lxml")
    
    return soup


def save_dict_to_json(dictionary, filename):
    with open(filename, 'w') as file:
        json.dump(dictionary, file, indent=4)
        
        
def load_json(filename):
    with open(filename, 'r') as file:
        data = json.load(file)
        
    return data


def get_symbols():
    # get all symbols urls
    URL = "https://www.set.or.th/set/commonslookup.do?language=en&country=US"
    soup = get_soup(URL)    
    symbol_urls = {} # (key, value) --> (prefix, url)
    header = soup.find("div", attrs={"class":"col-xs-12 padding-top-10 text-center capital-letter"})
    for head in header.find_all("a"):
        symbol_urls[head.text] = f"https://www.set.or.th/{head.attrs['href']}"
    
    # get all symbols list
    symbols = {} # (key, value) --> (prefix, symbol list)
    for prefix, url in tqdm(symbol_urls.items(), desc="getting symbols"):
        symbols[prefix] = []
        soup = get_soup(url)
        for row in soup.find_all("tr", attrs={"valign":"top"}):
            symbols[prefix].append(row.td.text)
    
    FILENAME = "SET_symbols.json"     
    save_dict_to_json(symbols, FILENAME)
    print(f"Saved to '{FILENAME}'")
    

def get_company_highlights(symbol):
    data = {}
    data["symbol"] = symbol
    if '&' in symbol:
        symbol_url = symbol.replace('&', '%26')
    else:
        symbol_url = symbol
    URL = f"https://www.set.or.th/set/companyhighlight.do?symbol={symbol_url}&ssoPageId=5&language=en&country=US"
    soup = get_soup(URL)
    table = soup.find("table", attrs={"class":"table table-hover table-info"})
    
    # helper functions
    def get_date(table_name):
        if table_name == "FinancialData":
            header = table.find_all("thead")[0]
            # header = header.find_all("th")[1:-1]
        elif table_name == "Statistics":
            header = table.find_all("thead")[1]
            # header = header.find_all("th")[1:]
        date = []
        for  head in header.find_all("th")[1:]:
            text = head.get_text(" ")
            if not text in [" ", "", "\xa0"]:
                date.append(text)
                
        return date
    
    def add_table_dict(table_name):
        date = get_date(table_name)
        data[table_name] = {}
        data[table_name]["date"] = date
        data[table_name]["info"] = {}
    
    def save_info(table_name):
        add_table_dict(table_name)
        
        if table_name == "FinancialData":
            rows = table.tbody.find_all("td")
        elif table_name == "Statistics":
            for i, row in enumerate(table.tbody.find_all("td")):
                if row.text == "Last Price(Baht)": 
                    index = i
                    break
            rows = table.tbody.find_all("td")[index:]
            
        for row in rows:
            if table_name == "FinancialData":
                if row.text == "Last Price(Baht)": break
            attrs = row.attrs
            if attrs.get('style', None) == 'text-align:left;' and not attrs.get('colspan', None) is None:
                pass
            elif attrs.get('style', None) == 'text-align:left;':
                name = row.text 
                data[table_name]["info"][name] = []
            else:
                info = row.get_text(strip=True)
                if info != '':
                    info = info.replace(',','')
                    try:
                        info = float(info)
                    except:
                        pass
                    data[table_name]["info"][name].append(info)
    
    def fill_blank(table_name):
        length = len(data[table_name]['date'])
        for col in data[table_name]['info'].values():
            while len(col) < length:
                col.insert(0, '-')
    
    table_names = ["FinancialData", "Statistics"]
    for table_name in table_names:
        save_info(table_name)
        fill_blank(table_name)

    return data


def show_company_highlights(data):
    symbol = data["symbol"]
    
    table_name = "FinancialData"
    print(f"*** {symbol} | {table_name} ***")
    df = pd.DataFrame(data[table_name]["info"], index=data[table_name]["date"]).T
    display(df)
    print("-"*50)
    table_name = "Statistics"
    print(f"\n*** {symbol} | {table_name} ***")
    df = pd.DataFrame(data[table_name]["info"], index=data[table_name]["date"]).T
    display(df)
    
    
def get_all_company_highlights():
    if not os.path.exists("SET_symbols.json"):
        get_symbols()
    symbols = load_json("SET_symbols.json")
    
    company_highlights = {}
    FILENAME = "SET_companyHighlights.json"

    for prefix, symbols_list in tqdm(symbols.items(), desc="getting company highlights"):
        for symbol in (symbols_list):
            data = get_company_highlights(symbol)
            company_highlights[symbol] = data
        save_dict_to_json(company_highlights, FILENAME)
    print(f"Saved to '{FILENAME}'")