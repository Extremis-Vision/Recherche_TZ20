import requests

def weather(city="Seppois-le-Haut"):
    api_key = 'bb158fe427638ce39503671c8179386d'
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric'
    
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        liste = {}
        liste["temperature"] = data['main']['temp']
        liste["description"] = data['weather'][0]['description']
        liste["humiditer"] = data['main']["humidity"]
        liste["temp_max"] = data['main']["temp_max"]
        liste["temp_min"] = data['main']["temp_min"]

        return "La temperature est de " + str(liste["temperature"]) + "°C, la description est " + liste["description"] + ", l'humidité est de " + str(liste["humiditer"]) + "%, la température maximale est de " + str(liste["temp_max"]) + "°C et la température minimale est de " + str(liste["temp_min"]) + "°C."
    else:
        return None    
    
#print(weather())