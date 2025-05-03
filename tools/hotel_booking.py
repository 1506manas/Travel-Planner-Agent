from phi.tools.python import PythonTools
from dotenv import load_dotenv
import requests
import os

load_dotenv()
opentrip_api = os.getenv('OPENTRIP_API_KEY')

class HotelBookingTool(PythonTools):
    name = "hotel_booking"
    description = (
        "Tool for finding hotels in a location."
        "Suggest a hotel in the arrival city."
        "Suggest the check in and check out time."
    )

    def run(self, destination, date):
        try:
            # Using OpenTripMap API for places (hotels/accommodation)
            api_key = opentrip_api
            url = f"https://api.opentripmap.com/0.1/en/places/geoname?name={destination}&apikey={api_key}"
            geo_data = requests.get(url).json()
            
            lon = geo_data.get("lon")
            lat = geo_data.get("lat")
            
            places_url = f"https://api.opentripmap.com/0.1/en/places/radius?radius=5000&lon={lon}&lat={lat}&kinds=accomodations&apikey={api_key}"
            places_data = requests.get(places_url).json()
            
            if "features" in places_data and len(places_data["features"]) > 0:
                place_name = places_data["features"][0]["properties"]["name"]
                return f"Found hotel: {place_name} in {destination}."
            else:
                return "No hotels found."
        
        except Exception as e:
            return f"Hotel search failed: {str(e)}"
