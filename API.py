from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Input placeholders
max_budget = "10000"
search_destination = "Islamabad"
no_of_adults = "2"
no_of_children = "1"
children_ages = ["10"]  # Add more as per requirement
start_date = "2024-02-15"  # Format: YYYY-MM-DD
end_date = "2024-02-16"  # Format: YYYY-MM-DD

# Setting up the Chrome WebDriver
service = Service(executable_path="chromedriver.exe")
driver = webdriver.Chrome(service=service)

# Navigating to Booking.com
driver.get("https://www.booking.com")

time.sleep(12)  # Adjust sleep time as necessary

# Determine window size
window_width = driver.get_window_size()["width"]
window_height = driver.get_window_size()["height"]
'''

'''

# Wait for the destination field to be available and enter the search destination
destination_input = WebDriverWait(driver, 50).until(
    EC.presence_of_element_located((By.ID, "b2indexPage")) #ss
)
destination_input.send_keys(search_destination)

# Selecting the start and end date
date_field = driver.find_element(By.CLASS_NAME, "xp__dates")
date_field.click()
# Use the `data-date` attribute to find the correct date elements and click them
start_date_element = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, f"td[data-date='{start_date}']"))
)
start_date_element.click()
end_date_element = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, f"td[data-date='{end_date}']"))
)
end_date_element.click()

# Adjusting the number of adults and children
guest_field = driver.find_element(By.CLASS_NAME, "xp__guests")
guest_field.click()

# Code to set the correct number of adults
adults_minus_button = driver.find_element(By.CSS_SELECTOR, "button[aria-label='Decrease number of Adults']")
adults_plus_button = driver.find_element(By.CSS_SELECTOR, "button[aria-label='Increase number of Adults']")
# Adjust adults
for _ in range(int(no_of_adults) - 1):  # Assumes default is 1 adult
    adults_plus_button.click()


children_plus_button = driver.find_element(By.CSS_SELECTOR, "button[aria-label='Increase number of Children']")
for _ in range(int(no_of_children)):
    children_plus_button.click()
   
    child_age_dropdown = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, "sb-group__field.sb-group-children__field.sb-group__field--select"))
    )
    for index, age in enumerate(children_ages):
        child_age_dropdown[index].find_element(By.TAG_NAME, "select").send_keys(age)


search_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
search_button.click()

# Wait for the page to load and display the top result
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "sr_property_block")))
top_result = driver.find_element(By.CLASS_NAME, "sr_property_block")
print(top_result.text)

# Clean up by closing the browser
driver.quit()
