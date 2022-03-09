import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

driver = webdriver.Chrome(service=Service(ChromeDriverManager(log_level=0).install()))
url = "https://web.archive.org/web/20180926132852/http://www.seleniumeasy.com/test/basic-first-form-demo.html"
driver.get(url)
driver.implicitly_wait(60)

sum1 = driver.find_element(By.ID, 'sum1')
sum2 = driver.find_element(By.ID, 'sum2')

sum1.send_keys(120)
sum2.send_keys(18)

button = driver.find_element(By.CSS_SELECTOR, "button[onclick='return total()']")
button.click()
time.sleep(5)
