from flask import Flask, request

app = Flask(__name__)

@app.route('/')
def home():
    return '''
        <form method="POST" action="/input">
            <input type="text" name="user_input">
            <input type="submit" value="Convert">
        </form>
    '''

@app.route('/input', methods=['POST'])
def input():
    user_input = request.form['user_input']   
    celsius = float(user_input)
    celsius = (celsius - 32) / 1.8
    celsius = '{:.1f}'.format(celsius)
    return f'{user_input} Fahrenheit is {celsius} Celsius'

if __name__ == '__main__':
    app.run()