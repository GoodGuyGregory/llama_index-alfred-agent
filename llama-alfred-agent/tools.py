from llama_index.core.tools import FunctionTool
from llama_index.tools.duckduckgo import DuckDuckGoSearchToolSpec
import colorama
import requests
import json
from datetime import datetime


from weather_forecast import WeatherForecast
from aqi_forecast import AQIForecast

import pandas as pd

class Tools:
    '''
        Tools Class holds all of the tools that Alfred could leverage.
        
        Included Tools:
        
        * duck_duck_go_search_tool : allows for searching Duck Duck Go for answers *see create_duck_duck_go_tool* for usage example
        
        * gotham_weather_tool: allows for string based queries to allow for weather checking based on popular cities. **see create_weather_api_tool* for usage example 
        
    '''
    def __init__(self, weather_api_key: str, air_now_api_key: str, status_updates=False ):
        self.status_updates = status_updates
        self.duck_duck_go_search_tool = self.create_duck_duck_go_tool()
        self.city_locations = self._retrieve_city_data()

        if weather_api_key is None:
            raise Exception('Missing weather_api_key')
        else:
            self.weather_api_key = weather_api_key
            
        if air_now_api_key is None:
            raise Exception('Missing air_now_api_key')
        else:
            self.air_now_api_key = air_now_api_key
            
            
        self.gotham_weather_tool = FunctionTool.from_defaults(self.get_weather_info)
        self.gotham_aqi_tool = FunctionTool.from_defaults(self.get_air_pollution_info)
        
        if self.status_updates:
            print(colorama.Fore.YELLOW + "✅ 🌞 Gotham Weather tool has been created")
            print(colorama.Fore.YELLOW + f"✅ 🌲🔥 Gotham Air Quality Index tool has been created")
        
        self.tool_belt = [self.duck_duck_go_search_tool, self.gotham_weather_tool, self.gotham_aqi_tool]
    
    def create_duck_duck_go_tool(self):
        '''
            creates the DuckDuckGo Search tool from LlamaIndex
            and returns the tool for later use
            
            Example usage:
            
            response = self.duck_duck_go_search_tool("Who is the silver robot from daft punk?")
            
            print(response.raw_output[-1]['body'])
            
            Args: 
                self : class instance
            Returns:
                search_tool (FunctionTool): represents the FunctionTool Spec for DuckDuckGoSearch
        '''
        # initializes the duckduckgosearchtool
        tool_spec = DuckDuckGoSearchToolSpec()
        
        search_tool = FunctionTool.from_defaults(tool_spec.duckduckgo_full_search)
        
        if self.status_updates:
            print(colorama.Fore.YELLOW + f"✅ 🦆 Duck Duck Go tool has been created")
        
        return search_tool
    
    def check_supplied_city(self, query_city: str):
        '''
            helper method to determine if the supplied `query_city` is in the city_locations
            which contains 50 cities that are the most populated US cities.

            Args:
                query_city (str): a city whose location is being queried
            Returns:
                found (bool) : represents the status of the city being queried, 
                                * True will be found
                                * False implies it is not found.
        '''
        found = True
        
        if query_city.capitalize() in self.city_locations.keys():
            return found
        else:
            found = False
            return found
    
    def get_weather_info(self, location: str):
        '''
            takes the top 50 cities from wikipedia by population and supplies them as cities
            to search weather for using the OpenWeatherAPI, leveraging the `_get_weather_info()` 
            function
            
            **Sources**
            
            * [Wikipedia Article](https://en.wikipedia.org/wiki/List_of_United_States_cities_by_population)
            * [OpenWeather API Documentation](https://openweathermap.org/api/one-call-3#current)
        
            Args:
                location (str): city to search the weather information through the API request
            Returns:
                forecast_resp (str): forecast which contains city name, forecast, temperature, feels like, sunrise, and sunset
                                        
                                    Example: 
                                    
                                    City: Portland
                                    Forecast: Clear sky 
                                    Temperature: 88.83 
                                    Feels Likes: 89.31 
                                    Sunrise: 06:08 
                                    Sunset: 20:23
        '''

        if self.check_supplied_city(location):
            
            lat, lon = self.city_locations[location.capitalize()] 
            us_units = "imperial"
            
            resp = requests.get(f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&units={us_units}&appid={self.weather_api_key}")

            if resp.status_code == 200:
                
                weather_forecast = WeatherForecast(response_text=json.loads(resp.text))
                
                if weather_forecast.weather_emoji: 
                    forecast_resp =  f"""City: {weather_forecast.name}\n Forecast: {weather_forecast.weather_emoji} {weather_forecast.weather_desc} \n Temperature: {weather_forecast.temp} \n Feels Likes: {weather_forecast.feels_like} \n Sunrise: {weather_forecast.sunrise} \n Sunset: {weather_forecast.sunset}"""
                else:
                    forecast_resp =  f"""City: {weather_forecast.name}\n Forecast: {weather_forecast.weather_desc} \n Temperature: {weather_forecast.temp} \n Feels Likes: {weather_forecast.feels_like} \n Sunrise: {weather_forecast.sunrise} \n Sunset: {weather_forecast.sunset}"""
                    
                return forecast_resp
            else:
                return resp.text
        else:
            return f"Supplied location: {location} is not allowed for searching"
        
    
    def get_air_pollution_info(self, location: str):
        '''
            leverages the Open Weather API to search for pollution AQI data from a supplied city location
            this method will return the value of the AQI based on a forecast returned from the OpenWeather API
            for that location, the increment is set to the current forecast
            
            **Sources**
            
            * [Open Weather Pollution API Documentation](https://openweathermap.org/api/air-pollution)
            
            Args:
                location (str): city in the form of 
            Returns:
                aqi_forecast (str) : returns the parsed attributes from a AQIForecast with details 
                                    about overall AQI forecast, and O3 levels and Pm2.5
                                    
                                    Example:
                                    
                                    
        '''
        
        if self.check_supplied_city(location):
            
            lat, lon = self.city_locations[location.capitalize()] 
            
            current_date = datetime.today().strftime('%Y-%m-%d')
            
            resp = requests.get(f"https://www.airnowapi.org/aq/forecast/latLong/?format=application/json&latitude={lat}&longitude={lon}&date={current_date}&distance=10&API_KEY={self.air_now_api_key}")

            if resp.status_code == 200:
                aqi_forecast = AQIForecast(response_forecast=json.loads(resp.text))
                return f"""AQI Forecast for {aqi_forecast.city}: \n Air Quality Category: {aqi_forecast.aqi_category} \n\n PM2.5 Air Quality: \n AQI: {aqi_forecast.pm25_aqi} \n Risk Levels: {aqi_forecast.pm25_category} \n O3 Air Quality: \n AQI: {aqi_forecast.o3_aqi} \n Risk Levels: {aqi_forecast.o3_category}"""
        else:
            return f"Supplied location: {location} is not allowed for searching AQI"
    
    def _retrieve_city_data(self):
        '''
            takes city_locations file and parses the internal city data with lat/long for each city. 
            inside a dict for later look up from the tool. all cities are unique there are no duplications
            amongst popular cities.
            
            Args: 
                None
            Returns:
                parsed_cities (dict): dict of cities with `{"city": [lat, long]}` format 
    
        '''
        
        city_locations = pd.read_csv('./data/city_locations.csv', header=None, sep=",")
        
        parsed_cities = {}
        
        for city_details in city_locations.values:
            # isolates the city from the 'city, state' format
            location = city_details[0].split(",")[0]
            
            # this will parse the city_name field and the lat/long into the dict 🦇
            parsed_cities[f"{location}"] = [city_details[1], city_details[2]]
        
        return parsed_cities