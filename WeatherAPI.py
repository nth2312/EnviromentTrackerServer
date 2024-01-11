import requests

def GetWeather(apiKey, city):
    base_url = "http://api.openweathermap.org/data/2.5/weather"
    params = {
        'q': city,
        'appid': apiKey,
        'units': 'metric'
    }

    try:
        response = requests.get(base_url, params=params)
        data = response.json()

        if response.status_code == 200:
            return data['weather'][0]['description']
        else:
            print(f"Error {response.status_code}: {data['message']}")
            data = "clear"
            return data

    except requests.RequestException as e:
        print(f"Error: {e}")

apiKey = "2b1ee2e2dbb1cf55b213fa28591db615"
city = "Hanoi"

#print(GetWeather(apiKey, city))
