from flask import Flask, request, render_template
import requests

app = Flask(__name__)

# API key for OpenWeatherMap
API_KEY = '9f36f69dc631e636ec1a96fb2c950120'
BASE_URL = 'http://api.openweathermap.org/data/2.5/weather'

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        city = request.form['city']
        if city:
            weather_data = get_weather(city)
            if weather_data:
                return render_template('index.html', weather=weather_data)
            else:
                return render_template('index.html', error='City not found or API error.')
        else:
            return render_template('index.html', error='Please enter a city name.')
    return render_template('index.html')

def get_weather(city):
    params = {
        'q': city,
        'appid': API_KEY,
        'units': 'metric'
    }
    response = requests.get(BASE_URL, params=params)
    if response.status_code == 200:
        data = response.json()
        weather = {
            'city': city,
            'temperature': data['main']['temp'],
            'humidity': data['main']['humidity'],
            'wind_speed': data['wind']['speed'],
            'description': data['weather'][0]['description']
        }
        return weather
    return None

if __name__ == '__main__':
    app.run(debug=False, port=4449)

