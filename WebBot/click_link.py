from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

driver = webdriver.Chrome(service=Service(ChromeDriverManager(log_level=0).install()))
url = "https://www.goodreads.com/"
driver.get(url)
driver.implicitly_wait(30) # set only once
my_element = driver.find_element(By.LINK_TEXT, "Best Books 2021")
my_element.click()

