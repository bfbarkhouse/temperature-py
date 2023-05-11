from flask import Flask, request, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')
    
@app.route('/', methods=['GET', 'POST'])
def results():
    user_input = request.form['user_input']
    if not user_input:
        return render_template('index.html', error='Please enter a number.')
    else:
        if request.form["unit"] == "celsius":
            return convert_to_celsius(user_input)
        elif request.form["unit"] == "fahrenheit":
            return convert_to_fahrenheit(user_input)


def convert_to_celsius(user_input): 
    celsius = float(user_input)
    celsius = (celsius - 32) / 1.8
    celsius = '{:.1f}'.format(celsius)
    return render_template('index.html', title='Results', input=user_input, from_unit='Fahrenheit is', to_unit='in Celsius', result=celsius)

def convert_to_fahrenheit(user_input):  
    fahrenheit = float(user_input)
    fahrenheit = (fahrenheit * 9/5) + 32
    fahrenheit = '{:.1f}'.format(fahrenheit)
    return render_template('index.html', title='Results', input=user_input, from_unit='Celsius is', to_unit=' in Fahrenheit', result=fahrenheit)

if __name__ == '__main__':
    app.run()