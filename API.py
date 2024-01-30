from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from datetime import datetime

# Input placeholders
max_budget = "10000"
search_destination = "Islamabad"
no_of_adults = "1"
no_of_children = "1"
no_of_rooms = "1"
children_ages = ["1", "1", "1", "1", "1"]  # Add more as per requirement
start_date = "2024-02-29"  # Format: YYYY-MM-DD
end_date = "2024-03-03"  # Format: YYYY-MM-DD
max_per_day_accomodation_budget="10000"
minimum_review_points="8"

# Setting up the Chrome WebDriver
service = Service(executable_path="chromedriver.exe")
driver = webdriver.Chrome(service=service)

url = f"https://www.booking.com/searchresults.html?ss={search_destination}&ssne={search_destination}&ssne_untouched={search_destination}&label=gen173nr-1FCAEoggI46AdIM1gEaLUBiAEBmAExuAEYyAEP2AEB6AEB-AECiAIBqAIEuAKr4dytBsACAdICJDBhMWQxNjRjLTczY2YtNDRkYS04MjllLTFhN2U5YzRlMzM3MtgCBeACAQ&aid=304142&lang=en-us&sb=1&src_elem=sb&src=searchresults&dest_id=-2762812&dest_type=city&checkin={start_date}&checkout={end_date}&ltfd=%3A%3A5-2024_4-2024%3A%3A&group_adults={no_of_adults}&no_rooms={no_of_rooms}&group_children={no_of_children}"
#if there are children
if int(no_of_children)>0 :
    for i in range(int(no_of_children)):
        url += f"&age={children_ages[i]}"
#extra filters
url+=f"&nflt=price%3DPKR-min-{max_per_day_accomodation_budget}-1%3Breview_score%3D{minimum_review_points}0" #good reviews and budget constraint

# Navigating to Booking.com
driver.get(url)

time.sleep(10)  # Adjust sleep time as necessary
top_pick={}

result = driver.find_elements(By.CLASS_NAME, "f6431b446c")
header = result.pop(0)

list_price = []
list_names = []

class Hotel:
    def __init__(self, name, price):
        self.name = name
        self.price = price

print(f"HEADER: {header.text}")

list_hotels = []
for idx in range(0, len(result), 2):
    hotel = Hotel(result[idx].text, int(result[idx + 1].text.replace(",", "").replace("PKR", "")))
    list_hotels.append(hotel)

for hotel in list_hotels:
    print(f"{hotel.name} - {hotel.price}")

    
time.sleep(200)
driver.quit()
