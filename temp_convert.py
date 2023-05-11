from flask import Flask, request, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')
    # return '''
    # <!-- index.html -->
    # <!DOCTYPE html>
    # <html lang="en">
    # <head>
    # <meta charset="utf-8">
    # <meta name="viewport" content="width=device-width, initial-scale=1">
    # <title>Temperature Conversion</title>
    # <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bulma@0.9.4/css/bulma.min.css">
    # </head>
    # <body>
    # <section class="section">
    # <div class="container">
    #     <h1 class="title">Temperature Conversion</h1>
    #     <p class="subtitle"><form method="POST" action="/input">
    #         <input type="text" name="user_input"><br>
    #         <input type="radio" name="unit" id="celsius" value="celsius"> Convert to Celsius </input>
    #         <input type="radio" name="unit" id="fahrenheit" value="fahrenheit"> Convert to Fahrenheit </input><br>
    #         <input type="submit" name="submit" value="Convert">
    #     </form>
    #     </p>
    # </div>
    # </section>
    # </body>
    # </html>
    # '''

# @app.route('/input', methods=['POST'])
# def results():
#     user_input = request.form['user_input']
#     if request.form["unit"] == "celsius":
#         return convert_to_celsius(user_input)
#     elif request.form["unit"] == "fahrenheit":
#         return convert_to_fahrenheit(user_input)
@app.route('/', methods=['GET', 'POST'])
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
    #return f'{user_input} Fahrenheit is {celsius} Celsius'
    return render_template('index.html', title='Results', input=user_input, from_unit='Fahrenheit is', to_unit='in Celsius', result=celsius)

def convert_to_fahrenheit(user_input):
    #user_input = request.form['user_input']   
    fahrenheit = float(user_input)
    fahrenheit = (fahrenheit * 9/5) + 32
    fahrenheit = '{:.1f}'.format(fahrenheit)
    #return f'{user_input} Celsius is {fahrenheit} Fahrenheit'
    return render_template('index.html', title='Results', input=user_input, from_unit='Celsius is', to_unit=' in Fahrenheit', result=fahrenheit)

if __name__ == '__main__':
    app.run()