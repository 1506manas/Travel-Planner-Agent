from phi.tools.python import PythonTools
from dotenv import load_dotenv
import requests
import os

load_dotenv()
flight_api = os.getenv('FLIGHT_API_KEY')

class FlightSearchTool(PythonTools):
    name = "flight_search"
    description = (
        "Tool for searching flights using a public flight API."
        "Suggest a flight between the departure and arrival cities."
        "Try to get the flight details like airline name and flight number if possible."
    )

    def run(self, departure, destination, date):
        try:
            # Using Aviationstack public API (or mock free flight API)
            api_key = flight_api
            url = f"http://api.aviationstack.com/v1/flights?access_key={api_key}&dep_iata={departure}&arr_iata={destination}&flight_date={date}"
            response = requests.get(url)
            data = response.json()

            if "data" in data and len(data["data"]) > 0:
                flight = data["data"][0]
                airline = flight["airline"]["name"]
                flight_number = flight["flight"]["number"]
                dep_time = flight["departure"]["scheduled"]
                arr_time = flight["arrival"]["scheduled"]
                return f"Flight {airline} {flight_number} departs at {dep_time} and arrives at {arr_time}."
            else:
                return "No flights found for this route and date."

        except Exception as e:
            return f"Flight search failed: {str(e)}"
