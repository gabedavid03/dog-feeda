from flask import Flask, render_template, request
import json
# import serial

app = Flask(__name__)
# ser = serial.Serial('/dev/ttyAMC0', 9600)  # Change port and baud rate accordingly

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST': 
        feeds_per_day = request.form.get('times_per_day')
        amount_per_feed = request.form.get('amount_per_time')
        
        # Send over serial
        # ser.write(f"{times_per_day}, {amount_per_time}\n".encode())\
        with open('params.json', 'r') as file:
            try:
                params = json.load(file)
            except json.JSONDecodeError:
                params = {}
            params['FEEDS_PER_DAY'] = feeds_per_day
            params['AMOUNT_PER_FEED'] = amount_per_feed

        with open('params.json', 'w') as file:
            json.dump(params, file, indent=4)        

    return render_template('index.html')

def run_server():
    app.run(host='0.0.0.0', port=5000)

if __name__ == '__main__':
    run_server()