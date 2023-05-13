from flask import Flask, request, render_template
import logging
import requests
#import json

app = Flask(__name__)
logging.basicConfig(filename='temp_convert.log', encoding='utf-8', level=logging.DEBUG)

def getWeather():
    #get user location?
    #load weather from API
    weather_data = requests.get("https://api.open-meteo.com/v1/forecast?latitude=43.01&longitude=-71.42&timezone=GMT&forecast_days=1&daily=temperature_2m_max,temperature_2m_min")
    print(f'Response from weather API: {weather_data.status_code}')
    #parse max and min temps and populate global variables
    global day_max
    day_max = str(weather_data.json()['daily']['temperature_2m_max']).strip('[]')
    global day_min
    day_min = str(weather_data.json()['daily']['temperature_2m_min']).strip('[]')
    global day_unit
    day_unit = str(weather_data.json()['daily_units']['temperature_2m_max']).strip('[]')
    print(day_max, day_min, day_unit)
    return(day_max, day_min, day_unit)

@app.get('/')
def home():
    getWeather()
    return render_template('index.html', day_max=day_max, day_min=day_min, daily_unit=day_unit)
    
@app.post('/') #, methods=['POST'])
def results():
    user_input = request.form['user_input']
    ip_addr = request.environ.get('HTTP_X_FORWARDED_FOR', request.remote_addr)
    if not user_input:
        logging.info('Request from %s did not enter a number', ip_addr)
        print(f'Request from {ip_addr} did not enter a number')
        return render_template('index.html', result_container='notification is-primary', error='Please enter a number.', day_max=day_max, day_min=day_min, daily_unit=day_unit)
    elif 'unit' not in request.form:
        logging.info('Request from %s did not select a unit', ip_addr)
        print(f'Request from {ip_addr} did not select a unit')
        return render_template('index.html', result_container='notification is-primary', error='Please select a unit.', day_max=day_max, day_min=day_min, daily_unit=day_unit)
    else:
        if request.form["unit"] == "celsius":
            return convert_to_celsius(user_input, ip_addr)
        elif request.form["unit"] == "fahrenheit":
            return convert_to_fahrenheit(user_input, ip_addr)

def convert_to_celsius(user_input, ip_addr): 
    logging.info('User at %s entered %s', ip_addr, user_input)
    print (f'User at {ip_addr} entered {user_input}')
    celsius = float(user_input)
    celsius = (celsius - 32) / 1.8
    celsius = '{:.1f}'.format(celsius)
    return render_template('index.html', title='Results', input=user_input, from_unit='Fahrenheit is', to_unit='in Celsius', result_container='notification is-primary', result=celsius, day_max=day_max, day_min=day_min, daily_unit=day_unit)

def convert_to_fahrenheit(user_input, ip_addr):
    logging.info('User at %s entered %s', ip_addr, user_input)
    print (f'User at {ip_addr} entered {user_input}')  
    fahrenheit = float(user_input)
    fahrenheit = (fahrenheit * 9/5) + 32
    fahrenheit = '{:.1f}'.format(fahrenheit)
    return render_template('index.html', title='Results', input=user_input, from_unit='Celsius is', to_unit=' in Fahrenheit', result_container='notification is-primary', result=fahrenheit, day_max=day_max, day_min=day_min, daily_unit=day_unit)

if __name__ == '__main__':
    app.run()
    #app.run(debug=True)