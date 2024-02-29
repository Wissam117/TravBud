from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup
from PIL import Image
from io import BytesIO
import geocoder
import pandas as pd

app = Flask(__name__)

@app.route('/search_hotels', methods=['POST'])
def search_hotels():
    data = request.json
    search_destination = data['search_destination']
    no_of_adults = data['no_of_adults']
    no_of_children = data['no_of_children']
    no_of_rooms = data['no_of_rooms']
    children_ages = data['children_ages']  # Expect list of ages
    start_date = data['start_date']
    end_date = data['end_date']
    max_budget = data['max_budget']
    min_review_points = data['min_review_points']

    url = build_url(search_destination, no_of_adults, no_of_children, no_of_rooms, children_ages, start_date, end_date, max_budget, min_review_points)
    hotels = fetch_hotel_data(url)
    hotels_data = process_hotel_data(hotels)
    save_hotels_to_csv(hotels_data)

    return jsonify({"status": "success", "message": "Hotels data processed and saved."})

@app.route('/search_restaurants', methods=['POST'])
def search_restaurants():
    data = request.json
    location = data['location']

    fetch_tripadvisor_data(location)

    return jsonify({"status": "success", "message": "Restaurants data processed and saved."})

def build_url(search_destination, no_of_adults, no_of_children, no_of_rooms, children_ages, start_date, end_date, max_budget, min_review_points):
    base_url = f"https://www.booking.com/searchresults.html?ss={search_destination}&group_adults={no_of_adults}&no_rooms={no_of_rooms}&group_children={no_of_children}&checkin={start_date}&checkout={end_date}&nflt=price%3DPKR-min-{max_budget}-1%3Breview_score%3D{min_review_points}0"
    if int(no_of_children) > 0:
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
        # Process hotel images if needed
        hotels_data.append({'name': name, 'location': location, 'price': price})
        break  # Remove break to process all hotels
    return hotels_data

def save_hotels_to_csv(hotels_data):
    hotels_df = pd.DataFrame(hotels_data)
    hotels_df.to_csv('hotels.csv', header=True, index=False)

def getlatlong(loca):
    geolocator = geocoder.osm(loca)
    return geolocator.latlng

def fetch_tripadvisor_data(loca, category="restaurants", radius=5):
    api_key = "Your_TripAdvisor_API_Key_Here"
    locationx, locationy = getlatlong(loca)
    url = f"https://api.content.tripadvisor.com/api/v1/location/nearby_search?latLong={locationx},{locationy}&key={api_key}&category={category}&radius={radius}&language=en"
    
    headers = {"accept": "application/json"}
    response = requests.get(url, headers=headers)
    data = response.json()
    
    # Process and save restaurant data as needed
    # This is a placeholder for where you would process and save your TripAdvisor data
    print("Restaurant data processed")

if __name__ == '__main__':
    app.run(debug=True)







