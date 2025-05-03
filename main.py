import os
from datetime import datetime
from dotenv import load_dotenv
from phi.agent import Agent
from phi.model.groq import Groq

def delete_all_except(directory, files_to_keep):
    """Deletes all files in a directory except those specified in files_to_keep.

    Args:
        directory (str): The path to the directory.
        files_to_keep (list): A list of filenames to exclude from deletion.
    """
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        if os.path.isfile(file_path) and filename not in files_to_keep:
            os.remove(file_path)

def format_user_date(input_date: str) -> str:
    """Convert user input date (mmm-dd-yyyy) to YYYY-MM-DD format."""
    try:
        date_obj = datetime.strptime(input_date, "%b-%d-%Y")
        return date_obj.strftime("%Y-%m-%d")
    except ValueError:
        try:
            date_obj = datetime.strptime(input_date, "%B-%d-%Y")
            return date_obj.strftime("%Y-%m-%d")
        except ValueError:
            return input_date

load_dotenv()

# Load API keys
groq_api = os.getenv('GROQ_API_KEY')
phi_api = os.getenv('PHI_API_KEY')

# Import custom tools
from tools.flight_search import FlightSearchTool
from tools.hotel_booking import HotelBookingTool
from tools.calendar_manager import CalendarManagerTool
from tools.trip_advisor import TripAdvisorTool

# Define the agent
travel_agent = Agent(
    name="travel_assistant_agent",
    description="Execute the methods given in each tools, and pass the required parameters by your intelligence.",
    model=Groq(id="llama3-70b-8192"),
    tools=[
        FlightSearchTool(),
        HotelBookingTool(),
        TripAdvisorTool(),
        CalendarManagerTool().run
    ],
    instructions=[
        "You are a smart personal travel assistant.",
        "Convert the dates into the format of %Y-%m-%d %H:%M only.",
        "suggest users a flight, hotel, suggest nearby places to visit during free time.",
        "Help to update calendar with all different events separately.",
    ],
    markdown=True,
    show_tool_call=True,
    debug_mode=True,
)

if __name__ == "__main__":
    From = input("Enter the Departure City: ")
    To = input("Enter the Arrival City: ")
    Date = input("Enter the Date (YYYY-MM-DD): ")
    freeTime = input("Enter the free times in hours (range or integer): ")

    formated_date = format_user_date(Date)

    user_input = (
        f"Plan a trip from {From} to {To} on {Date}. "
        f"suggest a hotel, and suggest time and places to visit if I have {freeTime} hours free, update the calendar and book the different time slots for the different events."
        "The output format should contain 4 headings. 1) Flight Details, 2) Hotel Details, 3) Nearby Places to Visit, 4) Calendar Time Updation with Details"
    )

    print("\n=== Travel Plan Output ===\n")
    print(travel_agent.print_response(user_input, stream=True))

    # Example usage
    directory_path = os.getcwd()
    files_to_keep = ["calendar_debug_log.txt", ".env", "credentials.json", "main.py", "requirements.txt", "test.py", "token.pickle", "tools", "sample"]
    delete_all_except(directory_path, files_to_keep)
