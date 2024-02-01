from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from PIL import Image
from io import BytesIO
from datetime import datetime

class Hotel:
        def __init__(self, name, price):
            self.name = name
            self.price = price

def bookingcomscrap(max_per_day_accomodation_budget,search_destination,no_of_rooms,no_of_adults,no_of_children,children_ages,start_date,end_date,minimum_review_points):
    list_price = []
    list_names = []
    hotel_names = []
    hotel_prices = []
    list_hotels = []

    url = f"https://www.booking.com/searchresults.html?ss={search_destination}&ssne={search_destination}&ssne_untouched={search_destination}&label=gen173nr-1FCAEoggI46AdIM1gEaLUBiAEBmAExuAEYyAEP2AEB6AEB-AECiAIBqAIEuAKr4dytBsACAdICJDBhMWQxNjRjLTczY2YtNDRkYS04MjllLTFhN2U5YzRlMzM3MtgCBeACAQ&aid=304142&lang=en-us&sb=1&src_elem=sb&src=searchresults&dest_id=-2762812&dest_type=city&checkin={start_date}&checkout={end_date}&ltfd=%3A%3A5-2024_4-2024%3A%3A&group_adults={no_of_adults}&no_rooms={no_of_rooms}&group_children={no_of_children}"
   
    if int(no_of_children)>0 :
        for i in range(int(no_of_children)):
            url += f"&age={children_ages[i]}"
   
    url+=f"&nflt=price%3DPKR-min-{max_per_day_accomodation_budget}-1%3Breview_score%3D{minimum_review_points}0" #good reviews and budget constraint

    driver.get(url)
    time.sleep(15)
    result = driver.find_elements(By.CLASS_NAME, "f6431b446c")

    header = result.pop(0)
    
    hheader = ''.join(c for c in header.text if c.isdigit() )
   
    no_of_properties=int(hheader)
    if no_of_properties>0:

        for idx in range(0, len(result) and 10, 2): 
            hname= result[idx].text
            hpricie = ''.join(c for c in result[idx + 1].text if c.isdigit() )
            hotel = Hotel(hname, int(hpricie))
            list_hotels.append(hotel)
            
        for hotel in list_hotels:
            hotel_names.append(hotel.name)
            hotel_prices.append(hotel.price)
        for hoteel1 in hotel_names :
            top_pick=hoteel1
            break
        for hoteel2 in hotel_prices:
            top_pick_price=hoteel2
            break

        image_hotel=driver.find_element(By.CLASS_NAME,"f9671d49b1")
        screenshot=image_hotel.screenshot_as_png
        image=Image.open(BytesIO(screenshot))
        
        width, height = image.size 
        left = 4
        top = height / 5
        right = 154
        bottom = 3 * height / 5
        im1 = image.crop((left, top, right, bottom))
        newsize = (600, 600)
        im1 = im1.resize(newsize)
        #im1.show() 
        #output_path = "image.png"  
        #im1.save(output_path)
        time.sleep(20)

    else:
        time.sleep(20)
        exit

#'''
search_destination = input("Enter search destination: ")
no_of_adults = input("Enter number of adults: ")
no_of_children = input("Enter number of children: ")
no_of_rooms = input("Enter number of rooms: ")
children_ages_input = input("Enter children ages (comma-separated): ")
children_ages = children_ages_input.split(", ")
start_date = input("Enter start date (YYYY-MM-DD): ")
end_date = input("Enter end date (YYYY-MM-DD): ")
max_per_day_accomodation_budget = input("Enter max per day accommodation budget: ")
minimum_review_points = input("Enter minimum review points: ")
#'''

service = Service(executable_path="chromedriver.exe")
driver = webdriver.Chrome(service=service)

bookingcomscrap(max_per_day_accomodation_budget,search_destination,no_of_rooms,no_of_adults,no_of_children,children_ages,start_date,end_date,minimum_review_points)


driver.quit()
