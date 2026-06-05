import requests

def get_user_input():
    try:
        latitude = float(input('Enter latitude: '))
        longitude = float(input('Enter longitude: '))
        timezone = input('Enter timezone: ')
        return latitude, longitude, timezone
    except ValueError:
        print('Invalid value')
        return

def build_params(latitude, longitude, timezone):

    params = {
        'latitude' : latitude,
        'longitude' : longitude,
        'current' : ['temperature_2m', 'wind_speed_10m'],
        'timezone' : timezone
    }

    return params

def show_weather(data):
    print(f"Temperature: {data['current']['temperature_2m']} °C")
    print(f"Wind speed: {data['current']['wind_speed_10m']} km/h")


def get_weather():
    
    latitude, longitude, timezone = get_user_input()
    params = build_params(latitude, longitude, timezone)
    
    try:
        response = requests.get('https://api.open-meteo.com/v1/forecast', params=params, timeout=5)
    except requests.exceptions.ConnectionError: 
        print('No connection')
        return
    except requests.exceptions.Timeout:
        print('The waiting time has expired')
        return
    try:
        response.raise_for_status()
    except requests.exceptions.HTTPError as error:
        print(f'Error: {error}')
        return

    try:
        data = response.json()
        show_weather(data)
    except requests.exceptions.JSONDecodeError:
        print('The response from the server was not in the correct format')

get_weather()