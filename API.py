from bs4 import BeautifulSoup
import requests
import pandas as pd
from PIL import Image
from io import BytesIO

def get_user_input():
    search_destination = input("Enter search destination: ")
    no_of_adults = input("Enter number of adults: ")
    no_of_children = input("Enter number of children: ")
    no_of_rooms = input("Enter number of rooms: ")
    children_ages = input("Enter children ages (comma-separated): ").split(", ")
    start_date = input("Enter start date (YYYY-MM-DD): ")
    end_date = input("Enter end date (YYYY-MM-DD): ")
    max_budget = input("Enter max per day accommodation budget: ")
    min_review_points = input("Enter minimum review points: ")
    return search_destination, no_of_adults, no_of_children, no_of_rooms, children_ages, start_date, end_date, max_budget, min_review_points

def build_url(search_destination, no_of_adults, no_of_children, no_of_rooms, children_ages, start_date, end_date, max_budget, min_review_points):
    base_url = f"https://www.booking.com/searchresults.html?ss={search_destination}&ssne={search_destination}&ssne_untouched={search_destination}&group_adults={no_of_adults}&no_rooms={no_of_rooms}&group_children={no_of_children}&checkin={start_date}&checkout={end_date}&nflt=price%3DPKR-min-{max_budget}-1%3Breview_score%3D{min_review_points}0"
    if(int(no_of_children) > 0):
        for age in children_ages:
            base_url += f"&age={age}"
    return base_url

def fetch_hotel_data(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; CrOS x86_64 8172.45.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.64 Safari/537.36',
        'Accept-Language': 'en-US, en;q=0.5'
    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    return soup.findAll('div', {'data-testid': 'property-card'})

def process_hotel_data(hotels):
    hotels_data = []
    for hotel in hotels:
        name = hotel.find('div', {'data-testid': 'title'}).text.strip()
        location = hotel.find('span', {'data-testid': 'address'}).text.strip()
        price = ''.join(c for c in hotel.find("span", {"data-testid": "price-and-discounted-price"}).text if c.isdigit())
        thumbnail_url = hotel.find("img", {"data-testid": "image"})['src']
        process_image(thumbnail_url)
        hotels_data.append({'name': name, 'location': location, 'price': price})
        break 
    return hotels_data

def process_image(thumbnail_url):
    response = requests.get(thumbnail_url)
    image = Image.open(BytesIO(response.content))
    cropped_image = crop_and_resize_image(image)
    save_image(cropped_image, "image.png")

def crop_and_resize_image(image):
    width, height = image.size
    crop_rectangle = (4, height / 5, 154, 3 * height / 5)
    cropped_image = image.crop(crop_rectangle).resize((480, 360))
    return cropped_image

def save_image(image, path):
    image.save(path)

def save_hotels_to_csv(hotels_data):
    hotels_df = pd.DataFrame(hotels_data)
    hotels_df.to_csv('hotels.csv', header=True, index=False)

def fetch_tripadvisor_data(loca, category="restaurants", radius=7):
    url = f"https://api.content.tripadvisor.com/api/v1/location/search?key=8A8C09F8CDC8468B9AEAA1460B8F54F7&searchQuery={loca}&category={category}&radius={radius}"
    if radius:
        url += "&radiusUnit=km"
    url += "&language=en"

    headers = {"accept": "application/json"}
    response = requests.get(url, headers=headers)
    data = response.json()  

    # Extracting required data
    extracted_data = []
    if "data" in data:
        for item in data["data"]:
            location_id = item.get("location_id")
            name = item.get("name")
            address_string = item["address_obj"].get("address_string", "")
            city = item["address_obj"].get("city", "")
            extracted_data.append({
                "location_id": location_id,
                "name": name,
                "address_string": address_string,
                "city": city
            })
            break

    if extracted_data:
        df = pd.DataFrame(extracted_data)
        df.to_csv('tripadvisor_data.csv', index=False)
        print("TripAdvisor data saved to tripadvisor_data.csv")
    else:
        print("No data found to save")

def main():
    user_inputs = get_user_input()
    url = build_url(*user_inputs)
    hotels = fetch_hotel_data(url)
    hotels_data = process_hotel_data(hotels)
    save_hotels_to_csv(hotels_data)
    fetch_tripadvisor_data(user_inputs[0])  
   

if __name__ == "__main__":
    main()
