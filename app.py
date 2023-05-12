from flask import Flask, request, render_template
import logging

app = Flask(__name__)
logging.basicConfig(filename='temp_convert.log', encoding='utf-8', level=logging.DEBUG)

@app.route('/')
def home():
    return render_template('index.html')
    
@app.route('/', methods=['GET', 'POST'])
def results():
    user_input = request.form['user_input']
    ip_addr = request.environ.get('HTTP_X_FORWARDED_FOR', request.remote_addr)
    if not user_input:
        logging.info('Request from %s did not enter a number', ip_addr)
        print(f'Request from {ip_addr} did not enter a number')
        return render_template('index.html', result_container='notification is-primary', error='Please enter a number.')
    elif 'unit' not in request.form:
        logging.info('Request from %s did not select a unit', ip_addr)
        print(f'Request from {ip_addr} did not select a unit')
        return render_template('index.html', result_container='notification is-primary', error='Please select a unit.')
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
    return render_template('index.html', title='Results', input=user_input, from_unit='Fahrenheit is', to_unit='in Celsius', result_container='notification is-primary', result=celsius)

def convert_to_fahrenheit(user_input, ip_addr):
    logging.info('User at %s entered %s', ip_addr, user_input)
    print (f'User at {ip_addr} entered {user_input}')  
    fahrenheit = float(user_input)
    fahrenheit = (fahrenheit * 9/5) + 32
    fahrenheit = '{:.1f}'.format(fahrenheit)
    return render_template('index.html', title='Results', input=user_input, from_unit='Celsius is', to_unit=' in Fahrenheit', result_container='notification is-primary', result=fahrenheit)

if __name__ == '__main__':
    app.run(debug=True)