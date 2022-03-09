import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

driver = webdriver.Chrome(service=Service(ChromeDriverManager(log_level=0).install()))
url = "https://www.amazon.com/"
driver.get(url)
driver.implicitly_wait(30)

search_box = driver.find_element(By.CSS_SELECTOR, 'input[id="twotabsearchtextbox"]')
search_box.send_keys('isaac asimov')

search_submit = driver.find_element(By.CSS_SELECTOR, 'input[id="nav-search-submit-button"]')
search_submit.click()

time.sleep(5)