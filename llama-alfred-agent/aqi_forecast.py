

class AQIForecast:
    '''
        AQIForecast class to ensure that the pm25 and o3 levels are parsed 
        from an incoming dict
    '''
    def __init__(self, response_forecast: dict):
        self._parse_aqi_forecast(response_forecast)
        
        self.city
        self.aqi_category
        
        self.pm25_aqi
        self.pm25_category
        
        self.o3_aqi
        self.o3_category
        
    def _parse_aqi_forecast(self, response_forecast: dict):
        o3_forecast_resp = response_forecast[1]
        
        pm25_forecast_resp = response_forecast[2]
        
        self.city = o3_forecast_resp["ReportingArea"]
        self.aqi_category = pm25_forecast_resp["Category"]["Name"]
        
        self.o3_aqi = o3_forecast_resp["AQI"]
        self.o3_category = f"Number: {o3_forecast_resp["Category"]["Number"]} | Category: {o3_forecast_resp["Category"]["Name"]}" 
        
        
        pm25_forecast_resp = response_forecast[2]
        
        self.pm25_aqi = pm25_forecast_resp["AQI"]
        self.pm25_category = f"Number: {pm25_forecast_resp["Category"]["Number"]} | Category: {pm25_forecast_resp["Category"]["Name"]}" 
        
    