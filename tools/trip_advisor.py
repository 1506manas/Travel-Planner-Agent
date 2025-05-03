from phi.tools.python import PythonTools
from dotenv import load_dotenv
import requests
import os

load_dotenv()
opentrip_api = os.getenv('OPENTRIP_API_KEY')

class TripAdvisorTool(PythonTools):
    name = "trip_advisor"
    description = (
        "Suggests places to visit nearby using OpenTripMap API."
        "The date and time should follow the format as %Y-%m-%d %H:%M only"
    )

    def run(self, location, free_time_hours):
        try:
            api_key = opentrip_api
            url = f"https://api.opentripmap.com/0.1/en/places/geoname?name={location}&apikey={api_key}"
            geo_data = requests.get(url).json()
            lon = geo_data.get("lon")
            lat = geo_data.get("lat")

            kinds = "interesting_places" if free_time_hours > 2 else "cafes"
            places_url = f"https://api.opentripmap.com/0.1/en/places/radius?radius=3000&lon={lon}&lat={lat}&kinds={kinds}&limit=5&apikey={api_key}"
            places_data = requests.get(places_url).json()
            
            suggestions = []
            if "features" in places_data:
                for feature in places_data["features"]:
                    suggestions.append(feature["properties"]["name"])
            return f"Suggested places: {', '.join(suggestions)}"
        
        except Exception as e:
            return f"Trip advisory failed: {str(e)}"
