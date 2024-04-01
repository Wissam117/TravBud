from flask import Flask, jsonify, request
import requests
from bs4 import BeautifulSoup
import pandas as pd
import geocoder



app = Flask(__name__)



@app.route('/fetch-hotels', methods=['POST'])
def fetch_hotels():
    data = request.json
    search_destination = data.get('search_destination')
    no_of_adults = data.get('no_of_adults')
    no_of_children = data.get('no_of_children')
    no_of_rooms = data.get('no_of_rooms')
    children_ages = data.get('children_ages',[])
    start_date = data.get('start_date')
    end_date = data.get('end_date')
    max_budget = data.get('max_budget')
    min_review_points = data.get('min_review_points')
    url = build_url(search_destination, no_of_adults, no_of_children, no_of_rooms, children_ages, start_date, end_date, max_budget, min_review_points)
    hotels = fetch_hotel_data(url)
    hotels_data = process_hotel_data(hotels)

    return jsonify(hotels_data)

@app.route('/fetch-restaurants', methods=['GET'])
def fetch_restaurants():
    loca = request.args.get('location')
    fetch_tripadvisor_data(loca)  
    df = pd.read_csv('restaurants.csv')
    return df.to_json(orient='records')


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
        hotels_data.append({'name': name, 'location': location, 'price': price,'thumbnail':thumbnail_url})
        break 
    return hotels_data

def getlatlong(loca):
    geolocator = geocoder.osm(loca)
    locationx = geolocator.latlng[0]
    locationy = geolocator.latlng[1]
    return locationx,locationy
    

def fetch_tripadvisor_data(loca, category="restaurants", radius=5, api_key="8A8C09F8CDC8468B9AEAA1460B8F54F7"): #added api_key parameter
    headers = {"accept": "application/json"}
    headers1 = {"accept": "application/json"}
    locationx,locationy=getlatlong(loca)
    location_id=""
    extracted_data = []

    url = f"https://api.content.tripadvisor.com/api/v1/location/nearby_search?latLong={locationx}%2C%20{locationy}&key={api_key}&category={category}&radius={radius}"
    if radius:
        url += "&radiusUnit=km"
    url += "&language=en"
    response = requests.get(url, headers=headers)
    data = response.json()   
    for item in data["data"]:
        if "data" in data:
            location_id = item.get("location_id")
            url1 = f"https://api.content.tripadvisor.com/api/v1/location/{location_id}/photos?key={api_key}&language=en&limit=3&source=Management"
            response = requests.get(url1,headers=headers1)
            data1 = response.json()
        break

        


if __name__ == '__main__':
    app.run(debug=True)