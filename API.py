from flask import Flask, jsonify, request
import requests
from bs4 import BeautifulSoup
import pandas as pd
from PIL import Image
from io import BytesIO
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
    
    if hotels:
        hotels_data = process_hotel_data(hotels)
        success = save_hotels_to_csv(hotels_data)
        
        message = "Data saved" if success else "Data not saved"
        
        return jsonify({"message": message})
    else:
        return jsonify({"message": "No hotels found with the provided search criteria."})


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
        process_hotel_image(thumbnail_url)
        hotels_data.append({'name': name, 'location': location, 'price': price})
        break 
    return hotels_data

def getlatlong(loca):
    geolocator = geocoder.osm(loca)
    locationx = geolocator.latlng[0]
    locationy = geolocator.latlng[1]
    return locationx,locationy
    

def process_hotel_image(thumbnail_url):
    response = requests.get(thumbnail_url)
    image = Image.open(BytesIO(response.content))
    save_image(image, "Hotel.png")
    save_image(crop_and_resize_image(image), "Hotel.png")

def process_restaurant_image(restaurant_img_link,img_no):
    response = requests.get(restaurant_img_link)   
    ximage = Image.open(BytesIO(response.content))
    save_image(ximage,"Eatery"+".png")
    save_image(crop_and_resize_image(ximage),"Eatery"+f"{img_no}"+".png")


def process_restaurant_image(restaurant_img_link,img_no):
    response = requests.get(restaurant_img_link)   
    ximage = Image.open(BytesIO(response.content))
    save_image(ximage,"Eatery"+f"{img_no}"+".png")
    save_image(crop_and_resize_image(ximage),"Eatery"+f"{img_no}"+".png")

def crop_and_resize_image(image):
    resized_image = image.resize((300, 300))
    return resized_image


def save_image(image, path):
    image.save(path)

def save_hotels_to_csv(hotels_data):
    try:
        hotels_df = pd.DataFrame(hotels_data)
        hotels_df.to_csv('hotels.csv', header=True, index=False)
        return True  
    except Exception as e:
        print(f"Error saving hotels data to CSV: {e}")
        return False  


def fetch_tripadvisor_data(loca, category="restaurants", radius=5):
    api_key="8A8C09F8CDC8468B9AEAA1460B8F54F7"

    headers = {"accept": "application/json"}
    headers1 = {"accept": "application/json"}
    locationx,locationy=getlatlong(loca)
    location_id=""
    extracted_data = []
    x=1

    url = f"https://api.content.tripadvisor.com/api/v1/location/nearby_search?latLong={locationx}%2C%20{locationy}&key={api_key}&category={category}&radius={radius}"
    if radius:
        url += "&radiusUnit=km"
    url += "&language=en"
    response = requests.get(url, headers=headers)
    data = response.json()   
    for item in data["data"]:   
        if "data" in data:
            location_id = item.get("location_id")
            name = item.get("name")
            address_string = item["address_obj"].get("address_string", "")
            city = item["address_obj"].get("city", "")
                
        url1 = f"https://api.content.tripadvisor.com/api/v1/location/{location_id}/photos?key={api_key}&language=en&limit=3&source=Management"
        response = requests.get(url1,headers=headers1)
        data1 = response.json()  
        if "data" in data1:
            for item in data1["data"]:
                original_image_url = data1['data'][0]['images']['original']['url']
                url_for_original_image = ''.join(c for c in original_image_url if c.isalnum() or c in ':/.-_')
                process_restaurant_image(url_for_original_image,x)
                x+=1
                if x>1:
                    break

        if x>1:
            break

    extracted_data.append({
                "name": name,
                "address_string": address_string,
                "city": city
            })        

    if extracted_data:
        df = pd.DataFrame(extracted_data)
        df.to_csv('restaurants.csv', index=False)
    else:
       exit

if __name__ == '__main__':
    app.run(debug=True)
