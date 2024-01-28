from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import time
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

def search_for_destination(driver, destination_for_search):
    search_field = driver.find_element_by_id('ss')

    search_field.send_keys(destination_for_search)

    driver.find_element_by_class_name('sb-searchbox__button').click()
      #finding search button and clicking it
    wait = WebDriverWait(driver, timeout=10).until(
        EC.presence_of_all_elements_located(
            (By.CLASS_NAME, 'sr-hotel__title')))

def scrape_results(driver, topn_results):
    accommodations_urls = list()
    top_results = list()

    for accomodation_title in driver.find_elements_by_class_name('sr-hotel__title'):
        accommodations_urls.append(accomodation_title.find_element_by_class_name('hotel_name_link').get_attribute('href'))

    for url in range(0, topn_results):
        if url == topn_results:
            break
        url_data = scrape_accommodation_data(driver, accommodations_urls[url])
        top_results.append(url_data)
    
    return top_results

def scrape_accommodation_data(driver, accommodation_url):
    driver.get(accommodation_url)
    time.sleep(12)

    accommodation_fields = dict()

    # Get the accommodation name
    accommodation_fields['name'] = driver.find_element_by_id('hp_hotel_name').text.strip('Hotel')

    # Get the accommodation score
    accommodation_fields['score'] = driver.find_element_by_class_name('bui-review-score--end').find_element_by_class_name('bui-review-score__badge').text
    
    # Get the accommodation location
    accommodation_fields['location'] = driver.find_element_by_id('showMap2').find_element_by_class_name('hp_address_subtitle').text

    # Get the most popular facilities
    accommodation_fields['popular_facilities'] = list()
    facilities = driver.find_element_by_class_name('hp_desc_important_facilities')

    for facility in facilities.find_elements_by_class_name('important_facility'):
        accommodation_fields['popular_facilities'].append(facility.text)
    
    return accommodation_fields

if __name__ == '__main__':

        service = Service(executable_path="chromedriver.exe")
        driver = webdriver.Chrome(service=service)
        driver.get("https://www.booking.com/")

        search_for_destination(driver, 'Islamabad')
        top_results = scrape_results(driver, 1)
        print(top_results)        
   
        driver.quit()
