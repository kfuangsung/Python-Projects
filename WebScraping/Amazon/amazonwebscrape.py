import time
import random
import json 
import requests
import numpy as np
import matplotlib.pyplot as plt
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from PIL import Image
from bs4 import BeautifulSoup
from tqdm.notebook import tqdm_notebook


def get_soup(url):
    option = webdriver.ChromeOptions()
    option.add_argument('--headless')
    driver = webdriver.Chrome(ChromeDriverManager(log_level=0).install(), options=option)
    driver.get(url)
    time.sleep(10)
    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")
    driver.close()
    
    return soup
    

def get_bestsellerbooks(soup, data_dict):
    if data_dict == {}:
        index = 0
    else:
        index = list(data_dict.keys())[-1] + 1
            
    for item in soup.find_all("div", attrs={"id":"gridItemRoot"}):
        # get title
        title = item.find("div", attrs={"class":"_p13n-zg-list-grid-desktop_truncationStyles_p13n-sc-css-line-clamp-1__1Fn1y"})
        title = title.text
        
        # get images
        img = item.find('img')
        image = img['src']
        
        # item link
        itemLink = item.find("a", attrs={"class":"a-link-normal", "tabindex":"-1", "role":"link"})
        itemLink = "https://www.amazon.com/" + itemLink['href']
        
        # get author
        author = item.find("a", attrs={"class":"a-size-small a-link-child"})
        if author is None: 
            author = item.find('span', attrs={"class":"a-size-small a-color-base"})
        author = author.find("div", attrs={"class":"_p13n-zg-list-grid-desktop_truncationStyles_p13n-sc-css-line-clamp-1__1Fn1y"})
        author = author.text

        # get review stars
        reviewStars = item.find("span", attrs={"class":"a-icon-alt"})
        if not reviewStars is None:
            reviewStars = reviewStars.text

        # get number of reviews
        numberOfReviews = item.find('span', attrs={"class":"a-size-small"})
        if not numberOfReviews is None:
            numberOfReviews = numberOfReviews.text

        # get cover type
        coverType = item.find("span", attrs={"class":"a-size-small a-color-secondary a-text-normal"}).text 

        # get price
        price = item.find("span", attrs={"class":"a-size-base a-color-price"})
        if not price is None:
            price = price.text
            
        data_dict[index] = {}
        data_dict[index]['title'] = title
        data_dict[index]['image'] = image
        data_dict[index]['itemLink'] = itemLink
        data_dict[index]['author'] = author
        data_dict[index]['reviewStars'] = reviewStars
        data_dict[index]['numberOfReviews'] = numberOfReviews
        data_dict[index]['coverType'] = coverType
        data_dict[index]['price'] = price
        
        index += 1  


def get_amazon_search_soup(keyword, page):
    url = f"https://www.amazon.com/s?k={keyword}&page={page}"
    # headers = get_headers()
    # webpage = requests.get(URL, headers=headers)
    # if webpage.ok:
    #     soup = BeautifulSoup(webpage.text, "lxml")
    #     msg = f"KEYWORD:{keyword} | PAGE:{page} | SUCCESS"
    # else:
    #     soup = None
    #     msg = f"KEYWORD:{keyword} | PAGE:{page} | ERROR"
    # print(msg)
    soup = get_soup(url)
    
    return soup
        
        
def get_search_results(soup, data_dict):
    
    # set index of dictionary
    if data_dict == {}:
        index = 0
    else:
        index = list(data_dict.keys())[-1] + 1
        
    search_res = soup.find_all('span', attrs={"data-component-type":"s-search-results"})
    for item in search_res[0].find_all("div", attrs={"class":"a-section"}):

        # get item link
        title = item.find("a", attrs={"class":"a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal"})
        if title is None: continue
        itemLink = "https://www.amazon.com" + title["href"]

        # get item name
        name = title.find("span")#, attrs={"class":"a-size-medium a-color-base a-text-normal"})
        if name is None: continue
        name = name.text

        # get item image 
        image = item.find("span", attrs={"data-component-type":"s-product-image"})
        if image is None: continue
        image = image.find('img', attrs={'class':'s-image'})
        if image is None: continue
        image = image['src']

        # get review stars
        reviewStars = item.find('span', attrs={'class':'a-icon-alt'})
        if not reviewStars is None: 
            reviewStars = reviewStars.text

        # get number of reviews
        numberOfReviews = item.find('span', attrs={'class':'a-size-base'})
        if not numberOfReviews is None: 
            numberOfReviews = numberOfReviews.text

        # fet current prices
        currentPrice = item.find('span', attrs={'class':'a-price'})
        if not currentPrice is None: 
            currentPrice = currentPrice.find('span', attrs={'class':'a-offscreen'})
        if not currentPrice is None: 
            currentPrice = currentPrice.text

        # get old prices
        oldPrice = item.find('span', attrs={'class':'a-price a-text-price'})
        if not oldPrice is None:
            oldPrice = oldPrice.find('span', attrs={'class':'a-offscreen'})
        if not oldPrice is None:
            oldPrice = oldPrice.text

        # store results
        data_dict[index] = {}
        data_dict[index]['itemLink'] = itemLink
        data_dict[index]['name'] = name
        data_dict[index]['image'] = image
        data_dict[index]['reviewStars'] = reviewStars
        data_dict[index]['numberOfReviews'] = numberOfReviews
        data_dict[index]['currentPrice'] = currentPrice
        data_dict[index]['oldPrice'] = oldPrice
        index += 1
        

