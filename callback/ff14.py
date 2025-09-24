# import json
from EorzeaEnv import EorzeaLang, EorzeaTime, EorzeaWeather, EorzeaPlaceName, EorzeaRainbow
from data.weather import weather_dict

weather_map = weather_dict

def get_weather(area):
    target_area = weather_map.get(area)
    if not target_area:
        return None

    # weather_forecast_list = [f"{place_name} | {' --> '.join(EorzeaWeather.forecast(EorzeaPlaceName(place_name, strict=False), EorzeaTime.weather_period(step=2), lang=EorzeaLang.KO))}" for place_name in target_area]
    weather_forecast_list = [" --> ".join(EorzeaWeather.forecast(EorzeaPlaceName(place_name, strict=False), EorzeaTime.weather_period(step=2), lang=EorzeaLang.KO)) for place_name in target_area]
    return (target_area, weather_forecast_list)

def get_et():
    et_now = EorzeaTime().now()
    return f"{et_now.hour}:{et_now.minute}"

if __name__ == '__main__':
    print(get_weather('황금'))