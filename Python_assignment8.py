from flask import Flask, request, jsonify
import requests

app = Flask(__name__)


API_KEY = "your_openweathermap_api_key"

@app.route('/')
def home():
    return "Welcome to the Weather App! 🌦️ Use /weather?city=<city_name> to get the weather."

@app.route('/weather', methods=['GET'])
def get_weather():
   
    city = request.args.get('city')
    
    if not city:
        return jsonify({"error": "City parameter is required"}), 400

    try:
        api_url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
        response = requests.get(api_url)
        data = response.json()

        if response.status_code != 200:
            return jsonify({"error": data.get("message", "Unable to fetch weather data.")}), response.status_code

        weather_info = {
            "city": data["name"],
            "temperature": data["main"]["temp"],
            "description": data["weather"][0]["description"],
            "humidity": data["main"]["humidity"],
            "wind_speed": data["wind"]["speed"]
        }
        return jsonify(weather_info)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
