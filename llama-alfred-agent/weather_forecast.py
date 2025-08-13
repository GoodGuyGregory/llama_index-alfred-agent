import datetime
import unicodedata


class WeatherForecast:

    def __init__(self, response_text: dict):
        self.weather_emoji = None
        # handles the parsing of the attributes We need
        self._create_weather_attributes(response_text=response_text)

        self.name: str
        self.temp: float
        self.feels_like: float
        self.weather_desc: str
        self.sunrise: datetime
        self.sunset: datetime
    
    def _create_weather_attributes(self, response_text: dict):
        self.name = response_text["name"]
        # "weather":[{"id":800,"main":"Clear","description":"clear sky","icon":"01d"}],
        self.weather_desc = response_text["weather"][0]["description"].capitalize()
        
        try:
            if response_text["weather"][0]["icon"]:
                self.weather_emoji = unicodedata.lookup('U+' + response_text["weather"][0]["icon"])
        except KeyError:
            print(f"no emoji found for conditions: {self.weather_desc}")
        
        self.temp = response_text["main"]["temp"]
        self.feels_like = response_text["main"]["feels_like"]
        
        sunrise_unix = response_text["sys"]["sunrise"]
        
        date_time = datetime.datetime.fromtimestamp(sunrise_unix)
        # Format the date and time as HH:MM
        self.sunrise = date_time.strftime("%H:%M")
        
        sunset_unix = response_text["sys"]["sunset"]
        
        date_time = datetime.datetime.fromtimestamp(sunset_unix)
        # Format the date and time as HH:MM
        self.sunset = date_time.strftime("%H:%M")


    