from flask import Flask, render_template, request
import time
# import serial

app = Flask(__name__)
# ser = serial.Serial('/dev/ttyAMC0', 9600)  # Change port and baud rate accordingly

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST': 
        times_per_day = request.form.get('times_per_day')
        amount_per_time = request.form.get('amount_per_time')
        
        # Send over serial
        # ser.write(f"{times_per_day}, {amount_per_time}\n".encode())\
        with open('params.txt', 'w') as file:
            file.write(f"{times_per_day}, {amount_per_time}\n")

        print(times_per_day, amount_per_time)

    return render_template('index.html')

def run_server():
    app.run(host='0.0.0.0', port=5000)

if __name__ == '__main__':
    run_server()