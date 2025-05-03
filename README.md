# 🧠 Travel Planner Agent

An AI-powered Trip Planner that helps you organize your travel from one city to another — including flights, hotels, places to visit, and syncing everything directly with your Google Calendar.  
Built using an intelligent **Agent AI** that automates planning based on user preferences.

---

## 🤖 What is Agent AI?

This application leverages **Agent AI** built with **PhiData** — a framework that allows creating intelligent and modular agents that can perform multiple tasks through tool usage.

In the context of this travel planner, the **Agent AI**:

- Takes the user's inputs and intelligently coordinates multiple tools to gather all relevant travel data
- Chooses appropriate API calls dynamically based on intent (e.g., searching for flights or places)
- Maintains context across multiple steps of the planning process
- Automatically structures and schedules the itinerary, reducing manual effort
- Integrates all the results seamlessly into the user’s Google Calendar

This allows users to experience a **smart assistant-like interaction**, where they just specify basic details, and the agent handles the rest.

---

## ✨ Features

This application takes **4 user inputs**:
- 🏙️ **Departure City**
- 🏙️ **Arrival City**
- 📅 **Date of Departure**
- ⏱️ **Free Time (in hours)**

Using these, the agent performs the following:

1. ✈️ **Suggest a Flight** between the two cities  
2. 🏨 **Suggest a Hotel** in the arrival city  
3. 📍 **Suggests nearby places** to explore within the free time  
4. 📆 **Adds all the above information** to your **Google Calendar** automatically

---

## 🛠 Technologies Used

| Component       | Technology/API Used                           |
|----------------|------------------------------------------------|
| Agent AI       | [PhiData](https://docs.phidata.com/)             |
| Flight Info    | [Aviationstack API](https://aviationstack.com/)|
| Hotels & Places| [OpenTripMap API](https://dev.opentripmap.org/login)     |
| Calendar Sync  | [Google Calendar API](https://console.developers.google.com/) via Google Developer Console |

---

## 🚀 Getting Started

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt

1. **Run The Application**:
   ```bash
   python main.py