def save_dict_to_json(dictionary, filename):
    with open(filename, 'w') as file:
        json.dump(dictionary, file, indent=4)
    print(f"Saved file '{filename}'")
        
        
def load_json(filename):
    with open(filename, 'r') as file:
        data = json.load(file)
    return data


def books_web_scraping():
    data_dict = {}
    BEST_SELLERS_BOOKS_URLS = [
        "https://www.amazon.com/best-sellers-books-Amazon/zgbs/books",
        "https://www.amazon.com/best-sellers-books-Amazon/zgbs/books/ref=zg_bs_pg_2?_encoding=UTF8&pg=2"
    ]
    FILENAME = "AmazonBestSellersBooks.json"        
    
    for url in tqdm_notebook(BEST_SELLERS_BOOKS_URLS):
        soup = get_soup(url)
        get_bestsellerbooks(soup, data_dict)
        save_dict_to_json(data_dict, FILENAME)
            
    print(f"Total data: {len(data_dict)}")


def show_books_results(data, n=10):
    for i in random.sample(range(len(data)), n):
        index = str(i)
        title = data[index]['title']
        image = data[index]['image']
        itemLink = data[index]['itemLink']
        author = data[index]['author']
        reviewStars = data[index]['reviewStars']
        numberOfReviews = data[index]['numberOfReviews']
        coverType = data[index]['coverType']
        price = data[index]['price']
        
        image = requests.get(image, stream=True).raw
        image =Image.open(image)
        plt.imshow(image)
        plt.axis(False)
        plt.show()
        print(itemLink)
        print(title)
        print(author)
        print(f"{reviewStars} | {numberOfReviews}")
        print(coverType)
        print(price)
        print('-'*50)

        
def search_web_scraping(keyword, total_pages):
    data_dict = {}
    FILENAME = f"AmazonSearch_{keyword}.json"
    for page in tqdm_notebook(range(total_pages)):
        soup = get_amazon_search_soup(keyword, page+1)
        if soup is None: continue
        get_search_results(soup, data_dict)
        print(f"Page: {page+1} | Success | ",end='')
        save_dict_to_json(data_dict, FILENAME)
        
    print(f"Total data: {len(data_dict)}")
    

def show_search_results(data, n=10):
    for i in random.sample(range(len(data)), n):
        index = str(i)
        itemLink = data[index]['itemLink']
        name = data[index]['name']
        image = data[index]['image']
        reviewStars = data[index]['reviewStars']
        numberOfReviews = data[index]['numberOfReviews']
        currentPrice = data[index]['currentPrice']
        oldPrice = data[index]['oldPrice']
        
        image = requests.get(image, stream=True).raw
        image =Image.open(image)
        plt.imshow(image)
        plt.axis(False)
        plt.show()
        print(itemLink)
        print(name)
        print(f"{reviewStars} | {numberOfReviews}")
        print(f"{currentPrice} | ({oldPrice})")
        print('-'*50)
    
    
def get_item_info(itemUrl):
    itemInfo = {}
    soup = get_soup(itemUrl)
    if not soup is None:
        details = soup.find_all("tr", attrs={"class":"a-spacing-small"})
        for detail in details:
            temp = []
            for info in detail.find_all("span"):
                if not info is None:
                    temp.append(info.text)
            itemInfo[temp[0]] = temp[1]
    
    return itemInfo


def get_data_info(filename, keys=None):
    data = load_json(filename)
    
    if keys is None:
        keys = list(data.keys())
        
    new_keys = []
    for i in tqdm_notebook(keys, leave=False):
        itemUrl = data[i]['itemLink']
        itemInfo = get_item_info(itemUrl)
        if len(itemInfo) == 0: new_keys.append(i)
        data[i]['itemInfo'] = itemInfo
        save_dict_to_json(data, filename)
            
    return new_keys


def get_all_data_info(filename, keys=None, max_try=5):
    
    for i in range(max_try):
        keys = get_data_info(filename, keys)
        if len(keys) == 0: break
        print(f"Attempt: {i+1} | Number of failures: {len(keys)} | Retrying")
    
    print(f"Number of failures: {len(keys)}")
    print("DONE")
    
    
def get_price_from_string(x):
    if x is None:
        return np.nan
    else:
        return float(x.replace(',', '').strip('$'))
    
def get_review_score(x):
    if x is None:
        return np.nan
    else:
        return float(x.split(" ")[0])
    
def get_number_of_reviews(x):
    if x is None:
        return np.nan
    else:
        try:
            return float(x.replace(',', ''))
        except:
            return np.nan

def get_brand(x):
    if 'Brand' in x:
        return x['Brand']
    else:
        return None