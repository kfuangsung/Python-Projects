import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager

driver = webdriver.Chrome(service=Service(ChromeDriverManager(log_level=0).install()))
url = "https://www.amazon.com/Best-Sellers-Books/zgbs/books"
driver.get(url)
driver.implicitly_wait(30)

html = driver.find_element(By.TAG_NAME, 'html')
html.send_keys(Keys.END)

time.sleep(5)