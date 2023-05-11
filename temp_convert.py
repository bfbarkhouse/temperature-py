from flask import Flask, request

app = Flask(__name__)

@app.route('/')
def home():
    return '''
        <form method="POST" action="/input">
            <input type="text" name="user_input"><br>
            <input type="radio" name="unit" id="celsius" value="celsius"> Convert to Celsius </input>
            <input type="radio" name="unit" id="fahrenheit" value="fahrenheit"> Convert to Fahrenheit </input><br>
            <input type="submit" name="submit" value="Convert">
        </form>
    '''

@app.route('/input', methods=['POST'])
def results():
    user_input = request.form['user_input']
    if request.form["unit"] == "celsius":
        return convert_to_celsius(user_input)
    elif request.form["unit"] == "fahrenheit":
        return convert_to_fahrenheit(user_input)

def convert_to_celsius(user_input):
    #user_input = request.form['user_input']   
    celsius = float(user_input)
    celsius = (celsius - 32) / 1.8
    celsius = '{:.1f}'.format(celsius)
    return f'{user_input} Fahrenheit is {celsius} Celsius'

def convert_to_fahrenheit(user_input):
    #user_input = request.form['user_input']   
    fahrenheit = float(user_input)
    fahrenheit = (fahrenheit * 9/5) + 32
    fahrenheit = '{:.1f}'.format(fahrenheit)
    return f'{user_input} Celsius is {fahrenheit} Fahrenheit'

if __name__ == '__main__':
    app.run()