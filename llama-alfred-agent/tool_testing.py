from tools import Tools
from dotenv import load_dotenv
import os
import colorama


def main():
    load_dotenv()
    
    OPEN_WEATHER_API_KEY = os.getenv("OPEN_WEATHER_API_KEY")
    
    AIRNOW_API_KEY = os.getenv("AIRNOW_API_KEY")
    
    tools = Tools(status_updates=True,weather_api_key=OPEN_WEATHER_API_KEY, air_now_api_key=AIRNOW_API_KEY)
    
    print(colorama.Fore.WHITE + "-"*15)
    
    pdx_weather_response = tools.get_weather_info("portland")
    
    print(f"Weather Forecast:\n {pdx_weather_response}")
    print(colorama.Fore.WHITE + "-"*15)
    
    pdx_aqi_response = tools.get_air_pollution_info("portland")
    
    print(f"AQI Forecast:\n {pdx_aqi_response}")
    print(colorama.Fore.WHITE + "-"*15)
    

main()