from selenium import webdriver
from selenium.webdriver.chrome.service import service
import time
service=Service(executable_path="chromedriver.exe")
driver=webdriver.Chrome(service=service)
driver.get(https://www.google.com)

