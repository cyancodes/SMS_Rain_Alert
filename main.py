import requests
from twilio.rest import Client
import os

OWM_API_KEY = os.environ.get("OWM_API_KEY")
MY_LAT = os.environ.get("MY_LAT")
MY_LONG = os.environ.get("MY_LONG")

TWILIO_SID = os.environ.get("TWILIO_SID")
TWILIO_AUTH_TOKEN = os.environ.get("TWILIO_AUTH_TOKEN")
TWILIO_FROM = os.environ.get("TWILIO_FROM")
TWILIO_TO = os.environ.get("TWILIO_TO")

params = {
    "lat": MY_LAT,
    "lon": MY_LONG,
    "appid": OWM_API_KEY,
    "units": "metric",
    "cnt": 4
}
response = requests.get("https://api.openweathermap.org/data/2.5/forecast", params=params)
response.raise_for_status()
weather_json = response.json()

#  Uses list comprehension to create a list of hours when the ID is less than 700,
#  which indicates possible rain
hourly_weather_ids = [
    entry["weather"][0]["id"] for entry in weather_json["list"]
    if entry["weather"][0]["id"] <= 700]

#  Checks to see if there have been any rain entries added to the list, if so
#  it means there might be rain, and will tell you to bring a brolly.
if len(hourly_weather_ids) > 0:
    client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)
    message = client.messages \
        .create(
        body="It's gonna be a rainy one. Make sure to bring a ☂️",
        from_=TWILIO_FROM,
        to=TWILIO_TO
    )
    print(message.status)
